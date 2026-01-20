import os
from Logger import Logger
from typing import Optional
from pydantic import Field
from elden_ring_wiki import MDVectorStore
from graphql_resources import (
    GraphQLClient,
    GraphQLQueryExecutor,
    GraphQLToolingDescription,
)
from mcp.server.fastmcp import FastMCP
from config import (
    eldenring_api_host,
    wiki_vectorstore_collection_name,
    wiki_vectorstore_embedding_function,
    wiki_vectorstore_persist_directory,
)
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

wiki_vector_store: MDVectorStore = None
vector_store_retriever = None


@mcp.tool(
    name="search_elden_ring_wiki",
    description="""
    Returns relevant context from the wiki that should be used to answer
    questions about Elden Ring game mechanics, lore and guides.

    When using the retrieved context:
    - Answer based ONLY on the provided context
    - Cite specific details from the context
    - Be precise with stats and numbers
    - If context doesn't contain the answer, say so

    Args:
        query: The search query about Elden Ring
    """,
)
def search_elden_ring_wiki(
    query: str = Field(description="The search query about Elden Ring"),
) -> str:
    log = Logger()
    log.debug("search_elden_ring_wiki called with query: %s", query)
    global wiki_vector_store
    global vector_store_retriever
    if wiki_vector_store is None:
        log.info("Initializing wiki vectorstore")
        wiki_vector_store = MDVectorStore(
            persist_directory=wiki_vectorstore_persist_directory,
            collection_name=wiki_vectorstore_collection_name,
            embedding_function=wiki_vectorstore_embedding_function,
        )
        wiki_vector_store.get_or_create_vectorstore()

    if vector_store_retriever is None:
        log.info("Initializing wiki retriever")
        vector_store_retriever = wiki_vector_store.get_retriever()

    results = vector_store_retriever.invoke(query)
    data = {
        "query": query,
        "num_results": len(results),
        "results": [
            {
                "title": result.metadata["title"],
                "content": result.page_content,
            }
            for result in results
        ],
    }
    json_data = json.dumps(data, indent=2)
    log.debug("search_elden_ring_wiki results: %s", json_data)
    return json_data


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
