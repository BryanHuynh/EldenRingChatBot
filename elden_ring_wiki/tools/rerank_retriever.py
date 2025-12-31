from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank
from langchain_core.retrievers import RetrieverLike

def rerank_retriever(retriever: RetrieverLike, k=5) -> ContextualCompressionRetriever:
    compressor = FlashrankRerank(top_n=k)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=retriever,
    )
    return compression_retriever