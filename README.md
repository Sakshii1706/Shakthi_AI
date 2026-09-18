# Shakthi AI

Shakthi AI is a multilingual student-assistance application with a Streamlit UI integrated with separate Kannada ASR and RAG components.

## Project Architecture

### Streamlit UI

Location:

C:\Shakthi_AI

The UI provides:
- Student assistant
- Kannada voice input
- Text queries
- RAG responses
- Source display
- Telemetry
- Knowledge manager

### Kannada ASR

Location:

C:\ShakthiAI-ASR

The voice pipeline uses the AI4Bharat IndicConformer Kannada ASR model.

The ASR environment is maintained separately because it has its own NeMo and PyTorch dependency stack.

### RAG Backend

Location:

C:\ShakthiAI

The production RAG pipeline uses:
- SQLite retrieval
- FastEmbed multilingual embeddings
- 384-dimensional embeddings
- Top-k = 2 retrieval
- Gemma 3:4B through Ollama
- Kannada-aware Unicode normalization
- Domain relevance guardrails
- Grounding guardrails

## Voice Query Flow

Microphone
    |
    v
IndicConformer Kannada ASR
    |
    v
Raw Kannada transcription
    |
    v
Conservative ASR normalization
    |
    v
RAGPipeline
    |
    v
SQLite retrieval
    |
    v
Gemma 3:4B via Ollama
    |
    v
Grounded Kannada response

The raw ASR transcription is displayed to the user. Only verified, conservative corrections are applied before the query is sent to RAG.

## Requirements

The Streamlit UI directly requires:

streamlit==1.61.1

Python 3.11 is used for the integrated UI and RAG environment.

The RAG backend and Kannada ASR use separate environments and dependencies.

## External Runtime Requirements

For the complete local application, the following components are required:

- ShakthiAI RAG backend
- ShakthiAI-ASR Kannada ASR environment
- Ollama
- Gemma 3:4B model
- FFmpeg for audio processing

## Configuration

The `.env.example` file documents the environment variables used to locate the separate Kannada ASR environment and script.

Current integration paths are local Windows paths and may need to be changed on another machine.

## Development Principle

Integrate first.

Do not randomly rewrite or replace the separate ASR or RAG backend repositories. Changes from those repositories should be inspected, validated, and integrated deliberately.

## Repository Boundary

This repository contains the Streamlit UI and its integration layer.

The RAG backend and Kannada ASR remain separate project components.
