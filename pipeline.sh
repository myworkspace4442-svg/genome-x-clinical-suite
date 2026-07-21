#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}=============================================${NC}"
echo -e "${GREEN}   GENOME-X PIPELINE AUTOMATOR (LINUX DEV)   ${NC}"
echo -e "${GREEN}=============================================${NC}"

echo "⚙️ [DevOps]: Launching Genome-X Suite via Docker Compose..."
docker compose up -d --build

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ [Success]: Genome-X Engine is now running optimally!${NC}"
    echo "🌍 Access the Interactive UI Dashboard at: http://localhost:8501"
else
    echo "❌ [Error]: Pipeline deployment failed. Check Linux Docker logs."
fi