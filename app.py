from graphql_resources import GraphQLClient, GraphQLQueryExecutor
from pprint import pprint
from config import eldenring_api_host

if __name__ == "__main__":
    client = GraphQLClient(eldenring_api_host)

    executor = GraphQLQueryExecutor(client)
    result = executor.build_operation(
        "boss",
        args={"name": ("contains", ["Mohg", "Malenia"])},
        selection={"name": None, "location": None, "drops": None},
    )
    print(result)

    # strainer = bs4.SoupStrainer("div", {"id": "wiki-content-block"})

    # loader = WebBaseLoader(
    #     web_paths=("https://eldenring.wiki.fextralife.com/Axe+of+Godrick",),
    #     bs_kwargs={"parse_only": strainer},
    # )
    # data = loader.load()
    # pprint(data[0].page_content.replace("\n+", "\n"))
