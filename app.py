import uvicorn
from Logger import Logger
from typing import Any, Optional
from pydantic import Field
from graphql_resources import (
    GraphQLClient,
    GraphQLQueryExecutor,
    GraphQLToolingDescription,
)
from mcp.server.fastmcp import FastMCP
from pprint import pprint
from config import eldenring_api_host
from graphql_resources.my_schema import (
    Query,
    AttributeEntry,
    ScalingEntry,
    AttributeEntryNames,
    ScalingEntryNames,
    ScalingEntryScaling,
)
import json


mcp = FastMCP("DocumentMCP")
graphql_client = GraphQLClient(eldenring_api_host)
graphql_tooling_description = GraphQLToolingDescription(
    Query,
    entries=[AttributeEntry, ScalingEntry],
    enums=[AttributeEntryNames, ScalingEntryScaling, ScalingEntryNames],
)


@mcp.tool(
    name="query_elden_ring_graphql",
    description=graphql_tooling_description.build_tooling_description(),
)
def query_elden_ring_graphql(
    root: str = Field(description="The root field to query from the schema"),
    args: Optional[dict] = Field(
        default=None,
        description="A dictionary of arguments to filter the results. Use operators like eq, neq, gt, gte, lt, lte, contains, in.",
        optional=True,
    ),
    selection: Optional[dict] = Field(
        default=None,
        description="A nested dictionary specifying which fields to select in the response.",
    ),
) -> str:
    """
    Run Dynamic queries against Elden Ring API using a JSON-based query format.
    """

    log = Logger()
    log.debug(
        "query_elden_ring_graphql called with root: %s, args: %s, selection: %s",
        root,
        args,
        selection,
    )

    executor = GraphQLQueryExecutor(graphql_client)
    try:
        result = executor.build_operation(root, selection=selection, args=args)
    except Exception as e:
        log.error("Error building operation: %s", e)
        return {"success": False, "error": str(e)}
    
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    # print(query_elden_ring_graphql(
    #     root="location",
    #     args={"region": ["eq", "Limgrave"]},
    #     selection=None
    # ))
    mcp.run()

# {
#   "region": [
#     "eq",
#     "Limgrave"
#   ]
# }


# {
#   "id": null,
#   "name": null,
#   "description": null,
#   "region": null
# }
