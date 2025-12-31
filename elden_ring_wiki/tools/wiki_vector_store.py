import json
import os
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_classic.retrievers import (
    BM25Retriever,
    EnsembleRetriever,
    ParentDocumentRetriever,
    ContextualCompressionRetriever,
)
import chromadb
from chromadb.config import Settings
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
        base_url: str = "http://localhost:11434",
        docstore_directory: Optional[str] = None,
        llm_model: str = "llama3.2",
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OllamaEmbeddings(
            model=embedding_function, base_url= base_url
        )
        self.llm_model = llm_model
        self.docstore_directory = docstore_directory
        self.vectorstore = self.get_or_create_vectorstore()
        self._llm = None

    @property
    def llm(self):
        """Lazy load LLM instance"""
        if self._llm is None:
            self._llm = ChatOllama(model=self.llm_model, temperature=0.8)
        return self._llm

    def get_or_create_vectorstore(self):
        if os.path.exists(self.persist_directory):
            print(f"Loading existing vectorstore: {self.collection_name}")
            vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
        else:
            print(f"Creating new vectorstore: {self.collection_name}")
            vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory
            )
        self.vectorstore = vectorstore
        
        return self.vectorstore
    
    def get_existing_document_metadata(self) -> set[str]:
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized")
        collection = self.vectorstore._collection
        all_data = collection.get(include=['metadatas'])
        meta_datas = all_data['metadatas']
        meta_data_set = set([json.dumps(metadata, sort_keys=True) for metadata in meta_datas])
        return meta_data_set


    def upsert_documents(self, documents: list[Document]):
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized")
        existing_documents = self.get_existing_document_metadata()
        for document in documents:
            if json.dumps(document.metadata, sort_keys=True) not in existing_documents:
                self.vectorstore.add_documents([document])
                print(f"✓ Added document: {document.metadata['title']}")
            else:
                print(f"✗ Document already exists: {document.metadata['title']}")
        
        

    def get_retriever(
        self,
        search_type: str = "similarity",
        filter_dict: Optional[dict] = None,
        **search_kwargs,
    ):
        if filter_dict:
            search_kwargs["filter"] = filter_dict
        return self.vectorstore.as_retriever(search_type=search_type, **search_kwargs)
