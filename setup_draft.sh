#!/bin/bash
# FPL Draft Setup Script
# =======================

echo "🏈 FPL Draft Tool Setup"
echo "======================="

# Check if we're in a virtual environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✓ Virtual environment active: $VIRTUAL_ENV"
else
    echo "❌ No virtual environment detected!"
    echo "Please run these commands first:"
    echo "  python3 -m venv fpl_draft_env"
    echo "  source fpl_draft_env/bin/activate"
    echo "  Then run this script again"
    exit 1
fi

echo ""
echo "Installing required packages..."
pip install pandas numpy requests matplotlib seaborn beautifulsoup4 lxml openpyxl

echo ""
echo "Checking API key..."
if [[ -z "$FBRAPI_KEY" ]]; then
    echo "⚠️  FBRAPI_KEY not set!"
    echo "To set your API key, run:"
    echo "  export FBRAPI_KEY='your_api_key_here'"
    echo ""
    echo "You can still use the tool with sample data."
else
    echo "✓ FBRAPI_KEY is set"
fi

echo ""
echo "Creating directory structure..."
mkdir -p draft_data
mkdir -p exports

echo ""
echo "Testing installation..."
python3 -c "
import pandas as pd
import numpy as np
import requests
print('✓ All packages installed successfully!')
print('📊 Pandas version:', pd.__version__)
print('🔢 NumPy version:', np.__version__)
print('🌐 Requests version:', requests.__version__)
"

echo ""
echo "🎯 SETUP COMPLETE!"
echo "=================="
echo ""
echo "Usage Instructions:"
echo "1. Pre-draft: python pre_draft_analysis.py"
echo "2. Live draft: python live_draft_tool.py"
echo ""
echo "Commands for live draft tool:"
echo "  add <player>        - Mark player as taken"
echo "  suggest FW          - Get forward suggestions"  
echo "  suggest MF          - Get midfielder suggestions"
echo "  suggest DF          - Get defender suggestions"
echo "  suggest GK          - Get goalkeeper suggestions"
echo "  compare Salah,Kane  - Compare players"
echo "  strategy           - Get round strategy"
echo "  status             - Show draft status"
echo "  help               - All commands"
echo ""
echo "Good luck with your draft! 🍀"