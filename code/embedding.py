import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
import os

class GeminiEmbeddingFunction(EmbeddingFunction):
    """
    Custom embedding function using the Gemini AI API for document retrieval.

    This class extends the EmbeddingFunction class and implements the __call__ method
    to generate embeddings for a given set of documents using the Gemini AI API.

    Parameters:
    - input (Documents): A collection of documents to be embedded.

    Returns:
    - Embeddings: Embeddings generated for the input documents.
    """
    def __call__(self, input: Documents) -> Embeddings:
        GEMINI_API_KEY = "AIzaSyDxSeOvPuVfdPhPpKhlkcWJDGuHUzdss8Q"
        
        genai.configure(api_key= GEMINI_API_KEY)
        model = "models/embedding-001"
        title = "Custom query"
        return genai.embed_content(model=model,
                                   content=input,
                                   task_type="retrieval_document",
                                   title=title)["embedding"]