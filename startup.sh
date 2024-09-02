#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run src/app.py
