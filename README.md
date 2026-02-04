# 📚 DocuMind AI

An intelligent document research assistant powered by Google's Gemini API and Retrieval-Augmented Generation (RAG).

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Features

- **📄 Multi-Document Upload**: Process multiple PDF documents simultaneously
- **🤖 AI-Powered Q&A**: Ask natural language questions and get accurate answers
- **📍 Source Citations**: Every answer includes references to specific pages and documents
- **📊 Document Summaries**: Generate comprehensive summaries of entire documents
- **🔍 Semantic Search**: Find relevant information based on meaning, not just keywords
- **💬 Conversation History**: Maintain context across multiple questions
- **⚡ Fast Processing**: Optimized chunking and embedding generation

## 🏗️ Architecture

```
User Question → Embedding → Vector Search → Context Retrieval → LLM → Answer with Sources
```

**Tech Stack:**
- **Frontend**: Streamlit
- **LLM**: Google Gemini 1.5 Flash
- **Vector Database**: ChromaDB
- **Embeddings**: Gemini text-embedding-004
- **PDF Processing**: PyPDF2

## 📋 Prerequisites

- Python 3.8 or higher
- Free Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/documind-ai.git
cd documind-ai
```

### 2. Create virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

## 🚀 Usage

### Run the application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Application

1. **Upload Documents**: Click "Upload PDFs" in the sidebar and select one or more PDF files
2. **Wait for Processing**: The app will extract text, create chunks, and generate embeddings
3. **Ask Questions**: Type your question in the input field
4. **View Results**: Get AI-generated answers with source citations
5. **Explore Sources**: Expand source cards to see exact text and relevance scores

### Example Questions

- "What are the main topics discussed in these documents?"
- "Summarize the key findings from the research paper"
- "What methodology was used in the study?"
- "Compare the approaches mentioned in document A and document B"

## 📁 Project Structure

```
documind-ai/
├── app.py                      # Main Streamlit application
├── core/
│   ├── __init__.py
│   ├── gemini_client.py        # Gemini API wrapper
│   ├── embeddings.py           # Embedding generation
│   ├── vector_store.py         # ChromaDB operations
│   ├── rag_pipeline.py         # RAG implementation
│   └── document_processor.py   # Complete processing pipeline
├── utils/
│   ├── __init__.py
│   ├── pdf_parser.py           # PDF text extraction
│   └── chunking.py             # Text chunking logic
├── data/
│   ├── uploads/                # Uploaded PDFs (gitignored)
│   └── chroma_db/              # Vector database (gitignored)
├── tests/
│   └── test_*.py               # Unit tests
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore
└── README.md
```

## 🧪 Testing

Run individual components:

```bash
# Test Gemini API
python -c "from core.gemini_client import GeminiClient; print(GeminiClient().generate_text('Hello!'))"

# Test PDF parsing
python -c "from utils.pdf_parser import PDFParser; print(PDFParser().extract_text_from_pdf('sample.pdf'))"

# Test embeddings
python -c "from core.embeddings import EmbeddingGenerator; print(len(EmbeddingGenerator().generate_embedding('test')))"
```

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file path: `app.py`
5. Add secrets in Advanced settings:
   ```toml
   GEMINI_API_KEY = "your_api_key_here"
   ```
6. Click Deploy!

### Environment Variables for Production

For Streamlit Cloud, add secrets via the dashboard. For other platforms:

```bash
export GEMINI_API_KEY=your_api_key_here
```

## ⚙️ Configuration

### Chunking Parameters

Edit in `utils/chunking.py`:

```python
chunk_size = 1000      # Characters per chunk
chunk_overlap = 200    # Overlap between chunks
```

### Retrieval Parameters

Edit in `core/rag_pipeline.py`:

```python
n_results = 5          # Number of chunks to retrieve
```

### Model Selection

Edit in `core/gemini_client.py`:

```python
self.model = genai.GenerativeModel('gemini-1.5-flash')  # or 'gemini-1.5-pro'
```

## 📊 API Limits (Free Tier)

- **Requests per minute**: 15 RPM
- **Requests per day**: 1,500 RPD
- **Tokens per minute**: 1M TPM

The app includes automatic retry with exponential backoff to handle rate limits.

## 🐛 Troubleshooting

### API Key Error
- Verify `.env` file exists and contains valid key
- Ensure `python-dotenv` is installed
- Check key has no extra spaces

### Rate Limit Errors
- Wait a few minutes between large batches
- The app automatically retries with backoff
- Consider upgrading to paid tier for higher limits

### PDF Parsing Issues
- Ensure PDFs are not password-protected
- Try different PDFs if one fails
- Check PDF is not corrupted

### ChromaDB Persistence
- Ensure `data/chroma_db/` directory exists
- Check write permissions
- Delete and recreate if corrupted

## 🎯 Roadmap

- [ ] Support for more document formats (DOCX, TXT, HTML)
- [ ] Multi-language support
- [ ] Advanced filtering and sorting
- [ ] Export results to PDF/DOCX
- [ ] User authentication
- [ ] Document versioning
- [ ] Collaborative features

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini API for powerful LLM capabilities
- ChromaDB for efficient vector storage
- Streamlit for the amazing web framework
- The open-source community

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/documind-ai](https://github.com/yourusername/documind-ai)

---

⭐ If you find this project helpful, please consider giving it a star!
