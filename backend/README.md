# Tata Legal AI - Backend

Backend service for the Tata Legal AI contract analysis prototype.

The backend accepts a PDF contract, extracts its text, identifies clauses, retrieves relevant legal knowledge from ChromaDB, and uses a Groq LLM to analyze each clause for risk.

---

## 1. Backend Flow

PDF Upload
    ↓
File Validation
    ↓
OCR / Text Extraction
    ↓
Clause Parsing
    ↓
RAG Retrieval
    ↓
ChromaDB
    ↓
Groq LLM
    ↓
Clause Risk Analysis
    ↓
JSON API Response

---

## 2. Main Features

- PDF upload
- PDF text extraction / OCR
- Contract clause parsing
- Legal knowledge retrieval using RAG
- ChromaDB vector database
- Sentence Transformers embeddings
- Groq LLM-based clause analysis
- Risk classification
- Risk explanation
- Recommendations
- Retrieved source references
- API health check
- Swagger API documentation
- Basic API error handling

---

## 3. Project Structure

backend/
│
├── api/
│   └── upload.py
│
├── services/
│   ├── ocr_service.py
│   ├── parser_service.py
│   ├── rag_service.py
│   └── ai_service.py
│
├── models/
│
├── chroma_db/
│
├── main.py
│
├── requirements.txt
├── requirements-full.txt
└── README.md

---

## 4. Services

### ocr_service.py

Responsible for extracting text from uploaded PDF documents.

### parser_service.py

Identifies and structures clauses from the extracted document text.

### rag_service.py

Retrieves relevant legal knowledge from ChromaDB for a given clause or query.

### ai_service.py

Sends the clause and retrieved legal context to the Groq LLM and returns:

- Summary
- Risk level
- Risk reason
- Recommendation

### api/upload.py

Connects the complete pipeline:

PDF → OCR → Parser → RAG → AI → JSON response

### main.py

Creates the FastAPI application and exposes the API routes.

---

## 5. RAG Configuration

Embedding model:

sentence-transformers/all-MiniLM-L6-v2

Embedding dimension:

384

Vector database:

ChromaDB

The current prototype uses a local ChromaDB.

For the final team version, the vector database should be regenerated from the agreed knowledge-base PDFs rather than relying permanently on a copied/generated database.

---

## 6. LLM Configuration

The backend uses Groq through LangChain.

The API key is loaded from a `.env` file.

Required environment variable:

GROQ_API_KEY=your_groq_api_key

Do NOT commit the `.env` file or API key to GitHub.

---

## 7. Installation

Create and activate a virtual environment:

Windows PowerShell:

python -m venv venv

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

---

## 8. Run the Backend

From the backend directory:

uvicorn main:app --reload

The backend will normally run at:

http://127.0.0.1:8000

---

## 9. Swagger Documentation

Open:

http://127.0.0.1:8000/docs

Available APIs include:

GET /

GET /health

POST /upload

---

## 10. Health Check

Endpoint:

GET /health

Expected response:

{
    "status": "ok",
    "service": "Tata Legal AI Backend"
}

---

## 11. Upload Contract

Endpoint:

POST /upload

Upload a PDF contract using Swagger.

The backend will:

1. Validate the file
2. Extract text
3. Parse clauses
4. Retrieve relevant legal knowledge
5. Analyze each clause using the LLM
6. Return structured JSON

---

## 12. Analysis Response

Each analyzed clause contains:

- clause_no
- clause_name
- clause_text
- analysis
- sources

The analysis contains:

- clause_name
- summary
- risk_level
- risk_reason
- recommendation

Sources contain:

- source
- page

---

## 13. Error Handling

The API validates uploaded files.

Examples:

Non-PDF file:

HTTP 400

{
    "detail": "Only PDF files are supported."
}

Empty PDF:

HTTP 400

{
    "detail": "The uploaded PDF is empty."
}

Unable to extract text:

HTTP 422

{
    "detail": "Could not extract text from the PDF."
}

No clauses detected:

HTTP 422

{
    "detail": "No clauses could be identified in the document."
}

Unexpected processing error:

HTTP 500

---

## 14. Environment Variables

Create a `.env` file inside the backend directory:

GROQ_API_KEY=your_groq_api_key

The `.env` file must remain private and should not be committed to Git.

---

## 15. Important Knowledge Base Note

The current prototype knowledge base contains synthetic demonstration/reference material.

It must not be represented as actual confidential Tata material or as an actual Tata-approved legal position.

For the final implementation, use the knowledge base and vector database agreed upon by the project team.

---

## 16. Development Status

Current backend prototype:

- PDF upload: Complete
- OCR/text extraction: Complete
- Clause parsing: Complete
- RAG retrieval: Complete
- ChromaDB integration: Complete
- LLM analysis: Complete
- RAG + LLM integration: Complete
- API error handling: Complete
- Health check: Complete
- Swagger testing: Complete

---

## 17. Team Notes

The backend is designed to provide the frontend with structured clause-level analysis.

The frontend can consume the `/upload` API response and display:

- Contract clauses
- Risk level
- Summary
- Risk reason
- Recommendation
- Source references

The vector database / embedding pipeline should remain coordinated with the team member responsible for the knowledge-base and vector layer.