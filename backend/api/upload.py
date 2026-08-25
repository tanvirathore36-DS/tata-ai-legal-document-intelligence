from fastapi import APIRouter, UploadFile, File, HTTPException

from services.ocr_service import extract_text_from_pdf
from services.parser_service import parse_clauses
from services.rag_service import retrieve_relevant_knowledge
from services.ai_service import analyze_clause


router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    # ---------------------------------------------------------
    # Step 1: Validate uploaded file
    # ---------------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file was provided."
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )


    try:

        # -----------------------------------------------------
        # Step 2: Read uploaded PDF
        # -----------------------------------------------------

        pdf_bytes = await file.read()

        if not pdf_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty."
            )


        # -----------------------------------------------------
        # Step 3: OCR
        # -----------------------------------------------------

        extracted_text = extract_text_from_pdf(pdf_bytes)

        if not extracted_text or not extracted_text.strip():
            raise HTTPException(
                status_code=422,
                detail="Could not extract text from the PDF."
            )


        # -----------------------------------------------------
        # Step 4: Parse clauses
        # -----------------------------------------------------

        clauses = parse_clauses(extracted_text)

        if not clauses:
            raise HTTPException(
                status_code=422,
                detail="No clauses could be identified in the document."
            )


        # -----------------------------------------------------
        # Step 5: RAG + AI analysis
        # -----------------------------------------------------

        analyzed_clauses = []

        for clause in clauses:

            clause_name = clause.get("clause_name", "")
            clause_text = clause.get("clause_text", "")

            # Retrieve relevant legal knowledge
            retrieved_knowledge = retrieve_relevant_knowledge(
                clause_text
            )

            # Convert retrieved knowledge into LLM context
            context = "\n\n".join(
                item.get("content", "")
                for item in retrieved_knowledge
            )

            # Analyze clause using Groq + RAG context
            analysis = analyze_clause(
                clause_name,
                clause_text,
                context
            )

            # Keep only source information for the frontend
            sources = []

            for item in retrieved_knowledge:

                sources.append({
                    "source": item.get("source"),
                    "page": item.get("page")
                })

            # Combine original clause + analysis + sources
            analyzed_clause = {
                **clause,
                "analysis": analysis,
                "sources": sources
            }

            analyzed_clauses.append(analyzed_clause)


        # -----------------------------------------------------
        # Step 6: Return final response
        # -----------------------------------------------------

        return {
            "filename": file.filename,
            "message": "File uploaded and processed successfully",
            "extracted_text": extracted_text,
            "clauses": analyzed_clauses
        }


    except HTTPException:
        # Re-raise our intentional HTTP errors
        raise


    except Exception as e:
        # Handle unexpected backend errors
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the document: {str(e)}"
        )