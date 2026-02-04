"""
Document Processor

Complete pipeline for processing PDF documents and storing in vector database.
"""

from utils.pdf_parser import PDFParser
from utils.chunking import TextChunker
from core.embeddings import EmbeddingGenerator
from core.vector_store import VectorStore
from typing import Dict, Optional


class DocumentProcessor:
    """Complete pipeline for processing and storing documents"""
    
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 150
    ):
        """
        Initialize document processor with all required components
        
        Args:
            chunk_size (int): Size of text chunks in characters
            chunk_overlap (int): Overlap between chunks
        """
        self.parser = PDFParser()
        self.chunker = TextChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store = VectorStore()
    
    def process_document(self, pdf_path: str) -> Dict:
        """
        Process a PDF document and store in vector database
        
        Complete pipeline:
        1. Parse PDF and extract text
        2. Chunk text into smaller pieces
        3. Generate embeddings for chunks
        4. Store chunks and embeddings in vector database
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            Dict: Processing results containing:
                - success: Boolean indicating success/failure
                - filename: Name of processed document
                - total_pages: Number of pages processed
                - total_chunks: Number of chunks created
                - error: Error message if failed
        """
        print(f"\n📚 Processing document: {pdf_path}")
        print("=" * 50)
        
        # Step 1: Parse PDF
        print("📖 Step 1/4: Parsing PDF...")
        doc_data = self.parser.extract_text_from_pdf(pdf_path)
        
        if not doc_data:
            return {
                'success': False,
                'error': 'Failed to parse PDF. Check if file is valid and not encrypted.'
            }
        
        print(f"   ✓ Extracted text from {doc_data['total_pages']} pages")
        
        # Step 2: Chunk text
        print("✂️  Step 2/4: Chunking text...")
        chunks = self.chunker.chunk_document(doc_data)
        
        if not chunks:
            return {
                'success': False,
                'error': 'No text found in document or chunking failed.'
            }
        
        print(f"   ✓ Created {len(chunks)} chunks")
        
        # Display chunk statistics
        stats = self.chunker.get_chunk_statistics(chunks)
        print(f"   📊 Avg chunk size: {stats['avg_chunk_size']:.0f} chars")
        
        # Step 3: Generate embeddings
        print("🧮 Step 3/4: Generating embeddings...")
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embedding_gen.generate_embeddings_batch(texts)
        
        # Filter out failed embeddings
        valid_chunks = []
        valid_embeddings = []
        
        for chunk, embedding in zip(chunks, embeddings):
            if embedding is not None:
                valid_chunks.append(chunk)
                valid_embeddings.append(embedding)
        
        if not valid_embeddings:
            return {
                'success': False,
                'error': 'Failed to generate embeddings. Check API key and connection.'
            }
        
        print(f"   ✓ Generated {len(valid_embeddings)} embeddings")
        
        if len(valid_embeddings) < len(chunks):
            print(f"   ⚠️  Warning: {len(chunks) - len(valid_embeddings)} embeddings failed")
        
        # Step 4: Store in vector database
        print("💾 Step 4/4: Storing in vector database...")
        try:
            self.vector_store.add_chunks(valid_chunks, valid_embeddings)
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to store in database: {str(e)}'
            }
        
        print("=" * 50)
        print("✅ Processing complete!\n")
        
        return {
            'success': True,
            'filename': doc_data['filename'],
            'total_pages': doc_data['total_pages'],
            'total_chunks': len(valid_chunks),
            'failed_chunks': len(chunks) - len(valid_chunks)
        }
    
    def get_stats(self) -> Dict:
        """
        Get statistics about stored documents
        
        Returns:
            Dict: Database statistics
        """
        return self.vector_store.get_collection_stats()
    
    def delete_document(self, filename: str) -> bool:
        """
        Delete a document from the vector store
        
        Args:
            filename (str): Name of document to delete
            
        Returns:
            bool: True if deleted, False if not found
        """
        count = self.vector_store.delete_document(filename)
        return count > 0
    
    def list_documents(self) -> list:
        """
        List all processed documents
        
        Returns:
            list: List of document filenames
        """
        return self.vector_store.get_all_documents()
    
    def clear_all_documents(self) -> None:
        """
        Clear all documents from the vector store
        
        Warning: This action cannot be undone!
        """
        self.vector_store.clear_all()
        print("✅ All documents cleared from database")
