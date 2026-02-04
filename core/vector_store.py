"""
Vector Store

Manages vector storage and similarity search using ChromaDB.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os


class VectorStore:
    """Manage vector storage with ChromaDB"""
    
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        """
        Initialize ChromaDB client with persistence
        
        Args:
            persist_directory (str): Directory to persist the vector database
        """
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}  # Use cosine similarity
        )
    
    def add_chunks(
        self, 
        chunks: List[Dict], 
        embeddings: List[List[float]]
    ) -> None:
        """
        Add document chunks with embeddings to vector store
        
        Args:
            chunks (List[Dict]): List of chunk dictionaries containing:
                - text: The chunk text
                - filename: Source document filename
                - page_number: Page number in source document
                - chunk_id: Unique identifier within document
            embeddings (List[List[float]]): Corresponding embedding vectors
        """
        if len(chunks) != len(embeddings):
            raise ValueError(
                f"Mismatch: {len(chunks)} chunks but {len(embeddings)} embeddings"
            )
        
        # Generate unique IDs
        ids = [
            f"{chunk['filename']}_{chunk['page_number']}_{chunk['chunk_id']}" 
            for chunk in chunks
        ]
        
        # Extract documents (text content)
        documents = [chunk['text'] for chunk in chunks]
        
        # Prepare metadata (exclude 'text' to avoid duplication)
        metadatas = [{
            'filename': chunk['filename'],
            'page_number': chunk['page_number'],
            'chunk_id': chunk['chunk_id'],
            'char_count': chunk.get('char_count', 0)
        } for chunk in chunks]
        
        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        
        print(f"✓ Added {len(chunks)} chunks to vector store")
    
    def search(
        self, 
        query_embedding: List[float], 
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:
        """
        Search for similar chunks using vector similarity
        
        Args:
            query_embedding (List[float]): Query embedding vector
            n_results (int): Number of results to return
            where (Dict, optional): Metadata filter (e.g., {'filename': 'doc.pdf'})
            
        Returns:
            Dict: Search results containing:
                - documents: List of matching text chunks
                - metadatas: List of metadata dicts
                - distances: List of similarity distances
                - ids: List of chunk IDs
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )
        
        return results
    
    def delete_document(self, filename: str) -> int:
        """
        Delete all chunks from a specific document
        
        Args:
            filename (str): Name of document to delete
            
        Returns:
            int: Number of chunks deleted
        """
        # Get all IDs for this document
        results = self.collection.get(
            where={"filename": filename}
        )
        
        if results['ids']:
            self.collection.delete(ids=results['ids'])
            count = len(results['ids'])
            print(f"✓ Deleted {count} chunks from {filename}")
            return count
        
        return 0
    
    def get_all_documents(self) -> List[str]:
        """
        Get list of all unique document filenames in the store
        
        Returns:
            List[str]: List of document filenames
        """
        all_data = self.collection.get()
        
        if not all_data['metadatas']:
            return []
        
        # Extract unique filenames
        filenames = set(meta['filename'] for meta in all_data['metadatas'])
        return sorted(list(filenames))
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the vector store
        
        Returns:
            Dict: Statistics including:
                - total_chunks: Total number of chunks stored
                - unique_documents: Number of unique documents
                - documents: List of document filenames
        """
        count = self.collection.count()
        documents = self.get_all_documents()
        
        return {
            'total_chunks': count,
            'unique_documents': len(documents),
            'documents': documents
        }
    
    def clear_all(self) -> None:
        """
        Clear all data from the vector store
        
        Warning: This action cannot be undone!
        """
        # Delete the collection
        self.client.delete_collection(name="documents")
        
        # Recreate empty collection
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        print("✓ Vector store cleared")
    
    def get_chunks_by_document(self, filename: str) -> Dict:
        """
        Get all chunks for a specific document
        
        Args:
            filename (str): Document filename
            
        Returns:
            Dict: Chunks data including documents, metadatas, and ids
        """
        results = self.collection.get(
            where={"filename": filename}
        )
        
        return results
