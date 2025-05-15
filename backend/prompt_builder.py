def build_prompt(ingredient_name, retrieved_info):
    """Build a prompt for the generative AI model."""
    info_text = "\n".join([
        f"- {r['name']}: {r['category'].capitalize()} ({r['details']}, Regulation: {r['regulation']})"
        for r in retrieved_info
    ])
    return f"""
You are a cosmetic formulation expert with deep knowledge of EU cosmetic regulations and the COSING database.

### Task:
Explain the safety status of the ingredient "{ingredient_name}" based on the following COSING data:
{info_text}

### Instructions:
- Provide a clear, concise explanation (under 100 words).
- Clarify why the ingredient is proibited, restricted, or allowed, referencing restrictions, conditions, product types, or warnings.
- If not found, suggest possible reasons (e.g., INCI name mismatch).
- Example: "Homosalate is allowed as a UV filter in face products at 7.34% max, per COSING (EC) 2009/1223."
"""