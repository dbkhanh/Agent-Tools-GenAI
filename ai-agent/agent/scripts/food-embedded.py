import numpy as np
from fastembed import TextEmbedding
from data.documents import *

INPUT = "How is the dog food?"

documents = []
for i in range(1, 101):
    document = globals()[f"DOCUMENT_{i}"]
    documents.append(document)

text_embedding = TextEmbedding()
input_embedded = np.asarray(list(text_embedding.embed([INPUT])))[0]
document_embeddings = []

for doc in documents:
    if 'ProductId' in doc:
        id_embedded = np.asarray(list(text_embedding.embed([doc['ProductId']])))[0]
        document_embeddings.append(id_embedded)
    if 'ProfileName' in doc:
        profile_embedded = np.asarray(list(text_embedding.embed([doc['ProfileName']])))[0]
        document_embeddings.append(profile_embedded)
    if 'Text' in doc:
        text_embedded = np.asarray(list(text_embedding.embed([doc['Text']])))[0]
        document_embeddings.append(text_embedded)