"""
Text Chunking

Splits documents into smaller chunks for processing and embedding.
"""

from typing import List, Dict, Optional
import re


class TextChunker:
    """Split text into overlapping chunks for processing"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize text chunker
        
        Args:
            chunk_size (int): Target size of each chunk in characters
            chunk_overlap (int): Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(
        self, 
        text: str, 
        metadata: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text (str): Text to chunk
            metadata (Dict, optional): Metadata to attach to each chunk
            
        Returns:
            List[Dict]: List of chunk dictionaries with text and metadata
        """
        # Clean text
        text = self._clean_text(text)
        
        # Split into sentences first for better boundaries
        sentences = self._split_into_sentences(text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # Check if adding this sentence exceeds chunk size
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append(current_chunk.strip())
                
                # Start new chunk with overlap from previous chunk
                if len(current_chunk) > self.chunk_overlap:
                    overlap_text = current_chunk[-self.chunk_overlap:]
                else:
                    overlap_text = current_chunk
                
                current_chunk = overlap_text + " " + sentence
            else:
                # Add sentence to current chunk
                current_chunk += " " + sentence
        
        # Add remaining text as final chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Format chunks as list of dictionaries with metadata
        formatted_chunks = []
        for i, chunk in enumerate(chunks):
            chunk_dict = {
                'text': chunk,
                'chunk_id': i,
                'char_count': len(chunk)
            }
            
            # Add metadata if provided
            if metadata:
                chunk_dict.update(metadata)
                
            formatted_chunks.append(chunk_dict)
        
        return formatted_chunks
    
    def _clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text (str): Raw text
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\'\"]', '', text)
        
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Uses simple regex-based sentence splitting.
        
        Args:
            text (str): Text to split
            
        Returns:
            List[str]: List of sentences
        """
        # Split on sentence boundaries (., !, ?)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Filter out empty sentences
        sentences = [s for s in sentences if s.strip()]
        
        return sentences
    
    def chunk_document(self, document_data: Dict) -> List[Dict]:
        """
        Chunk entire document with page information preserved
        
        Args:
            document_data (Dict): Document data from PDF parser containing:
                - filename: Document filename
                - total_pages: Total number of pages
                - pages: List of page dictionaries
            
        Returns:
            List[Dict]: All chunks from document with metadata
        """
        all_chunks = []
        
        for page in document_data['pages']:
            # Skip empty pages
            if not page['text'].strip():
                continue
            
            # Prepare metadata for this page
            page_metadata = {
                'filename': document_data['filename'],
                'page_number': page['page_number'],
                'total_pages': document_data['total_pages']
            }
            
            # Chunk the page text
            chunks = self.chunk_text(page['text'], page_metadata)
            all_chunks.extend(chunks)
        
        return all_chunks
    
    def get_chunk_statistics(self, chunks: List[Dict]) -> Dict:
        """
        Get statistics about chunks
        
        Args:
            chunks (List[Dict]): List of chunk dictionaries
            
        Returns:
            Dict: Statistics including counts, sizes, etc.
        """
        if not chunks:
            return {
                'total_chunks': 0,
                'avg_chunk_size': 0,
                'min_chunk_size': 0,
                'max_chunk_size': 0
            }
        
        chunk_sizes = [chunk['char_count'] for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes)
        }
