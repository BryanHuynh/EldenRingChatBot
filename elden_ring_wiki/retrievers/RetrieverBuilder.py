from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.retrievers import BaseRetriever
from langchain_classic.retrievers import EnsembleRetriever
from dataclasses import dataclass
from langchain_classic.retrievers.contextual_compression import (
    ContextualCompressionRetriever,
)
from langchain_community.document_compressors import FlashrankRerank
from langchain_core.documents import Document


@dataclass
class RetrieverConfig:
    retriever: BaseRetriever
    weight: float


class RetrieverBuilder:
    def __init__(
        self,
        vector_store: Chroma,
        k_init: int = 100,
        base_retriever_search_type: str = "similarity",
        use_parent_child_retriever: bool = False,
    ):
        self.vector_store = vector_store
        self.base_retriever_search_type = base_retriever_search_type
        self.base_retriever = vector_store.as_retriever(
            search_type=base_retriever_search_type, **{"k": k_init}
        )
        self.retrievers: list[RetrieverConfig] = [RetrieverConfig(self.base_retriever, 0.5)]
        self.use_reranker = False
        self.reranker_top_n = 10
        self.use_embeddings_filter = False
        self.embeddings_filter_config = {}
        self.use_parent_child_retriever = use_parent_child_retriever

    def add_retriver(self, retriever_name: str, retriever: BaseRetriever, weight):
        self.retrievers[retriever_name] = RetrieverConfig(retriever, weight)
        return self

    def add_bm25_retriever(
        self, k: int = 100, alpha: float = 0.5, weight: float = 0.25
    ):
        collection = self.vector_store._collection
        collection_data = collection.get()

        # Convert the collection data to Document objects
        docs = []
        for i, doc_id in enumerate(collection_data.get("ids", [])):
            doc = Document(
                page_content=collection_data["documents"][i],
                metadata=collection_data.get("metadatas", [{}])[i] if collection_data.get("metadatas") else {}
            )
            docs.append(doc)

        bm25_retriever = BM25Retriever.from_documents(
            documents=docs,
            k=k,
        )
        self.retrievers.append(RetrieverConfig(bm25_retriever, weight))
        return self

    def add_embeddings_filter(self, embeddings, similarity_threshold: float = None):
        """Enable embeddings filtering on the final retriever"""
        self.use_embeddings_filter = True
        self.embeddings_filter_config = {
            "embeddings": embeddings,
            "similarity_threshold": similarity_threshold,
        }
        return self

    def add_reranker(self, top_n: int = 10):
        """Enable reranking on the final retriever"""
        self.use_reranker = True
        self.reranker_top_n = top_n
        return self

    def build(self):
        ensemble_retriever = EnsembleRetriever(
            retrievers=[
                retriever_config.retriever
                for retriever_config in self.retrievers
            ],
            weights=[
                retriever_config.weight for retriever_config in self.retrievers
            ],
        )

        if self.use_reranker:
            compressor = FlashrankRerank(top_n=self.reranker_top_n)
            compression_retriever = ContextualCompressionRetriever(
                base_compressor=compressor,
                base_retriever=ensemble_retriever,
            )
            return compression_retriever

        return ensemble_retriever
