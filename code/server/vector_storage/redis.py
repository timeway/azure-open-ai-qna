import logging
import os
from typing import Any, Callable

from dotenv import load_dotenv
from langchain.vectorstores.redis import Redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

load_dotenv()

logger = logging.getLogger()


class RedisExtended(Redis):

    def __init__(self, redis_url: str = None, index_name: str = None, embedding_function: Callable = None, **kwargs: Any):

        self.redis_url = f"redis://:{os.getenv('REDIS_PASSWORD')}@{os.getenv('REDIS_ADDRESS')}:{os.getenv('REDIS_PORT')}" if redis_url is None else redis_url
        self.index_name = "embeddings" if index_name is None else index_name

        super().__init__(self.redis_url, self.index_name, embedding_function)

        try:
            self.client.ft(self.index_name).info()
        except:
            # Create Redis Index
            self.create_index()

    def create_index(self, prefix="doc", distance_metric: str = "COSINE"):
        content = TextField(name="content")
        metadata = TextField(name="metadata")
        content_vector = VectorField(
            "content_vector",
            "HNSW", {
                "TYPE": "FLOAT32",
                "DIM": 1536,
                "DISTANCE_METRIC": distance_metric,
                "INITIAL_CAP": 1000,
            }
        )
        # Create index
        self.client.ft(self.index_name).create_index(
            fields=[content, metadata, content_vector],
            definition=IndexDefinition(prefix=[prefix], index_type=IndexType.HASH)
        )

    def delete_keys_pattern(self, pattern: str = "*") -> None:
        keys = self.client.keys(pattern)
        for key in keys:
            self.client.delete(key)

    def delete_all(self):
        self.client.flushall()
