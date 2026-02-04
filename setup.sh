#!/bin/bash

# DocuMind AI - Automated Setup Script
# This script sets up the complete environment for DocuMind AI

set -e  # Exit on error

echo "=================================================="
echo "  DocuMind AI - Automated Setup"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo "   ✓ Python $PYTHON_VERSION found"
else
    echo -e "${RED}   ✗ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

# Create virtual environment
echo ""
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✓ Virtual environment created"
else
    echo "   ✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo "   ✓ Virtual environment activated"
else
    echo -e "${RED}   ✗ Failed to activate virtual environment${NC}"
    exit 1
fi

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "   ✓ pip upgraded"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -r requirements.txt
echo "   ✓ All dependencies installed"

# Create .env file if it doesn't exist
echo ""
echo "🔑 Setting up environment variables..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "   ✓ .env file created from template"
        echo ""
        echo -e "${YELLOW}   ⚠️  IMPORTANT: Please edit .env file and add your Gemini API key${NC}"
        echo "   Get your free key at: https://makersuite.google.com/app/apikey"
    else
        echo -e "${RED}   ✗ .env.example not found${NC}"
    fi
else
    echo "   ✓ .env file already exists"
fi

# Create data directories
echo ""
echo "📁 Creating data directories..."
mkdir -p data/uploads data/chroma_db
echo "   ✓ Data directories created"

# Run system tests
echo ""
echo "🧪 Running system tests..."
python test_system.py

# Final instructions
echo ""
echo "=================================================="
echo "  Setup Complete! 🎉"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Edit .env file and add your Gemini API key:"
echo "   nano .env"
echo ""
echo "2. Run the application:"
echo "   streamlit run app.py"
echo ""
echo "3. Open your browser at:"
echo "   http://localhost:8501"
echo ""
echo "For more help, see:"
echo "   - README.md for full documentation"
echo "   - QUICKSTART.md for quick start guide"
echo "   - DEPLOYMENT.md for deployment instructions"
echo ""
echo "=================================================="
