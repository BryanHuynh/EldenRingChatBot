import json
import os
import sys
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_classic.storage import LocalFileStore
from langchain_classic.storage import create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from typing import Optional
from tqdm import tqdm
from elden_ring_wiki.tools.retrievers.RetrieverBuilder import RetrieverBuilder
from .splitters.WikiChildSplitter import WikiChildSplitter
from .formatters import FormatBuilder


class WikiVectorStore:
    def __init__(
        self,
        persist_directory: str,
        collection_name: str,
        embedding_function: str = "nomic-embed-text",
        base_url: str = "http://localhost:11434",
        docstore_directory: Optional[str] = None,
        llm_model: str = "llama3.2",
        format_documents: bool = True,
        use_ParentChildRetriever: bool = False,
        parent_doc_store_path: str = "./parent_docs_store",
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OllamaEmbeddings(model=embedding_function, base_url=base_url)
        self.llm_model = llm_model
        self.docstore_directory = docstore_directory
        self.vectorstore = self.get_or_create_vectorstore()
        self.format_documents = format_documents
        self.useParentChildRetriever = use_ParentChildRetriever
        if self.useParentChildRetriever:
            self.parent_doc_store_path = parent_doc_store_path
            fs = LocalFileStore(self.parent_doc_store_path)
            self.parent_store = create_kv_docstore(fs)
            self.parent_retriever = ParentDocumentRetriever(
                vectorstore=self.vectorstore,
                docstore=self.parent_store,
                child_splitter=WikiChildSplitter(),
            )
        self._llm = None

    def get_or_create_vectorstore(self):
        if os.path.exists(self.persist_directory):
            print(f"Loading existing vectorstore: {self.collection_name}")
            vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
        else:
            print(f"Creating new vectorstore: {self.collection_name}")
            vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
        return vectorstore

    def get_existing_document_metadata(self) -> set[str]:
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized")
        collection = self.vectorstore._collection
        all_data = collection.get(include=["metadatas"])
        meta_datas = all_data["metadatas"]
        meta_data_set = set(
            [json.dumps(metadata, sort_keys=True) for metadata in meta_datas]
        )
        return meta_data_set

    def upsert_documents(self, documents: list[Document]):
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized")
        for document in tqdm(documents, desc="Upserting documents", file=sys.stdout):
            tqdm.write(f"Processing document: {document.metadata['title']}")
            if self.format_documents:
                builder = FormatBuilder(document.page_content)
                formated_page_content = (
                    builder.append_h4_to_subheaders()
                    .remove_gallery_content()
                    .remove_video_guide()
                    .remove_empty_sections()
                    .remove_multiple_empty_lines()
                    .build()
                )
                document.page_content = formated_page_content
            if self.useParentChildRetriever:
                # remove wiki_links from metadata since upsert can't handle list
                del document.metadata["wiki_links"]
                self.parent_retriever.add_documents([document])
            else:
                self.vectorstore.add_documents([document])

    def get_retriever(
        self,
        search_type: str = "similarity",
        filter_dict: Optional[dict] = None,
        use_bm25: bool = False,
        bm25_k: int = 5,
        bm25_alpha: float = 0.5,
        bm25_weight: float = 0.25,
        use_reranker: bool = False,
        reranker_top_n: int = 10,
        k_init: int = 100,
        **search_kwargs,
    ):
        if filter_dict:
            search_kwargs["filter"] = filter_dict

        # If not using BM25 or reranker, return simple retriever
        if not use_bm25 and not use_reranker:
            return self.vectorstore.as_retriever(
                search_type=search_type, **search_kwargs
            )

        # Use RetrieverBuilder for advanced retrieval
        builder = RetrieverBuilder(
            vector_store=self.vectorstore,
            k_init=k_init,
            base_retriever_search_type=search_type,
        )

        if use_bm25:
            builder.add_bm25_retriever(k=bm25_k, alpha=bm25_alpha, weight=bm25_weight)

        if use_reranker:
            builder.add_reranker(top_n=reranker_top_n)

        return builder.build()
