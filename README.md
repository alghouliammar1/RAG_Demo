# OCR-Powered RAG Demo

A learning project for asking questions about scanned documents and images. The pipeline is split into four stages so each part can be built and tested independently.

## Project Layout

```text
data/
	raw/          Source documents and images (kept out of Git)
		pdfs/       PDF input files (kept out of Git)
	processed/    Extracted text and chunk artifacts (kept out of Git)
	index/        Local vector database files (kept out of Git)
src/ocr_rag/
	ocr.py        OCR and document text extraction
	chunking.py   Text splitting and source metadata
	vector_store.py Embeddings and vector database operations
	rag.py        Retrieval, prompting, and answer generation
tests/          Tests organized around the pipeline stages
```

## Build Roadmap

1. **OCR and extraction:** Read PDFs, scans, and images; emit text with source and page information.
2. **Chunking and metadata:** Split extracted text into manageable pieces while preserving document and page references.
3. **Embeddings and vector storage:** Embed chunks and persist them in a local vector database for semantic search.
4. **RAG query loop:** Retrieve relevant chunks, pass them to an LLM with a grounded prompt, and return an answer with citations.

The corresponding modules are intentionally small placeholders right now. Implement each stage behind its module boundary, then connect the stages in `rag.py`.

## Setup

Requires Python 3.11 or newer. Install only the optional dependencies needed for the stage you are working on:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,ocr,vectors,llm]"
```

OCR also requires the system Tesseract executable for `pytesseract`. Set provider credentials in a local `.env` based on `.env.example`; never commit secrets or private documents.

Run the test suite with `pytest`. Add source documents under `data/raw/`; generated text and indexes belong under `data/processed/` and `data/index/`.