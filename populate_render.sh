#!/bin/bash
# Script to populate the database on Render
# This can be run as a one-time job or manually via Render shell

set -e

echo "🦄 Starting database population..."
echo "=================================="

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL is not set!"
    exit 1
fi

# Check if TMDB_URL is set
if [ -z "$TMDB_URL" ]; then
    echo "❌ ERROR: TMDB_URL (TMDb API Key) is not set!"
    exit 1
fi

echo "✓ Environment variables are set"
echo "✓ Running populate_db.py..."
echo ""

python populate_db.py

echo ""
echo "=================================="
echo "✅ Database population complete!"
