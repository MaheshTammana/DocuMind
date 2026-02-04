# DocuMind AI - Project Structure

## 📂 Complete Directory Structure

```
documind-ai/
│
├── 📄 app.py                          # Main Streamlit application
├── 📄 requirements.txt                # Python dependencies
├── 📄 .env.example                    # Environment variables template
├── 📄 .gitignore                      # Git ignore rules
├── 📄 README.md                       # Main documentation
├── 📄 QUICKSTART.md                   # Quick start guide
├── 📄 DEPLOYMENT.md                   # Deployment instructions
├── 📄 LICENSE                         # MIT License
├── 📄 test_system.py                  # System test script
├── 📄 setup.sh                        # Linux/Mac setup script
├── 📄 setup.bat                       # Windows setup script
│
├── 📁 core/                           # Core functionality
│   ├── __init__.py                    # Package initialization
│   ├── gemini_client.py              # Gemini API wrapper
│   ├── embeddings.py                 # Embedding generation
│   ├── vector_store.py               # ChromaDB vector store
│   ├── rag_pipeline.py               # RAG implementation
│   └── document_processor.py         # Document processing pipeline
│
├── 📁 utils/                          # Utility functions
│   ├── __init__.py                    # Package initialization
│   ├── pdf_parser.py                 # PDF text extraction
│   └── chunking.py                   # Text chunking logic
│
├── 📁 data/                           # Data storage (gitignored)
│   ├── uploads/                      # Uploaded PDF files
│   │   └── .gitkeep
│   └── chroma_db/                    # Vector database
│       └── .gitkeep
│
├── 📁 tests/                          # Test files
│   └── (empty - ready for your tests)
│
└── 📁 .streamlit/                     # Streamlit configuration
    └── config.toml                   # UI theme and settings
```

## 📋 File Descriptions

### Root Files

| File | Purpose | Key Features |
|------|---------|--------------|
| `app.py` | Main application | Streamlit UI, tabs for Q&A/Summarize/Compare |
| `requirements.txt` | Dependencies | All Python packages needed |
| `.env.example` | Environment template | API key configuration |
| `README.md` | Documentation | Complete project guide |
| `QUICKSTART.md` | Quick setup | 5-minute setup guide |
| `DEPLOYMENT.md` | Deployment guide | Streamlit Cloud, Docker, Heroku |
| `test_system.py` | Testing script | Verify installation |
| `setup.sh` | Auto setup (Unix) | One-command setup |
| `setup.bat` | Auto setup (Windows) | One-command setup |

### Core Module (`core/`)

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `gemini_client.py` | API communication | `GeminiClient` - text generation with retry |
| `embeddings.py` | Vector generation | `EmbeddingGenerator` - text to vectors |
| `vector_store.py` | Database ops | `VectorStore` - ChromaDB CRUD operations |
| `rag_pipeline.py` | RAG system | `RAGPipeline` - Q&A, summarize, compare |
| `document_processor.py` | Full pipeline | `DocumentProcessor` - PDF to vector DB |

### Utils Module (`utils/`)

| File | Purpose | Key Classes/Functions |
|------|---------|----------------------|
| `pdf_parser.py` | PDF handling | `PDFParser` - extract text and metadata |
| `chunking.py` | Text splitting | `TextChunker` - smart text chunking |

## 🔄 Data Flow

```
1. PDF Upload (app.py)
   ↓
2. PDF Parser (utils/pdf_parser.py)
   ↓
3. Text Chunker (utils/chunking.py)
   ↓
4. Embedding Generator (core/embeddings.py)
   ↓
5. Vector Store (core/vector_store.py)
   ↓
6. RAG Pipeline (core/rag_pipeline.py)
   ↓
7. Gemini Client (core/gemini_client.py)
   ↓
8. Display Results (app.py)
```

## 🎯 Key Components

### 1. Document Processing Pipeline
- **Input**: PDF file
- **Process**: Parse → Chunk → Embed → Store
- **Output**: Chunks in vector database

### 2. RAG Question Answering
- **Input**: User question
- **Process**: Embed → Search → Retrieve → Generate
- **Output**: Answer with sources

### 3. Vector Database
- **Technology**: ChromaDB
- **Storage**: Local persistence
- **Search**: Cosine similarity

### 4. UI Components
- **Framework**: Streamlit
- **Tabs**: Q&A, Summarize, Compare
- **Features**: File upload, chat history, settings

## 📊 Dependencies

### Core Dependencies
- `google-generativeai` - Gemini API
- `chromadb` - Vector database
- `streamlit` - Web interface
- `pypdf2` - PDF parsing
- `python-dotenv` - Environment variables

### Supporting Libraries
- `numpy` - Numerical operations
- `pandas` - Data manipulation

## 🔧 Configuration Files

### `.env`
```
GEMINI_API_KEY=your_key_here
```

### `.streamlit/config.toml`
- Theme colors
- Server settings
- Upload limits

## 📝 Code Statistics

- **Total Python Files**: 11
- **Total Lines of Code**: ~2,500+
- **Core Modules**: 5
- **Utility Modules**: 2
- **Documentation Files**: 6

## 🎨 Design Patterns

1. **Modular Architecture**: Separation of concerns
2. **Single Responsibility**: Each module has one job
3. **Dependency Injection**: Components loosely coupled
4. **Error Handling**: Try-catch throughout
5. **Type Hints**: Better code documentation

## 🚀 Quick Reference Commands

### Setup
```bash
./setup.sh              # Linux/Mac
setup.bat              # Windows
```

### Run
```bash
streamlit run app.py
```

### Test
```bash
python test_system.py
```

### Deploy
```bash
git push origin main    # Auto-deploys to Streamlit Cloud
```

## 💡 Extension Points

Want to extend the project? Here are good starting points:

1. **New Document Types**: Add parsers in `utils/`
2. **Different LLMs**: Modify `core/gemini_client.py`
3. **Advanced Features**: Extend `core/rag_pipeline.py`
4. **UI Improvements**: Enhance `app.py`
5. **Testing**: Add tests in `tests/`

## 📚 Learning Resources

Each file includes:
- Comprehensive docstrings
- Type hints
- Inline comments
- Error handling examples

Perfect for learning:
- RAG systems
- Vector databases
- LLM integration
- Python best practices
- Streamlit development
