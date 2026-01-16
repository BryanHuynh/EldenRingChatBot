from langchain_classic.retrievers import (
    ParentDocumentRetriever,
    ContextualCompressionRetriever,
    BM25Retriever,
    EnsembleRetriever,
)
from langchain_core.embeddings import Embeddings
from ..splitters import MDSplitter
from langchain_classic.retrievers.document_compressors import (
    EmbeddingsFilter,
    DocumentCompressorPipeline,
)


class ParentDocumentEnsembledRetriever:
    def __init__(
        self,
        base_retriever: ParentDocumentRetriever,
        embeddings: Embeddings,
    ):
        self.embeddings = embeddings
        docstore = base_retriever.docstore
        doc_ids = list(docstore.yield_keys())
        self.parent_docs = docstore.mget(doc_ids)
        self.base_retriever = base_retriever
        self.ensembled_retriever = None
        self.k_docs = 10

    def add_bm25_retriever(self):
        if len(self.parent_docs) > 0:
            bm25_retriever = BM25Retriever.from_documents(
                self.parent_docs, k=self.k_docs
            )
            ensemble = EnsembleRetriever(
                retrievers=[bm25_retriever, self.base_retriever], weights=[0.5, 0.5]
            )
            self.ensembled_retriever = ensemble
            return self
        else:
            raise ValueError("No parent documents found")

    def build(
        self,
        k: int = 10,
    ) -> ContextualCompressionRetriever:
        splitter = MDSplitter()

        embeddings_filter = EmbeddingsFilter(embeddings=self.embeddings, k=k)

        pipeline = DocumentCompressorPipeline(
            transformers=[splitter, embeddings_filter]
        )

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline,
            base_retriever=self.ensembled_retriever
            if self.ensembled_retriever
            else self.base_retriever,
        )
        return compression_retriever
