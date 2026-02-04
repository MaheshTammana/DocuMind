# 🚀 Quick Start Guide

Get DocuMind AI running in 5 minutes!

## Step 1: Install Dependencies (2 min)

```bash
# Clone or download the project
cd documind-ai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configure API Key (1 min)

1. Get your free Gemini API key:
   - Visit: https://makersuite.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key

2. Create `.env` file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Step 3: Test Installation (1 min)

```bash
python test_system.py
```

You should see all tests pass ✅

## Step 4: Run the App (1 min)

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Step 5: Upload and Query

1. **Upload PDFs**: Click "Upload PDFs" in sidebar
2. **Wait**: Processing takes a few seconds
3. **Ask Questions**: Type your question and click "Get Answer"
4. **View Results**: See answers with source citations

## Example Usage

### Good Questions to Ask:
- "What are the main topics discussed?"
- "Summarize the key findings"
- "What methodology was used?"
- "What are the conclusions?"

### Features to Try:
- **Q&A Tab**: Ask questions about your documents
- **Summarize Tab**: Get document summaries
- **Compare Tab**: Compare multiple documents

## Troubleshooting

### "GEMINI_API_KEY not found"
- Make sure `.env` file exists
- Check the key is correct
- Restart the app after adding key

### "No module named..."
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### PDF not processing
- Check PDF is not encrypted
- Try a different PDF
- Check console for error messages

### Slow response
- This is normal for first request
- Subsequent requests are faster
- Using gemini-flash helps with speed

## Next Steps

1. Try different documents
2. Experiment with questions
3. Adjust settings in sidebar
4. Read full README.md for advanced features

## Need Help?

- Check README.md for detailed documentation
- Review DEPLOYMENT.md for hosting options
- Test with provided test_system.py
- Check logs for error messages

## Tips for Best Results

✅ **DO:**
- Upload clear, text-based PDFs
- Ask specific questions
- Use multiple smaller PDFs vs one huge PDF
- Check source citations

❌ **DON'T:**
- Upload scanned images (OCR not included)
- Ask questions about documents you haven't uploaded
- Expect perfect accuracy on complex topics
- Upload extremely large PDFs (>50 pages may be slow)

Happy researching! 📚
