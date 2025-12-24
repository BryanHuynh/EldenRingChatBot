from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


def _enrich_documents_page_content_with_metadata(documents: list[Document]):
    for document in documents:
        metadata_fields = ["title", "h1", "h2", "h3", "h4", "h5", "h6"]
        metadata_text = []

        # Build hierarchical context using > separator for clarity
        for field in metadata_fields:
            if field in document.metadata:
                value = document.metadata[field].strip()
                if value and value not in metadata_text:
                    metadata_text.append(value)

        # Create rich context prefix with hierarchical structure
        context_prefix = " > ".join(metadata_text)
        document.page_content = f"{context_prefix}\n\n{document.page_content}"

        # Add chunk position info for better debugging and tracking
        if "sub_chunk" in document.metadata and "total_sub_chunks" in document.metadata:
            document.metadata["chunk_info"] = f"{document.metadata['sub_chunk']}/{document.metadata['total_sub_chunks']}"

    return documents


def split_wiki_documents(
    documents: list[Document],
    max_embeddings: int = 2000,
    chunk_overlap_ratio: float = 0.2
) -> list[Document]:
    """
    Split wiki documents into chunks optimized for retrieval.

    Args:
        documents: List of documents to split
        max_embeddings: Maximum chunk size in characters (default: 2000, increased for better context)
        chunk_overlap_ratio: Ratio of overlap between chunks (default: 0.2)

    Returns:
        List of split and enriched documents
    """

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
        chunk_size=max_embeddings,
        chunk_overlap=int(max_embeddings * chunk_overlap_ratio),
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    all_splits: list[Document] = []
    for document in documents:
        splits = splitter.split_text(document.page_content)
        for split in splits:
            if len(split.page_content) > max_embeddings:
                sub_splits = sub_splitter.split_documents([split])
                for i, sub_split in enumerate(sub_splits):
                    sub_split.metadata["source"] = document.metadata["source"]
                    sub_split.metadata["title"] = document.metadata["title"]
                    sub_split.metadata["sub_chunk"] = i + 1
                    sub_split.metadata["total_sub_chunks"] = len(sub_splits)
                    sub_split.page_content = (
                        f"{document.metadata['title']}\n{sub_split.page_content}"
                    )
                    all_splits.append(sub_split)
            else:
                split.metadata["source"] = document.metadata["source"]
                split.metadata["title"] = document.metadata["title"]
                all_splits.append(split)
    enriched_splits = _enrich_documents_page_content_with_metadata(all_splits)
    return enriched_splits
