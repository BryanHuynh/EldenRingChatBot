from typing import Any, Dict
from sgqlc.operation import Operation

from graphql_resources import GraphQLClient
from graphql_resources.my_schema import Query
from rapidfuzz import fuzz, process


class GraphQLQueryExecutor:
    def __init__(self, client: GraphQLClient):
        self._client = client

    def build_operation(
        self,
        root: str,
        selection: Dict[str, Any] = None,
        args: dict[str, Any] = None,
    ):
        page = 0
        while True:
            op = Operation(Query)
            root_field = getattr(op, root)(page=page)
            if selection is None:
                for field in dir(root_field):
                    getattr(root_field, field)
            else:
                self._apply_selection(root_field, selection)
            response = self._client.execute_query(op)
            if(response['success'] == False):
                return response
            data = response["data"]
            if not data[root]:
                return []
            items = data[root]
            if args is None:
                return items
            else:
                filtered_items = [s for s in items if self._matches_filter(s, args)]
                if len(filtered_items) > 0:
                    return filtered_items
                page += 1

    def _apply_selection(self, field_obj, selection: dict):
        for name, sub in selection.items():
            child = getattr(field_obj, name)()
            if isinstance(sub, dict):
                self._apply_selection(child, sub)

    def _matches_filter(self, obj: Any, filt: dict) -> bool:
        if obj is None:
            return False
        for field, condition in filt.items():
            value = (
                obj.get(field) if isinstance(obj, dict) else getattr(obj, field, None)
            )

            if isinstance(condition, tuple):
                op, expected = condition
                if not self._compare(value, op, expected):
                    return False

            elif isinstance(condition, dict):
                if isinstance(value, list):
                    if not any(self._matches_filter(v, condition) for v in value):
                        return False
                elif isinstance(value, dict):
                    if not self._matches_filter(value, condition):
                        return False
                else:
                    return False

            else:
                if value != condition:
                    return False
        return True

    def _coerce_number(self, x: Any) -> Any:
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, str):
            try:
                return int(x)
            except ValueError:
                try:
                    return float(x)
                except ValueError:
                    return x
        return x

    def _compare(self, value: Any, op: str, expected: Any) -> bool:
        def fuzzy_contains(search_term: str, items_list: list, threshold: int = 90) -> bool:
            if not items_list:
                return False
            
            result = process.extractOne(
                search_term,
                items_list,
                scorer=fuzz.partial_ratio,
                score_cutoff=threshold
            )
            
            return result is not None


        if op == "eq":
            return fuzz.partial_ratio(value, expected) >= 90
        if op == "ne":
            return value != expected

        v_num = self._coerce_number(value)
        e_num = self._coerce_number(expected)

        if op == "gt":
            return v_num > e_num
        if op == "gte":
            return v_num >= e_num
        if op == "lt":
            return v_num < e_num
        if op == "lte":
            return v_num <= e_num

        if op == "contains":
            return fuzzy_contains(value, expected)

        raise ValueError(f"Unknown operator: {op}")
