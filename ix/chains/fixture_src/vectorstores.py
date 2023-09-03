from langchain.vectorstores import Chroma
from langchain.vectorstores.base import VectorStoreRetriever
from langchain.vectorstores.redis import RedisVectorStoreRetriever

from ix.api.components.types import NodeTypeField
from ix.chains.fixture_src.targets import EMBEDDINGS_TARGET, DOCUMENTS_TARGET


VECTORSTORE_CONNECTORS = [EMBEDDINGS_TARGET, DOCUMENTS_TARGET]

# common fields for the generic retriever
VECTORSTORE_RETRIEVER_FIELDS = [
    {
        "name": "allowed_search_types",
        "type": "list",
        "required": True,
        "default": ["similarity", "similarity_score_threshold", "mmr"],
    }
] + NodeTypeField.get_fields(
    VectorStoreRetriever,
    include=[
        "search_type",
    ],
)


REDIS_VECTORSTORE_CLASS_PATH = "ix.chains.components.vectorstores.AsyncRedisVectorstore"

REDIS_VECTORSTORE_RETRIEVER_FIELDS = (
    VECTORSTORE_RETRIEVER_FIELDS
    + NodeTypeField.get_fields(
        RedisVectorStoreRetriever,
        include=[
            "k",
            "score_threshold",
        ],
    )
)

REDIS_VECTORSTORE = {
    "class_path": REDIS_VECTORSTORE_CLASS_PATH,
    "type": "vectorstore",
    "name": "Redis Vector Store",
    "description": "Redis Vector Store",
    "connectors": VECTORSTORE_CONNECTORS,
    "fields": [
        {
            "name": "redis_url",
            "type": "string",
            "description": "URL of the Redis server",
            "default": "redis://redis:6379/0",
            "style": {"width": "100%"},
        },
        {
            "name": "index_name",
            "type": "string",
            "description": "Name of the index in the Redis",
        },
        {
            "name": "content_key",
            "type": "string",
            "default": "content",
            "description": "Key for storing content",
        },
        {
            "name": "metadata_key",
            "type": "string",
            "default": "metadata",
            "description": "Key for storing metadata",
        },
        {
            "name": "vector_key",
            "type": "string",
            "default": "content_vector",
            "description": "Key for storing vectors",
        },
    ]
    + REDIS_VECTORSTORE_RETRIEVER_FIELDS,
}

CHROMA_CLASS_PATH = "ix.chains.components.vectorstores.AsyncChromaVectorstore"
CHROMA = {
    "class_path": CHROMA_CLASS_PATH,
    "type": "vectorstore",
    "name": "Chroma",
    "description": "Chroma vector database",
    "connectors": VECTORSTORE_CONNECTORS,
    "fields": NodeTypeField.get_fields(
        Chroma,
        include=[
            "collection_name",
            "persist_directory",
            "persist_directory",
        ],
    )
    + VECTORSTORE_RETRIEVER_FIELDS,
}


def get_vectorstore_retriever_fieldnames(class_path: str):
    fields = {REDIS_VECTORSTORE_CLASS_PATH: REDIS_VECTORSTORE_RETRIEVER_FIELDS}.get(
        class_path, VECTORSTORE_RETRIEVER_FIELDS
    )
    return [field["name"] for field in fields]


VECTORSTORES = [REDIS_VECTORSTORE, CHROMA]
__all__ = ["VECTORSTORES"]
