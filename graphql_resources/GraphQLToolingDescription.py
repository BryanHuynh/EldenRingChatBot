from marshmallow import pprint
import sgqlc
from my_schema import (
    Query,
    AttributeEntry,
    ScalingEntry,
    AttributeEntryNames,
    ScalingEntryNames,
    ScalingEntryScaling,
)
import json


class GraphQLToolingDescription:
    def __init__(
        self,
        query: sgqlc.types.Type,
        entries: list[sgqlc.types.Type] = None,
        enums: list[sgqlc.types.Enum] = None,
    ):
        self.query = query
        self.entries = entries
        self.enums = enums or []
        self.root_fields = self.get_root_fields() or []
        self.type_fields = self.get_type_fields() or {}
        self.enum_values = self.get_enum_values(self.enums) or {}

    def build_tooling_description(self) -> str:
        overview = self.build_schema_overview()
        examples = self.build_examples()
        base = f"""
Run Dynamic queries against Elden Ring API using a JSON-based query format.

This tool takes in the following input:
- "root": The root field to query from the schema. 
- "args": A dictionary of arguments to filter the results.
- "selection": A nested dictionary specifying which fields to select in the response.

Selection syntax:
- "selection" is a nested JSON object where:
  - keys are field names
  - values are either:
    - None → select that scalar field
    - another object → select nested fields on that object
 - the following comparison operators are supported in "args":
    - "eq": equal to (uses fuzzy matching for strings by default, use when expecting a single result)
    - "neq": not equal to
    - "lt": less than
    - "lte": less than or equal to
    - "gt": greater than
    - "gte": greater than or equal to
    - "contains": value contains substring (for strings). Only use when expecting multiple results.
    - "in": value is in list (for strings)
 - if no selection is given, all fields will be selected by default.
 
Args syntax:
- "args" is a dictionary where:
    - keys are field names
    - values are either:
        - another object -> selected nested fields on that object
        - a tuple of (operator, value) → comparison check
        
Here is the schema overview:
{overview}

Here are some example queries you can use:
{examples}
Provide the response in JSON format based on the information and schema provided.
"""
        return base

    def build_examples(self) -> list[str]:
        examples = []
        examples.append(
            {
                "root": "location",
                "args": {"region": ("eq", "Limgrave")},
                "selection": {
                    "id": None,
                    "name": None,
                    "description": None,
                    "region": None,
                },
            }
        )
        examples.append(
            {
                "root": "shield",
                "args": {
                    "scalesWith": {"scaling": ("gte", "D")},
                    "requiredAttributes": {
                        "name": ("eq", "Str"),
                        "amount": ("gte", 15),
                    },
                },
                "selection": {
                    "id": None,
                    "name": None,
                    "description": None,
                    "defence": {
                        "name": None,
                        "amount": None,
                    },
                    "scalesWith": {
                        "name": None,
                        "scaling": None,
                    },
                    "requiredAttributes": {"name": None, "amount": None},
                    "category": None,
                },
            }
        )

        examples.append(
            {
                "root": "boss",
                "args": {
                    "region": ("in", ["Limgrave", "Mount Gelmir"]),
                },
                "selection": {
                    "id": None,
                    "name": None,
                    "description": None,
                    "region": None,
                },
            }
        )
        example_descriptions = [
            "Get all locations in the Limgrave region with their id, name, description, and region.",
            "Get all shields that scale with at least D scaling and require at least 15 Strength, including their id, name, description, defence stats, scaling details, required attributes, and category.",
            "Get all bosses located in either Limgrave or Mount Gelmir with their id, name, description, and region.",
        ]
        return "\n".join(
            f"example {index}: \n - description: {description} \n```json\n{json.dumps(x, indent=2)}\n```"
            for index, (x, description) in enumerate(
                zip(examples, example_descriptions)
            )
        )

    def build_schema_overview(self) -> str:
        lines: list[str] = []
        lines.append("Available Root Fields:")
        for root in self.root_fields:
            name = getattr(self.query, root).graphql_name
            lines.append(f"- {name}")

        lines.append("\nType Fields:")
        for type_name, fields in self.type_fields.items():
            lines.append(f"{type_name}:")
            for field_name, field_type in fields.items():
                lines.append(f"  - {field_name}: {field_type}")

        lines.append("\nEnum Values:")
        for enum_name, values in self.enum_values.items():
            lines.append(f"{enum_name}: {', '.join(values)}")

        return "\n".join(lines)

    def get_root_fields(self) -> list[str]:
        return [x for x in Query.__field_names__ if not x.startswith("get_")]

    def get_type_fields(self) -> dict[str]:
        roots = self.get_root_fields()
        root_attributes = {}
        for root in roots:
            root_graphql_name = getattr(Query, root).graphql_name
            gql_type = self.__unwrap(getattr(Query, root).type)
            type_dict = self.__type_to_dict(gql_type)
            root_attributes[root_graphql_name] = type_dict

        for entry in self.entries:
            gql_type = self.__unwrap(entry)
            type_dict = self.__type_to_dict(gql_type)
            root_attributes[entry.__name__] = type_dict

        return root_attributes

    def get_enum_values(self, enum_type):
        enum_attributes = {}
        for enum in self.enums:
            enum_attributes[enum.__name__] = list(enum.__choices__)
        return enum_attributes

    def __unwrap(self, t):
        while hasattr(t, "of_type"):
            t = t.of_type
        return t

    def __type_to_dict(self, gql_type):
        result = {}
        for name in gql_type.__field_names__:
            field = getattr(gql_type, name)
            base = self.__unwrap(field.type)
            result[name] = getattr(base, "__name__", str(base))
        return result


if __name__ == "__main__":
    tooling_description = GraphQLToolingDescription(
        query=Query,
        entries=[AttributeEntry, ScalingEntry],
        enums=[AttributeEntryNames, ScalingEntryScaling, ScalingEntryNames],
    )
    overview = tooling_description.build_tooling_description()
    print(overview)
