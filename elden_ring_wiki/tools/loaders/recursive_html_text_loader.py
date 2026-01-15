from .html_to_text_loader import Html2TextLoader
from langchain_core.documents import Document
import urllib.parse


class RecursiveHtmlTextLoader(Html2TextLoader):
    def __init__(
        self,
        base_url: str,
        starting_urls: list[str],
        remove_selectors=[],
        markdown_storage_path=None,
        disable_links=False,
        **kwargs,
    ):
        super().__init__(
            web_paths=starting_urls,
            load_from_local=False,
            remove_selectors=remove_selectors,
            markdown_storage_path=markdown_storage_path,
            disable_links=disable_links,
        )
        self.starting_urls = starting_urls
        self.visited_urls = set()
        self.exclusions = kwargs.get("exclusions", [])

    def recursive_load(
        self, urls: list[str] = None, depth: int = 0, depth_limit: int = 5
    ) -> list[Document]:
        if depth > depth_limit:
            return []

        if urls is None:
            urls = self.urls

        docs = []
        for url in urls:
            if any(url.startswith(exclusion) for exclusion in self.exclusions):
                continue
            if url.startswith("https://") and url not in self.base_urls:
                continue

            if url.startswith("/"):
                complete_url = urllib.parse.urljoin(self.base_url, url)

            if url not in self.visited_urls:
                self.visited_urls.add(url)
                documents = self.load(urls=[complete_url])
                docs.extend(documents)
                wiki_links = sum(
                    [documents.metadata["wiki_links"] for documents in documents], []
                )
                new_urls = [link["href"] for link in wiki_links if link]
                docs.extend(self.recursive_load(urls=new_urls, depth=depth + 1))
        return docs
