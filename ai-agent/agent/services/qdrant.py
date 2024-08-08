from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct
import uuid
from fastembed import TextEmbedding
from typing import List
from ..data.destinations import *
from ..data.documents import *
from dotenv import load_dotenv
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

API_KEY = os.getenv('QDRANT_KEY')
QDRANT_ENDPOINT = os.getenv('QDRANT_ENDPOINT')

class CustomizedQdrant:
    def __init__(
        self,
        endpoint_url: str,
        api_key: str,
        text_embedding_model: TextEmbedding = None,
        local_test: bool = False
    ) -> None:
        self.client = (
            QdrantClient(url=endpoint_url, api_key=api_key)
            if not local_test
            else QdrantClient("localhost", port=6333)
        )
        self.embedding_model = text_embedding_model
        self.vector_size = 384
        self.metric = models.Distance.COSINE

    def init_collection(self, collection_name: str):
        self.client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=self.vector_size, distance=self.metric
            )
        )

    def push_documents(
        self,
        documents: List[dict],
        metadata: List[str] = None,
        collection_name: str = "demo_collection",
    ):
        try:
            self.client.get_collection(collection_name)
        except Exception:
            logger.info(f"** Initialize collection {collection_name} **")
            self.init_collection(collection_name)

        if not metadata:
            metadata = [None for _ in documents]

        texts = [doc.get('Place') or doc.get('Text') for doc in documents] 
        embedded_docs = list(self.embedding_model.embed(texts))
        
        self.client.upsert(
            collection_name=collection_name,
            points=[
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=list(vector),
                    payload={
                        "metadata": meta,
                        "document": doc,
                    },
                )
                for vector, meta, doc in zip(embedded_docs, metadata, documents)
            ]
        )

    def search_documents(
        self,
        query_text: str,
        collection_name: str,
        threshold: float = 0.99
    ):
        try:
            self.client.get_collection(collection_name)
        except Exception:
            return []

        search_result = self.client.search(
            collection_name=collection_name,
            query_vector=list(
                list(self.embedding_model.embed([query_text]))[0]
            )
        )
        return [
            result.model_dump()
            for result in search_result
            if result.model_dump()["score"] >= threshold
        ]

    def get_collection_data(self, collection_name: str):
        try:
            response = self.client.scroll(collection_name=collection_name, with_payload=True)
            points = response[0]  # response[0] contains the points (documents)
            data = [point.payload for point in points]
            return data
        except Exception as e:
            logger.error(f"Error fetching collection data for {collection_name}: {e}", exc_info=True)
            raise

qdrant = CustomizedQdrant(
    endpoint_url=QDRANT_ENDPOINT,
    api_key=API_KEY,
    text_embedding_model=TextEmbedding()
)

documents = [globals()[f"DESTINATION_{i+1}"] for i in range(33)]
metadata = [f"doc{i+1}" for i in range(33)]

# Push documents to destination_collection
qdrant.push_documents(
    documents=documents,
    metadata=metadata,
    collection_name="destination_collection"
)

demo_documents = [globals()[f"DOCUMENT_{i+1}"] for i in range(100)]
demo_metadata = [f"doc{i+1}" for i in range(100)]

# Push documents to demo_collection
qdrant.push_documents(
    documents=demo_documents,
    metadata=demo_metadata,
    collection_name="demo_collection"
)
