#!/usr/bin/env zsh

# Obter os caminhos absolutos para os diretórios do backend e frontend
BASE_PATH=$(cd "$(dirname "$0")/.." && pwd)
BACKEND_PATH="$BASE_PATH/backend"
FRONTEND_PATH="$BASE_PATH/frontend"

echo "Abrindo terminal para o backend (FastAPI)..."
osascript <<EOF
tell application "Terminal"
    do script "cd '$BACKEND_PATH' && set -a && [ -f .env ] && source .env && set +a && poetry run uvicorn src.provaia.main:app --reload"
end tell
EOF

echo "Abrindo terminal para o frontend (Vue + Vite)..."
osascript <<EOF
tell application "Terminal"
    do script "cd '$FRONTEND_PATH' && npm run dev"
end tell
EOF