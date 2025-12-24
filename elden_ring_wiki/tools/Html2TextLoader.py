from dataclasses import dataclass
import json
import os
import sys
import html2text
import requests
from langchain_core.documents import Document
from bs4 import BeautifulSoup, Tag


@dataclass
class WikiLinkItem:
    title: str
    href: str


class Html2TextLoader:
    def __init__(
        self,
        web_paths: list[str] = [],
        load_from_local=False,
        remove_selectors=[],
        markdown_storage_path=None,
        disable_links=False,
    ):
        self.urls = web_paths
        self.load_from_local = load_from_local
        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_images = True
        self.h.ignore_emphasis = True
        self.h.body_width = 0
        self.remove_selectors = remove_selectors
        self.markdown_storage_path = (
            markdown_storage_path if markdown_storage_path else "./markdown_files"
        )
        self.disable_links = disable_links

    def find_wiki_links(
        self, content: Tag, selector=".wiki_link"
    ) -> list[WikiLinkItem]:
        links = []
        for element in content.select(selector=selector):
            title = (
                element.__getattr__("title")
                if element.__getattr__("title")
                else element.get_text()
            )
            href = element.attrs["href"] if element.attrs["href"] else None
            record = WikiLinkItem(title.strip(), href)
            if record not in links:
                links.append(record)
        return links

    def embed_video_links(self, content: Tag, selector=".youtube"):
        video_links = []
        for element in content.select(selector=selector):
            id = element.attrs["id"] if element.attrs["id"] else None
            if id:
                youtube_link = f"https://www.youtube.com/watch?v={id}"
                element.append(youtube_link)
                video_links.append(youtube_link)
        return video_links

    def save_documents(self, documents: list[Document]):
        for document in documents:
            with open(
                os.path.join(
                    self.markdown_storage_path, f"{document.metadata['title']}.md"
                ),
                "w+",
                encoding="utf-8",
                errors="replace",
            ) as page_content_file:
                page_content_file.write(document.page_content)

                metadata = {
                    "md_file": document.metadata["title"] + ".md",
                    "metadata": document.metadata,
                }
                with open(
                    os.path.join(
                        self.markdown_storage_path, f"{document.metadata['title']}.json"
                    ),
                    "w+",
                    encoding="utf-8",
                    errors="replace",
                ) as metadata_file:
                    json.dump(metadata, metadata_file, indent=4)

    def load_documents_from_local(self) -> list[Document]:
        docs = []
        metadata_files = [
            f
            for f in os.listdir(self.markdown_storage_path)
            if os.path.isfile and f.endswith(".json")
        ]
        for metadata_file in metadata_files:
            with open(
                os.path.join(self.markdown_storage_path, metadata_file), "r", encoding="utf-8"
            ) as metadata_file:
                metadata = json.load(metadata_file)
                with open(
                    os.path.join(self.markdown_storage_path, metadata["md_file"]), "r", encoding="utf-8"
                ) as page_content_file:
                    doc = Document(
                        page_content=page_content_file.read(),
                        metadata=metadata["metadata"],
                    )
                    docs.append(doc)
        return docs

    def load(self) -> list[Document]:
        docs = []
        if self.load_from_local:
            docs = self.load_documents_from_local()

        for url in self.urls:
            try:
                html = requests.get(url).text
                soup = BeautifulSoup(html, "html.parser")

                # Find content area
                content = soup.find("div", {"id": "wiki-content-block"})
                if not content:
                    raise ValueError("Unable to find content block for page")

                if content:
                    for selector in self.remove_selectors:
                        if selector.startswith(".") or selector.startswith("#"):
                            for element in content.select(selector):
                                element.decompose()
                        else:
                            for element in content.find_all(selector):
                                element.decompose()

                    for tag in content(["script", "style", "nav", "footer"]):
                        tag.decompose()

                    wiki_links = self.find_wiki_links(content)
                    if not self.disable_links:
                        video_links = self.embed_video_links(
                            content, self.disable_links
                        )

                    markdown = self.h.handle(str(content))                 

                    title = soup.find("h1")
                    title_text = title.get_text().split("|")[0].strip() if title else ""

                    docs.append(
                        Document(
                            page_content=markdown,
                            metadata={"source": url, "title": title_text, "wiki_links": [link.__dict__ for link in wiki_links]},
                        )
                    )
            except Exception as e:
                print(f"✗ Error: {e}")
        self.save_documents(docs)
        return docs
