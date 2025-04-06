#!/bin/bash

echo "🔄 Starting LTL Optimizer Backend..."

# Step 1: Ensure we're in the right place
cd "$(dirname "$0")"

# Step 2: Set up virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  python3 -m venv venv
fi

# Step 3: Activate virtual environment
source venv/bin/activate

# Step 4: Install required packages
echo "📚 Installing dependencies..."
pip install --upgrade pip
pip install 'uvicorn[standard]' fastapi sqlalchemy pydantic pandas scikit-learn

# Step 5: Run the app
echo "🚀 Launching backend on http://localhost:8000 ..."
PYTHONPATH=. uvicorn app.main:app --reload

