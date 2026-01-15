from langchain_text_splitters import TextSplitter
from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


class WikiChildSplitter(TextSplitter):
    def __init__(self, chunk_size: int = 2000, chunk_overlap_ratio: float = 0.2):
        super().__init__(chunk_size=chunk_size, chunk_overlap=int(chunk_size * chunk_overlap_ratio))

    def split_text(self, text: str) -> list[str]:
        headers_to_split_on = [
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
            ("####", "h4"),
        ]

        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on, strip_headers=True
        )

        sub_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )
        
        all_splits: list[Document] = []
        splits: list[Document] = splitter.split_text(text)
        for split in splits:
            if len(split.page_content) > self._chunk_size:
                sub_splits = sub_splitter.split_text(split.page_content)
                for index, sub_split in enumerate(sub_splits):
                    meta_data = split.metadata.copy()
                    meta_data["sub_chunk"] = index + 1
                    meta_data["total_sub_chunks"] = len(sub_splits)
                    sub_document = Document(page_content=sub_split, metadata=meta_data)
                    all_splits.append(sub_document)
            else:
                all_splits.append(split)

        enriched_splits: list[Document] = [self._enrich_document_page_content_with_metadata(doc) for doc in all_splits]
        return [doc.page_content for doc in enriched_splits]
                
  
    def _enrich_document_page_content_with_metadata(self, document: Document):
        metadata_fields = ["title", "h1", "h2", "h3", "h4", "h5", "h6", "sub_chunk", "total_sub_chunks"]
        metadata_text = []
        for field in metadata_fields:
            if field in document.metadata:
                value = str(document.metadata[field]).strip()
                if value and value not in metadata_text:
                    metadata_text.append(value)

        context_prefix = " > ".join(metadata_text)
        document.page_content = f"{context_prefix}\n\n{document.page_content}"

        return document