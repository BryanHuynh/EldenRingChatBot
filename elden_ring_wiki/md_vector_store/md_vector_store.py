import os
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_classic.storage import LocalFileStore
from langchain_classic.storage import create_kv_docstore
from langchain_classic.retrievers import ParentDocumentRetriever
from tqdm import tqdm
from ..splitters.md_splitter import MDSplitter
from ..formatters import FormatBuilder
from ..retrievers import ParentDocumentEnsembledRetriever


class MDVectorStore:
    def __init__(
        self,
        persist_directory: str,
        collection_name: str,
        embedding_function: str = "nomic-embed-text",
        base_url: str = "http://localhost:11434",
        llm_model: str = "llama3.2",
        format_documents: bool = True,
    ):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OllamaEmbeddings(model=embedding_function, base_url=base_url)
        self.llm_model = llm_model
        self.vectorstore = self.get_or_create_vectorstore()
        self.format_documents = format_documents
        self.parent_doc_store_path = os.path.join(persist_directory, "parent_docstore")
        self.parent_doc_store_fs = LocalFileStore(self.parent_doc_store_path)
        self.parent_store = create_kv_docstore(self.parent_doc_store_fs)
        self.parent_retriever = ParentDocumentRetriever(
            vectorstore=self.vectorstore,
            docstore=self.parent_store,
            child_splitter=MDSplitter(),
        )
        self.ensembed_retriever = None

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

    def insert_documents(self, documents: list[Document]):
        if self.vectorstore is None:
            raise ValueError("Vectorstore not initialized")
        pbar = tqdm(documents, desc="Upserting documents")
        for document in pbar:
            tqdm.set_description(
                f"Processing document: {document.metadata['title']: <75}"
            )
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
        del document.metadata["wiki_links"]
        self.parent_retriever.add_documents([document])

    def get_retriever(self):
        if self.ensembed_retriever is None:
            self.ensembed_retriever = (
                ParentDocumentEnsembledRetriever(self.parent_retriever, self.embeddings)
                .add_bm25_retriever()
                .build()
            )
        return self.ensembed_retriever
