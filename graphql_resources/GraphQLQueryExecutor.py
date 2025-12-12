from typing import Any, Dict
from sgqlc.operation import Operation

from Logger import Logger
from graphql_resources import GraphQLClient
from graphql_resources.my_schema import Query
from rapidfuzz import fuzz, process
import math


class GraphQLQueryExecutor:
    def __init__(self, client: GraphQLClient):
        self._client = client
        self.log = Logger()

    def build_operation(
        self,
        root: str,
        selection: Dict[str, Any] = None,
        args: dict[str, Any] = None,
    ):
        if args is not None and selection is not None:
            self._validate_filter_against_selection(args, selection)

        page = 0
        items = []
        while True:
            op = Operation(Query)
            root_field = getattr(op, root)(page=page)
            if selection is None:
                for field in dir(root_field):
                    getattr(root_field, field)
            else:
                self._apply_selection(root_field, selection)
            response = self._client.execute_query(op)
            if response["success"] == False:
                return response
            data = response["data"]
            if not data[root]:
                break
            else:
                page += 1
                items.extend(data[root])
        if args is None:
            return items
        else:
            filtered_items = [s for s in items if self._matches_filter(s, args)]
            if len(filtered_items) > 0:
                return filtered_items

    def _validate_filter_against_selection(
        self, filt: dict, selection: dict, path: str = ""
    ) -> str:
        for field, condition in filt.items():
            current_path = f"{path}.{field}" if path else field

            if field not in selection:
                raise ValueError(
                    f"Filter field '{current_path}' is not in the selection. Please include it in the query selection."
                )

            if isinstance(condition, dict):
                if not isinstance(selection[field], dict):
                    raise ValueError(
                        f"Filter field '{current_path}' is trying to filter a nested object, but the selection doesn't include nested fields."
                    )

                nested_error = self._validate_filter_against_selection(
                    condition, selection[field], current_path
                )
                if nested_error:
                    raise ValueError(nested_error)

        return None

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

            if isinstance(condition, list) and len(condition) == 2:
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

    ORDER = {"S": 6, "A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "NONE": 0}

    def _coerce_number(self, x: Any) -> Any:
        if x is None:
            return math.nan
        if isinstance(x, (int, float)):
            return x
        if isinstance(x, str):
            if x in self.ORDER:
                return self.ORDER[x]
            else:
                return math.nan
        return x

    def _compare(self, value: Any, op: str, expected: Any) -> bool:
        def fuzzy_contains(
            search_term: str, items_list: list, threshold: int = 90
        ) -> bool:
            if not items_list:
                return False

            result = process.extractOne(
                search_term,
                items_list,
                scorer=fuzz.partial_ratio,
                score_cutoff=threshold,
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

        if op == "contains" or op == "in":
            if isinstance(expected, list):
                return fuzzy_contains(value, expected)
            return fuzz.partial_ratio(value, expected) >= 90
            
            

        raise ValueError(f"Unknown operator: {op}")
