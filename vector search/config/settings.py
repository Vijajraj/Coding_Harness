# Chunking
CHUNK_SIZE = 500          # slightly smaller → better grounding
CHUNK_OVERLAP = 80        # enough continuity, less redundancy

# Embeddings
EMBEDDING_MODEL = "BAAI/bge-large-en"
TOP_K = 6                 # GLM benefits from slightly broader context

# Vector store
VECTOR_DB_PATH = "./vectordb/index.faiss"

# LLM (AirLLM)
LLM_MODEL = "THUDM/glm-4.5-air"
MAX_TOKENS = 256          # GLM is concise; higher adds noise
