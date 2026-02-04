"""
PDF Parser

Extracts text and metadata from PDF documents.
"""

import PyPDF2
from typing import List, Dict, Optional
import os


class PDFParser:
    """Parse PDF documents and extract text"""
    
    def extract_text_from_pdf(self, pdf_path: str) -> Optional[Dict]:
        """
        Extract text from PDF file page by page
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            Dict: Document data containing:
                - filename: Name of the PDF file
                - total_pages: Total number of pages
                - pages: List of page dictionaries with page_number and text
            
            None: If parsing fails
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                page_contents = []
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    # Clean up extracted text
                    text = text.strip()
                    
                    page_contents.append({
                        'page_number': page_num + 1,
                        'text': text
                    })
                
                return {
                    'filename': os.path.basename(pdf_path),
                    'total_pages': len(pdf_reader.pages),
                    'pages': page_contents
                }
                
        except FileNotFoundError:
            print(f"Error: File not found: {pdf_path}")
            return None
        except PyPDF2.errors.PdfReadError:
            print(f"Error: Invalid or corrupted PDF: {pdf_path}")
            return None
        except Exception as e:
            print(f"Error parsing PDF {pdf_path}: {e}")
            return None
    
    def get_document_metadata(self, pdf_path: str) -> Dict:
        """
        Extract PDF metadata (author, title, etc.)
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            Dict: Metadata dictionary containing available fields
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                if metadata is None:
                    return {
                        'title': 'Unknown',
                        'author': 'Unknown',
                        'pages': len(pdf_reader.pages)
                    }
                
                return {
                    'title': metadata.get('/Title', 'Unknown'),
                    'author': metadata.get('/Author', 'Unknown'),
                    'subject': metadata.get('/Subject', 'Unknown'),
                    'creator': metadata.get('/Creator', 'Unknown'),
                    'producer': metadata.get('/Producer', 'Unknown'),
                    'pages': len(pdf_reader.pages)
                }
        except Exception as e:
            print(f"Error getting metadata from {pdf_path}: {e}")
            return {}
    
    def validate_pdf(self, pdf_path: str) -> bool:
        """
        Check if a file is a valid PDF
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            bool: True if valid PDF, False otherwise
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # Try to access the first page
                _ = len(pdf_reader.pages)
            return True
        except Exception:
            return False
    
    def get_page_count(self, pdf_path: str) -> int:
        """
        Get the number of pages in a PDF
        
        Args:
            pdf_path (str): Path to PDF file
            
        Returns:
            int: Number of pages, or 0 if error
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        except Exception:
            return 0
    
    def extract_text_from_page(
        self, 
        pdf_path: str, 
        page_number: int
    ) -> Optional[str]:
        """
        Extract text from a specific page
        
        Args:
            pdf_path (str): Path to PDF file
            page_number (int): Page number (1-indexed)
            
        Returns:
            str: Extracted text, or None if error
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if page_number < 1 or page_number > len(pdf_reader.pages):
                    print(f"Error: Page {page_number} out of range")
                    return None
                
                page = pdf_reader.pages[page_number - 1]
                return page.extract_text().strip()
                
        except Exception as e:
            print(f"Error extracting page {page_number}: {e}")
            return None
