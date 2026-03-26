#!/bin/bash
cd "$(dirname "$0")"

echo "Activating virtual environment..."
source backend/venv/bin/activate

echo "Starting MLX Local Inference Server mimicking OpenAI API on port 8080..."
echo "We load the base Qwen2.5-Coder model and the trained adapter."
# If adapter does not exist yet during testing, we just serve the base model as a fallback
if [ -d "backend/training/adapters" ]; then
    python -m mlx_lm.server --model Qwen/Qwen2.5-Coder-1.5B-Instruct --adapter-path backend/training/adapters
else
    echo "Adapter not found. Serving the base model."
    python -m mlx_lm.server --model Qwen/Qwen2.5-Coder-1.5B-Instruct
fi
