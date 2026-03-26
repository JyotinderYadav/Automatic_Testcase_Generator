#!/bin/bash
echo "Installing requirements for local MLX training..."
source ../venv/bin/activate
pip install mlx mlx-lm datasets transformers openai

echo "Generating Combined MBPP & HumanEval dataset..."
python generate_combined_dataset.py

echo "Starting MLX LoRA Fine-tuning pipeline..."
echo "This will train the adapter for Qwen2.5-Coder using the finetune.yaml configuration."
python -m mlx_lm.lora --config finetune.yaml

echo "Training complete! Adapter saved to 'adapters' directory."
