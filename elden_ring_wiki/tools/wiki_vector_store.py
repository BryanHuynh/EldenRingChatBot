from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_classic.retrievers import (
    BM25Retriever,
    EnsembleRetriever,
    ParentDocumentRetriever,
    ContextualCompressionRetriever,
)
from langchain_classic.retrievers.multi_query import MultiQueryRetriever
from langchain_classic.retrievers.document_compressors import LLMChainExtractor
from langchain_classic.storage import LocalFileStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import Optional


class WikiVectorStore:
    def __init__(
        self,
        persist_directory: str,
        collection_name: str,
        embedding_function: str = "nomic-embed-text",
        docstore_directory: Optional[str] = None,
        llm_model: str = "llama3.2",
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OllamaEmbeddings(model=embedding_function)
        self.llm_model = llm_model
        self.docstore_directory = docstore_directory
        self.vectorstore = None
        self._llm = None

    @property
    def llm(self):
        """Lazy load LLM instance"""
        if self._llm is None:
            self._llm = ChatOllama(model=self.llm_model, temperature=0.8)
        return self._llm

    def create_vectorstore(self, documents: list[Document]):
        self.vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        return self

    def load_vectorstore(self):
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
        )
        return self

    def add_documents(self, documents: list[Document]):
        if self.vectorstore is None:
            return self.create_vectorstore(documents)
        return self.vectorstore.add_documents(documents)

    def get_retriever(
        self,
        search_type: str = "similarity",
        filter_dict: Optional[dict] = None,
        **search_kwargs
    ):
        if filter_dict:
            search_kwargs["filter"] = filter_dict
        return self.vectorstore.as_retriever(search_type=search_type, **search_kwargs)

