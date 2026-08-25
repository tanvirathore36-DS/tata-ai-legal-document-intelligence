import re


def parse_clauses(text: str) -> list:
    """
    Takes OCR-extracted contract text and separates it into clauses.
    """

    # Pattern for clauses like:
    # 1. PARTIES
    # 2. SCOPE OF SERVICES
    # 10. GOVERNING LAW

    pattern = r'(?m)^\s*(\d+)\.\s+([A-Z][A-Z\s&/-]+)\s*$'

    matches = list(re.finditer(pattern, text))

    clauses = []

    for i, match in enumerate(matches):

        clause_number = int(match.group(1))
        clause_name = match.group(2).strip()

        start = match.end()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        clause_text = text[start:end].strip()

        clauses.append({
            "clause_no": clause_number,
            "clause_name": clause_name,
            "clause_text": clause_text
        })

    return clauses