from fastapi import FastAPI, HTTPException
import logging
from api.models.util import PushDestinationsRequest, PushDocumentsRequest, SearchRequest
from agent.services import qdrant

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/create-collection/{collection_name}")
async def create_collection(collection_name: str):
    try:
        client = qdrant
        client.init_collection(collection_name)
        return {"message": f"Collection '{collection_name}' created successfully."}
    except Exception as e:
        logger.error(f"Error creating collection {collection_name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error creating collection: {str(e)}")

@app.post("/push-documents")
async def push_documents(request: PushDocumentsRequest):
    try:
        qdrant.push_documents(
            documents=[doc.dict() for doc in request.documents],
            metadata=request.metadata,
            collection_name=request.collection_name
        )
        return {"message": f"Documents pushed to collection '{request.collection_name}' successfully."}
    except Exception as e:
        logger.error(f"Error pushing documents to collection {request.collection_name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error pushing documents: {str(e)}")

@app.post("/push-destinations")
async def push_destinations(request: PushDestinationsRequest):
    try:
        qdrant.push_documents(
            documents=[doc.dict() for doc in request.documents],
            metadata=request.metadata,
            collection_name=request.collection_name
        )
        return {"message": f"Destinations pushed to collection '{request.collection_name}' successfully."}
    except Exception as e:
        logger.error(f"Error pushing destinations to collection {request.collection_name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error pushing destinations: {str(e)}")

@app.post("/initialize-push-demo-documents")
async def initialize_push_demo_documents():
    try:
        documents = [globals()[f"DOCUMENT_{i+1}"] for i in range(100)]
        metadata = [f"doc{i+1}" for i in range(100)]
        
        qdrant.push_documents(
            documents=documents,
            metadata=metadata,
            collection_name="demo_collection"
        )
        return {"message": "Predefined documents pushed to 'demo_collection' successfully."}
    except Exception as e:
        logger.error(f"Error pushing predefined documents to demo_collection: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error pushing predefined documents: {str(e)}")

@app.post("/initialize-push-destination-documents")
async def initialize_push_destination_documents():
    try:
        documents = [globals()[f"DESTINATION_{i+1}"] for i in range(33)]
        metadata = [f"doc{i+1}" for i in range(33)]
        
        qdrant.push_documents(
            documents=documents,
            metadata=metadata,
            collection_name="destination_collection"
        )
        return {"message": "Predefined documents pushed to 'destination_collection' successfully."}
    except Exception as e:
        logger.error(f"Error pushing predefined documents to destination_collection: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error pushing predefined documents: {str(e)}")


@app.post("/search-documents")
async def search_documents(request: SearchRequest):
    try:
        client = qdrant
        results = client.search_documents(
            query_text=request.query_text,
            collection_name=request.collection_name,
            threshold=request.threshold
        )
        return results
    except Exception as e:
        logger.error(f"Error searching documents in collection {request.collection_name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")

@app.get("/get-collection-data/{collection_name}")
async def get_collection_data(collection_name: str):
    try:
        client = qdrant
        data = client.get_collection_data(collection_name)
        return data
    except Exception as e:
        logger.error(f"Error getting collection data for {collection_name}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error getting collection data: {str(e)}")
