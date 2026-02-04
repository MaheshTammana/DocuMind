# Deployment Guide for DocuMind AI

This guide covers deploying DocuMind AI to Streamlit Cloud (free hosting).

## Prerequisites

1. GitHub account
2. Streamlit Cloud account (free at share.streamlit.io)
3. Your Gemini API key

## Step 1: Push to GitHub

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - DocuMind AI"

# Add remote (replace with your GitHub repo URL)
git remote add origin https://github.com/yourusername/documind-ai.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Set main file path: `app.py`
5. Click "Advanced settings"
6. Add secrets in the secrets section:

```toml
GEMINI_API_KEY = "your_actual_api_key_here"
```

7. Click "Deploy!"

## Step 3: Wait for Deployment

Streamlit Cloud will:
- Install dependencies from requirements.txt
- Set up the environment
- Launch your app

This typically takes 2-5 minutes.

## Step 4: Test Your Deployment

1. Upload a sample PDF
2. Ask a question
3. Verify results

## Troubleshooting

### Error: "No module named 'google.generativeai'"

Check requirements.txt includes all dependencies.

### Error: "GEMINI_API_KEY not found"

Verify you added the secret in Streamlit Cloud settings.

### App crashes on large PDFs

Streamlit Cloud has memory limits. Try:
- Using smaller PDFs
- Reducing chunk_size in DocumentProcessor
- Limiting n_results in RAG pipeline

## Alternative Deployment Options

### Local Deployment

```bash
streamlit run app.py
```

Access at: http://localhost:8501

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:

```bash
docker build -t documind-ai .
docker run -p 8501:8501 -e GEMINI_API_KEY=your_key documind-ai
```

### Heroku Deployment

1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

## Security Best Practices

1. Never commit API keys to git
2. Use environment variables for secrets
3. Add rate limiting for production
4. Implement user authentication if needed
5. Monitor API usage to avoid unexpected costs

## Monitoring

Monitor your deployment:
- Check Streamlit Cloud logs
- Monitor Gemini API usage at console.cloud.google.com
- Set up alerts for errors

## Updating Your Deployment

```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```

Streamlit Cloud auto-deploys on push to main branch.

## Support

For issues:
- Check logs in Streamlit Cloud dashboard
- Review error messages in browser console
- Visit Streamlit Community Forum
- Check Gemini API documentation

## Next Steps

After successful deployment:
1. Share your app URL
2. Create demo video
3. Write blog post about your project
4. Add to portfolio
5. Get feedback from users
