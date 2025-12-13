import os
import html2text
import requests
from langchain_core.documents import Document
from bs4 import BeautifulSoup


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

                    video_links = content.find_all(
                        "div", {"class": "youtube youtubebuildembed"}
                    )
                    for video_link in video_links:
                        id = video_link.attrs["id"]
                        youtube_link = f"https://www.youtube.com/watch?v={id}"
                        video_link.append(youtube_link)

                    markdown = self.h.handle(str(content))

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


