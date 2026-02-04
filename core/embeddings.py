"""
Embedding Generation

Generates vector embeddings for text using Gemini's embedding model.
"""

import google.generativeai as genai
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class EmbeddingGenerator:
    """Generate embeddings using Gemini API"""
    
    def __init__(self, model_name: str = "models/text-embedding-004"):
        """
        Initialize embedding generator
        
        Args:
            model_name (str): Name of the embedding model to use
        """
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        self.model_name = model_name
        
    def generate_embedding(self, text: str) -> Optional[List[float]]:
        """
        Generate embedding for a single text
        
        Args:
            text (str): Text to embed
            
        Returns:
            List[float]: Embedding vector, or None if error occurs
        """
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=text,
                task_type="retrieval_document"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def generate_embeddings_batch(
        self, 
        texts: List[str]
    ) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts
        
        Processes each text individually to handle errors gracefully.
        
        Args:
            texts (List[str]): List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors (None for failed items)
        """
        embeddings = []
        
        for i, text in enumerate(texts):
            if i % 10 == 0:
                print(f"Generating embeddings: {i}/{len(texts)}")
            
            embedding = self.generate_embedding(text)
            embeddings.append(embedding)
        
        print(f"Generated {len(embeddings)} embeddings")
        return embeddings
    
    def generate_query_embedding(self, query: str) -> Optional[List[float]]:
        """
        Generate embedding for a search query
        
        Uses 'retrieval_query' task type for optimized search performance.
        
        Args:
            query (str): Search query text
            
        Returns:
            List[float]: Query embedding vector, or None if error occurs
        """
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return None
    
    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of embeddings produced by this model
        
        Returns:
            int: Embedding dimension (768 for text-embedding-004)
        """
        # Generate a test embedding to determine dimension
        test_embedding = self.generate_embedding("test")
        return len(test_embedding) if test_embedding else 768
