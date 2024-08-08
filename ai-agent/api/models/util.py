from pydantic import BaseModel
from typing import List

class Document(BaseModel):
    id: str
    Text: str

class Destination(BaseModel):
    id: str
    Place: str

class PushDocumentsRequest(BaseModel):
    documents: List[Document]
    metadata: List[str]
    collection_name: str

class PushDestinationsRequest(BaseModel):
    documents: List[Destination]
    metadata: List[str]
    collection_name: str

class SearchRequest(BaseModel):
    query_text: str
    collection_name: str
    threshold: float