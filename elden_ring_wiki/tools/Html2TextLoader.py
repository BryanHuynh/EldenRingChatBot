from dataclasses import dataclass
import os
import html2text
import requests
from langchain_core.documents import Document
from bs4 import BeautifulSoup, Tag
from config import wiki_markdown_directory

@dataclass
class WikiLinkItem:
    title: str
    href: str
    
class Html2TextLoader:
    def __init__(
        self, web_paths: list[str], remove_selectors=[], markdown_storage_path=None
    ):
        self.urls = web_paths
        self.h = html2text.HTML2Text()
        self.h.ignore_links = True
        self.h.ignore_images = True
        self.h.ignore_emphasis = True
        self.h.body_width = 0
        self.remove_selectors = remove_selectors
        self.markdown_storage_path = (
            markdown_storage_path if markdown_storage_path else "./markdown_files"
        )
        
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
            if(record not in links):
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


    def load(self) -> list[Document]:
        docs = []

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
                    video_links = self.embed_video_links(content)

                    markdown = self.h.handle(str(content))

                    markdown += "## Links to related terms in article \n"
                    for wiki_link in wiki_links:
                        markdown += f"[{wiki_link.title}]({wiki_link.href}) \n"

                    title = soup.find("h1")
                    title_text = title.get_text(strip=True) if title else ""

                    docs.append(
                        Document(
                            page_content=markdown,
                            metadata={"source": url, "title": title_text},
                        )
                    )
                    with open(
                        os.path.join(
                            self.markdown_storage_path, f"{url.split('/')[-1]}.md"
                        ),
                        "w+",
                        encoding="utf-8",
                        errors="replace",
                    ) as f:
                        f.write(markdown)

            except Exception as e:
                print(f"✗ Error: {e}")

        return docs


if __name__ == "__main__":
    Html2TextLoader(
        ["https://eldenring.wiki.fextralife.com/Black+Knight+Edredd", "https://eldenring.wiki.fextralife.com/Spirit+Ashes"],
        markdown_storage_path=wiki_markdown_directory,
        remove_selectors=["#tagged-pages-container"],
    ).load()
