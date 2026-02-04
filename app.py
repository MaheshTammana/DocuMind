"""
DocuMind AI - Streamlit Application

Main application file for the intelligent document research assistant.
"""

import streamlit as st
from core.document_processor import DocumentProcessor
from core.rag_pipeline import RAGPipeline
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .source-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processor' not in st.session_state:
    st.session_state.processor = DocumentProcessor()
    st.session_state.rag = RAGPipeline()
    st.session_state.chat_history = []
    st.session_state.processing_complete = False

# Sidebar
with st.sidebar:
    st.markdown("# 📚 DocuMind AI")
    st.markdown("*Intelligent Document Research Assistant*")
    st.markdown("---")
    
    # File upload section
    st.markdown("### 📄 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF documents to analyze"
    )
    
    if uploaded_files:
        # Create uploads directory if it doesn't exist
        os.makedirs("./data/uploads", exist_ok=True)
        
        for uploaded_file in uploaded_files:
            file_path = f"./data/uploads/{uploaded_file.name}"
            
            # Check if file already processed
            existing_docs = st.session_state.processor.list_documents()
            
            if uploaded_file.name in existing_docs:
                st.info(f"📄 {uploaded_file.name} already processed")
                continue
            
            # Save file
            with open(file_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Process document
            with st.spinner(f"Processing {uploaded_file.name}..."):
                result = st.session_state.processor.process_document(file_path)
            
            if result['success']:
                st.success(f"✅ {uploaded_file.name}")
                st.caption(f"Pages: {result['total_pages']} | Chunks: {result['total_chunks']}")
                st.session_state.processing_complete = True
            else:
                st.error(f"❌ {uploaded_file.name}")
                st.caption(f"Error: {result.get('error', 'Unknown error')}")
    
    st.markdown("---")
    
    # Database statistics
    st.markdown("### 📊 Database Stats")
    stats = st.session_state.processor.get_stats()
    
    st.markdown(f"""
    <div class="stat-box">
        <b>Documents:</b> {stats['unique_documents']}<br>
        <b>Total Chunks:</b> {stats['total_chunks']}
    </div>
    """, unsafe_allow_html=True)
    
    if stats['documents']:
        with st.expander("📚 View Documents"):
            for doc in stats['documents']:
                st.text(f"• {doc}")
    
    st.markdown("---")
    
    # Settings
    st.markdown("### ⚙️ Settings")
    
    retrieval_count = st.slider(
        "Chunks to retrieve",
        min_value=3,
        max_value=10,
        value=5,
        help="Number of relevant chunks to retrieve for each question"
    )
    
    temperature = st.slider(
        "Response creativity",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher values make responses more creative, lower values more focused"
    )
    
    st.markdown("---")
    
    # Clear database
    if st.button("🗑️ Clear All Documents", type="secondary"):
        if st.session_state.processor.get_stats()['total_chunks'] > 0:
            st.session_state.processor.clear_all_documents()
            st.session_state.chat_history = []
            st.success("Database cleared!")
            st.rerun()

# Main content area
st.markdown('<div class="main-header">📚 DocuMind AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Ask questions about your documents</div>', unsafe_allow_html=True)

# Check if documents are uploaded
if stats['total_chunks'] == 0:
    st.info("👈 Please upload PDF documents using the sidebar to get started!")
    st.markdown("""
    ### How to use DocuMind AI:
    
    1. **Upload Documents**: Click on the file uploader in the sidebar and select your PDF files
    2. **Wait for Processing**: The system will extract text, create chunks, and generate embeddings
    3. **Ask Questions**: Type your questions in the input box below
    4. **Get Answers**: Receive AI-powered answers with source citations
    
    ### Example Questions:
    - "What are the main topics discussed in these documents?"
    - "Summarize the key findings"
    - "What methodology was used?"
    - "Compare the approaches in different documents"
    """)
else:
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs(["💬 Q&A", "📝 Summarize", "🔍 Compare"])
    
    # Tab 1: Q&A
    with tab1:
        st.markdown("### Ask a Question")
        
        # Question input
        question = st.text_input(
            "Enter your question:",
            placeholder="What are the main findings in the research paper?",
            key="question_input"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            ask_button = st.button("🔍 Get Answer", type="primary", use_container_width=True)
        with col2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        if ask_button and question:
            with st.spinner("🤔 Thinking..."):
                result = st.session_state.rag.answer_question(
                    question,
                    n_results=retrieval_count,
                    temperature=temperature
                )
            
            # Add to chat history
            st.session_state.chat_history.append({
                'question': question,
                'answer': result['answer'],
                'sources': result['sources'],
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 💬 Conversation")
            
            for i, chat in enumerate(reversed(st.session_state.chat_history)):
                with st.container():
                    st.markdown(f"**🙋 Question ({chat['timestamp']}):**")
                    st.markdown(chat['question'])
                    
                    st.markdown("**🤖 Answer:**")
                    st.markdown(chat['answer'])
                    
                    # Show sources
                    if chat['sources']:
                        st.markdown("**📚 Sources:**")
                        for j, source in enumerate(chat['sources'], 1):
                            with st.expander(
                                f"Source {j}: {source['filename']} (Page {source['page_number']}) - Relevance: {source['relevance_score']}"
                            ):
                                st.markdown(f"**Text Preview:**")
                                st.text(source['text_preview'])
                    
                    st.markdown("---")
    
    # Tab 2: Summarize
    with tab2:
        st.markdown("### 📝 Document Summary")
        st.markdown("Generate a comprehensive summary of a document")
        
        # Select document to summarize
        available_docs = st.session_state.processor.list_documents()
        selected_doc = st.selectbox(
            "Select document to summarize:",
            available_docs
        )
        
        if st.button("📝 Generate Summary", type="primary"):
            with st.spinner(f"Generating summary for {selected_doc}..."):
                summary = st.session_state.rag.summarize_document(selected_doc)
            
            st.markdown("### Summary")
            st.markdown(summary)
            
            # Download button
            st.download_button(
                label="📥 Download Summary",
                data=summary,
                file_name=f"{selected_doc}_summary.txt",
                mime="text/plain"
            )
    
    # Tab 3: Compare
    with tab3:
        st.markdown("### 🔍 Compare Documents")
        st.markdown("Compare information across multiple documents")
        
        # Select documents to compare
        available_docs = st.session_state.processor.list_documents()
        
        if len(available_docs) < 2:
            st.warning("Please upload at least 2 documents to use comparison feature")
        else:
            selected_docs = st.multiselect(
                "Select documents to compare:",
                available_docs,
                default=available_docs[:2] if len(available_docs) >= 2 else available_docs
            )
            
            comparison_question = st.text_input(
                "What would you like to compare?",
                placeholder="Compare the methodologies used in these papers",
                key="comparison_input"
            )
            
            if st.button("🔍 Compare", type="primary") and comparison_question and len(selected_docs) >= 2:
                with st.spinner("Analyzing documents..."):
                    comparison = st.session_state.rag.compare_documents(
                        comparison_question,
                        selected_docs
                    )
                
                st.markdown("### Comparison Results")
                st.markdown(comparison)
                
                # Download button
                st.download_button(
                    label="📥 Download Comparison",
                    data=comparison,
                    file_name="document_comparison.txt",
                    mime="text/plain"
                )

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    Made with ❤️ using Google Gemini API | 
    <a href="https://github.com/yourusername/documind-ai" target="_blank">GitHub</a>
</div>
""", unsafe_allow_html=True)
