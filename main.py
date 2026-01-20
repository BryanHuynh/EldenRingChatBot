import os
from Logger import Logger
from typing import Optional
from pydantic import Field
from graphql_resources import (
    GraphQLClient,
    GraphQLQueryExecutor,
    GraphQLToolingDescription,
)
from mcp.server.fastmcp import FastMCP
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


mcp = FastMCP("Elden Ring Companion")
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


RESOURCE_MEMORY = {}


def register_root_resource(root: str):
    @mcp.resource(
        f"elden://{root}",
        description=f"Resource for Elden Ring {root} data",
        name=f"{root}",
    )
    async def _resource():
        if root in RESOURCE_MEMORY:
            return RESOURCE_MEMORY[root]
        executor = GraphQLQueryExecutor(graphql_client)
        result = executor.build_operation(root, {"name": None}, {})
        RESOURCE_MEMORY[root] = result
        return result


for root_field in graphql_tooling_description.get_root_fields():
    register_root_resource(root_field)

if __name__ == "__main__":
    log = Logger()
    log.info("MCP Server started successfully")
    log.info(f"Current working directory: {os.getcwd()}")
    mcp.run(transport="stdio")
