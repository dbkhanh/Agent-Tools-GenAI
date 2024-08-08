import numpy as np
from fastembed import TextEmbedding
from data.destinations import *

INPUT = "What is mount Batur?"

ddocuments = []
for i in range(1, 34):
    document = globals()[f"DESTINATION_{i}"]
    ddocuments.append(document)

text_embedding = TextEmbedding()
input_embedded = np.asarray(list(text_embedding.embed([INPUT])))[0]
ddocument_embeddings = []

for doc in ddocuments:
    if 'Place' in doc:
        place_embedded = np.asarray(list(text_embedding.embed([doc['Place']])))[0]
        ddocument_embeddings.append(place_embedded)
    if 'Location' in doc:
        location_embedded = np.asarray(list(text_embedding.embed([doc['Location']])))[0]
        ddocument_embeddings.append(location_embedded)
    # if 'Google Maps Rating' in doc:
    #     mrating_embedded = np.asarray(list(text_embedding.embed([doc['Google Maps Rating']])))[0]
    #     document_embeddings.append(mrating_embedded)
    # if 'Google Reviews (Count)' in doc:
    #     reviews_embedded = np.asarray(list(text_embedding.embed([doc['Google Reviews (Count)']])))[0]
    #     document_embeddings.append(reviews_embedded)
    if 'Description' in doc:
        description_embedded = np.asarray(list(text_embedding.embed([doc['Description']])))[0]
        ddocument_embeddings.append(description_embedded)
    if 'Tourism/Visitor Fee (approx in USD)' in doc:
        tourism_embedded = np.asarray(list(text_embedding.embed([doc['Tourism/Visitor Fee (approx in USD)']])))[0]
        ddocument_embeddings.append(tourism_embedded)
