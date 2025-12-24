from dotenv import load_dotenv
import os

load_dotenv()

claude_model = os.getenv("CLAUDE_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
eldenring_api_host = os.getenv("ELDENRING_API_HOST", "")
log_file_path = os.getenv("LOG_FILE_PATH", None)
wiki_markdown_directory = os.getenv("WIKI_MARKDOWN_DIRECTORY", None)

wiki_vectorstore_persist_directory = os.getenv("WIKI_VECTORSTORE_PERSIST_DIRECTORY", None)
wiki_vectorstore_collection_name = os.getenv("WIKI_COLLECTION_NAME", None)
wiki_vectorstore_embedding_function = os.getenv("WIKI_EMBEDDING_FUNCTION", None)
wiki_vectorstore_docstore_dir = os.getenv("WIKI_DOCSTORE_DIRECTORY", None)
wiki_llm_model = os.getenv("WIKI_LLM_MODEL", "llama3.2")

assert wiki_markdown_directory, "Error: wiki markdown directory is not set. update .env"
assert wiki_vectorstore_persist_directory, "Error: wiki vectorstore persist directory is not set. update .env"
assert wiki_vectorstore_collection_name, "Error: wiki vectorstore collection name is not set. update .env"
assert wiki_vectorstore_embedding_function, "Error: wiki vectorstore embedding function is not set. update .env"
assert wiki_vectorstore_docstore_dir, "Error: wiki vectorstore docstore directory is not set. update .env"
assert eldenring_api_host, "Error: elden ring api host graphql service is not set. update .env"