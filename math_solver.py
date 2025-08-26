import sympy as sp

def solve_math(query: str):
    try:
        # Remove unnecessary words
        clean_query = query.lower().replace("calculate", "").replace("what is", "").replace("solve", "").strip()
        
        # Try evaluating
        expr = sp.sympify(clean_query)
        result = expr.evalf()
        return f"The answer is: {result}"
    except Exception:
        return None
