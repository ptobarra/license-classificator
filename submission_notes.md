# Submission Notes — Reviewer Guide

## What to Review First

1. README.md (architecture & approach)
2. /app/services/classifier.py (core logic)
3. /app/llm/ollama_client.py (LLM integration)
4. output/output.xlsx (results)
5. Dockerfile (deployment readiness)

## Key Engineering Highlights

- LLM provider abstraction
- Manual override safety layer
- Output governance & validation
- Scalable inference design

## If I Had More Time

- Add embeddings-based classifier
- Add evaluation metrics dashboard
- Add async batch inference workers
