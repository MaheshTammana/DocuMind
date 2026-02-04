"""
RAG Pipeline

Implements Retrieval-Augmented Generation for question answering.
"""

from core.gemini_client import GeminiClient
from core.embeddings import EmbeddingGenerator
from core.vector_store import VectorStore
from typing import List, Dict, Optional


class RAGPipeline:
    """Complete RAG (Retrieval-Augmented Generation) pipeline"""
    
    def __init__(self):
        """Initialize RAG pipeline components"""
        self.gemini_client = GeminiClient()
        self.embedding_gen = EmbeddingGenerator()
        self.vector_store = VectorStore()
    
    def answer_question(
        self, 
        question: str, 
        n_results: int = 5,
        temperature: float = 0.7
    ) -> Dict:
        """
        Answer a question using RAG
        
        Args:
            question (str): User's question
            n_results (int): Number of chunks to retrieve
            temperature (float): LLM temperature for generation
            
        Returns:
            Dict: Answer with sources containing:
                - answer: Generated answer text
                - sources: List of source dictionaries
                - retrieved_chunks: Number of chunks retrieved
        """
        print(f"\n🔍 Processing question: {question}")
        
        # Step 1: Generate query embedding
        print("  📊 Generating query embedding...")
        query_embedding = self.embedding_gen.generate_query_embedding(question)
        
        if not query_embedding:
            return {
                'answer': "Sorry, I couldn't process your question. Please try again.",
                'sources': [],
                'retrieved_chunks': 0
            }
        
        # Step 2: Retrieve relevant chunks from vector store
        print(f"  🔎 Retrieving top {n_results} relevant chunks...")
        search_results = self.vector_store.search(query_embedding, n_results)
        
        if not search_results['documents'][0]:
            return {
                'answer': "I couldn't find any relevant information in the uploaded documents. Please upload documents first or try rephrasing your question.",
                'sources': [],
                'retrieved_chunks': 0
            }
        
        # Step 3: Format context from retrieved chunks
        context = self._format_context(search_results)
        
        # Step 4: Generate answer using LLM with context
        print("  🤖 Generating answer...")
        answer = self._generate_answer(question, context, temperature)
        
        # Step 5: Format sources for display
        sources = self._format_sources(search_results)
        
        print("  ✅ Answer generated successfully!")
        
        return {
            'answer': answer,
            'sources': sources,
            'retrieved_chunks': len(search_results['documents'][0])
        }
    
    def _format_context(self, search_results: Dict) -> str:
        """
        Format retrieved chunks into context string for LLM
        
        Args:
            search_results (Dict): Results from vector store search
            
        Returns:
            str: Formatted context string
        """
        context_parts = []
        
        documents = search_results['documents'][0]
        metadatas = search_results['metadatas'][0]
        
        for i, (doc, meta) in enumerate(zip(documents, metadatas), 1):
            context_parts.append(
                f"[Source {i} - {meta['filename']}, Page {meta['page_number']}]\n{doc}\n"
            )
        
        return "\n".join(context_parts)
    
    def _generate_answer(
        self, 
        question: str, 
        context: str,
        temperature: float = 0.7
    ) -> str:
        """
        Generate answer using Gemini with retrieved context
        
        Args:
            question (str): User's question
            context (str): Retrieved context from documents
            temperature (float): Sampling temperature
            
        Returns:
            str: Generated answer
        """
        prompt = f"""You are a helpful AI assistant that answers questions based on provided context from documents.

Context from documents:
{context}

Question: {question}

Instructions:
- Answer the question based ONLY on the information provided in the context above
- If the context doesn't contain enough information to answer fully, say so
- Be concise but thorough in your answer
- When making claims, reference which source number you're using (e.g., "According to Source 1...")
- If information from multiple sources is relevant, synthesize it coherently

Answer:"""
        
        answer = self.gemini_client.generate_with_retry(
            prompt, 
            temperature=temperature,
            max_tokens=2048
        )
        
        return answer if answer else "I apologize, but I encountered an error generating the answer. Please try again."
    
    def _format_sources(self, search_results: Dict) -> List[Dict]:
        """
        Format sources for display in UI
        
        Args:
            search_results (Dict): Results from vector store search
            
        Returns:
            List[Dict]: Formatted source information
        """
        sources = []
        
        documents = search_results['documents'][0]
        metadatas = search_results['metadatas'][0]
        distances = search_results['distances'][0]
        
        for doc, meta, dist in zip(documents, metadatas, distances):
            # Convert distance to similarity score (cosine similarity)
            similarity_score = 1 - dist
            
            sources.append({
                'filename': meta['filename'],
                'page_number': meta['page_number'],
                'text_preview': doc[:300] + "..." if len(doc) > 300 else doc,
                'full_text': doc,
                'relevance_score': round(similarity_score, 3)
            })
        
        return sources
    
    def summarize_document(
        self, 
        filename: str, 
        max_chunks: int = 15
    ) -> str:
        """
        Generate a summary of an entire document
        
        Args:
            filename (str): Name of the document to summarize
            max_chunks (int): Maximum number of chunks to use
            
        Returns:
            str: Document summary
        """
        print(f"\n📄 Summarizing document: {filename}")
        
        # Get chunks for this document
        chunks_data = self.vector_store.get_chunks_by_document(filename)
        
        if not chunks_data['documents']:
            return f"Document '{filename}' not found in the database."
        
        # Combine text from first N chunks to avoid token limits
        documents = chunks_data['documents'][:max_chunks]
        full_text = " ".join(documents)
        
        # Limit text length to avoid exceeding context window
        max_chars = 15000
        if len(full_text) > max_chars:
            full_text = full_text[:max_chars] + "..."
        
        prompt = f"""Please provide a comprehensive summary of this document.

Document: {filename}

Content:
{full_text}

Your summary should include:
- Main topic and purpose of the document
- Key points and findings (3-5 bullet points)
- Important conclusions or takeaways

Summary:"""
        
        summary = self.gemini_client.generate_with_retry(
            prompt,
            temperature=0.3,  # Lower temperature for factual summary
            max_tokens=2048
        )
        
        print("  ✅ Summary generated!")
        
        return summary if summary else "Failed to generate summary."
    
    def compare_documents(
        self, 
        question: str, 
        filenames: List[str],
        n_results_per_doc: int = 3
    ) -> str:
        """
        Compare information across multiple documents
        
        Args:
            question (str): Comparison question or topic
            filenames (List[str]): Documents to compare
            n_results_per_doc (int): Chunks to retrieve per document
            
        Returns:
            str: Comparison analysis
        """
        print(f"\n📊 Comparing documents on: {question}")
        
        # Generate query embedding
        query_embedding = self.embedding_gen.generate_query_embedding(question)
        
        if not query_embedding:
            return "Error generating query embedding."
        
        # Get relevant chunks from each document
        doc_contexts = {}
        
        for filename in filenames:
            print(f"  📄 Retrieving from {filename}...")
            
            # Search within specific document
            results = self.vector_store.search(
                query_embedding,
                n_results=n_results_per_doc,
                where={"filename": filename}
            )
            
            if results['documents'][0]:
                doc_contexts[filename] = "\n".join(results['documents'][0])
        
        if not doc_contexts:
            return "No relevant information found in the specified documents."
        
        # Build comparison prompt
        context_str = ""
        for filename, context in doc_contexts.items():
            context_str += f"\n\n=== {filename} ===\n{context}"
        
        prompt = f"""Compare and analyze the information from these documents regarding: {question}

Documents:
{context_str}

Provide a comparison that:
1. Highlights key similarities between the documents
2. Points out important differences
3. Notes any conflicting information
4. Draws insightful conclusions from the comparison

Comparison:"""
        
        comparison = self.gemini_client.generate_with_retry(
            prompt, 
            temperature=0.3,
            max_tokens=2048
        )
        
        print("  ✅ Comparison complete!")
        
        return comparison if comparison else "Failed to generate comparison."
