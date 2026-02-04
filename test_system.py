#!/usr/bin/env python3
"""
Test Script for DocuMind AI

Quick tests to verify the system is working correctly.
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_api_key():
    """Test if API key is configured"""
    print("🔑 Testing API key configuration...")
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key and api_key != 'your_api_key_here':
        print("   ✅ API key found")
        return True
    else:
        print("   ❌ API key not configured properly")
        print("   Please set GEMINI_API_KEY in .env file")
        return False

def test_gemini_client():
    """Test Gemini API client"""
    print("\n🤖 Testing Gemini API client...")
    try:
        from core.gemini_client import GeminiClient
        client = GeminiClient()
        response = client.generate_text("Say 'Hello!'", max_tokens=10)
        if response:
            print(f"   ✅ API working! Response: {response[:50]}")
            return True
        else:
            print("   ❌ No response from API")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_embeddings():
    """Test embedding generation"""
    print("\n📊 Testing embedding generation...")
    try:
        from core.embeddings import EmbeddingGenerator
        gen = EmbeddingGenerator()
        embedding = gen.generate_embedding("Test text")
        if embedding and len(embedding) > 0:
            print(f"   ✅ Embeddings working! Dimension: {len(embedding)}")
            return True
        else:
            print("   ❌ Failed to generate embedding")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_vector_store():
    """Test vector store"""
    print("\n💾 Testing vector store...")
    try:
        from core.vector_store import VectorStore
        store = VectorStore()
        stats = store.get_collection_stats()
        print(f"   ✅ Vector store initialized")
        print(f"   Documents: {stats['unique_documents']}, Chunks: {stats['total_chunks']}")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_pdf_parser():
    """Test PDF parser"""
    print("\n📄 Testing PDF parser...")
    try:
        from utils.pdf_parser import PDFParser
        parser = PDFParser()
        print("   ✅ PDF parser initialized")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_chunker():
    """Test text chunker"""
    print("\n✂️  Testing text chunker...")
    try:
        from utils.chunking import TextChunker
        chunker = TextChunker()
        test_text = "This is a test. " * 100
        chunks = chunker.chunk_text(test_text)
        print(f"   ✅ Chunker working! Created {len(chunks)} chunks")
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("DocuMind AI - System Tests")
    print("=" * 60)
    
    tests = [
        test_api_key,
        test_gemini_client,
        test_embeddings,
        test_vector_store,
        test_pdf_parser,
        test_chunker
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 60)
    print(f"Results: {sum(results)}/{len(results)} tests passed")
    print("=" * 60)
    
    if all(results):
        print("\n✅ All systems operational! Ready to use DocuMind AI")
        print("\nTo start the app, run: streamlit run app.py")
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
    
    return all(results)

if __name__ == "__main__":
    main()
