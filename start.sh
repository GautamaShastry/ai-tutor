#!/bin/bash

echo "=== Telugu AI Tutor - Quick Start ==="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Start infrastructure
echo "Starting infrastructure services..."
docker-compose up -d

echo "Waiting for services to start..."
sleep 10

# Check services
echo ""
echo "Checking services..."
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Setup database:"
echo "   cd backend && python app/db/migrate.py"
echo ""
echo "2. Ingest data:"
echo "   python -m scripts.ingest_data --source custom --path ./data/sample"
echo "   python -m scripts.ingest_data --source samanantar --path ./data/samanantar"
echo ""
echo "3. Start backend (Terminal 1):"
echo "   cd backend && uvicorn app.main:app --reload"
echo ""
echo "4. Start frontend (Terminal 2):"
echo "   cd frontend && npm run dev"
echo ""
echo "5. Open http://localhost:3000"
echo ""
