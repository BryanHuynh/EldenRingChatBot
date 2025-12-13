from dotenv import load_dotenv
import os

load_dotenv()

claude_model = os.getenv("CLAUDE_MODEL", "")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "")
eldenring_api_host = os.getenv("ELDENRING_API_HOST", "")
log_file_path = os.getenv("LOG_FILE_PATH", None)
wiki_markdown_directory = os.getenv("WIKI_MARKDOWN_DIRECTORY", None)

assert eldenring_api_host, "Error: elden ring api host graphql service is not set. update .env"