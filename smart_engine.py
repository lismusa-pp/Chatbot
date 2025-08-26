from __future__ import annotations
import re
import math
import ast
import operator as op
from datetime import datetime

# ---------- Optional imports (handled gracefully) ----------
_transformers_ok = False
try:
    from transformers import pipeline, Conversation
    _transformers_ok = True
except Exception:
    Conversation = None
    pipeline = None

_wikipedia_ok = False
try:
    import wikipedia  # pip install wikipedia
    _wikipedia_ok = True
    wikipedia.set_lang("en")
except Exception:
    wikipedia = None

# Try to import your rule-based functions, whatever you named them
_rules_fn = None
try:
    from logic import rule_based_reply as _rules_fn       # our suggested name
except Exception:
    try:
        from logic import rule_based_response as _rules_fn  # your earlier version name
    except Exception:
        _rules_fn = None


# ---------- Safe calculator ----------
_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

def _eval_node(node):
    if isinstance(node, ast.Num):            # Python <=3.7 num; still produced under Constant sometimes
        return node.n
    if isinstance(node, ast.Constant):       # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numbers allowed")
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)
    raise ValueError("Unsupported expression")

def safe_calculate(expr: str) -> float:
    """
    Safely evaluate arithmetic like: 2+3*(4-1)/5**2
    """
    tree = ast.parse(expr, mode="eval")
    return _eval_node(tree.body)


# ---------- Wikipedia lookup ----------
_WHO_WHAT_PATTERN = re.compile(
    r"^\s*(who|what|when|where|why|how|tell me about|define)\b",
    re.IGNORECASE
)

def _looks_like_fact_question(text: str) -> bool:
    if _WHO_WHAT_PATTERN.search(text):
        return True
    # Also consider patterns like "capital of France", "age of X"
    return bool(re.search(r"\b(capital of|age of|founder of|meaning of|definition of)\b", text, re.I))

def wiki_answer(query: str, max_sentences: int = 3) -> str | None:
    if not _wikipedia_ok:
        return None
    try:
        # Try summary directly
        return wikipedia.summary(query, sentences=max_sentences)
    except Exception:
        try:
            # Fallback: search first result, then summary
            hits = wikipedia.search(query)
            if not hits:
                return None
            title = hits[0]
            return wikipedia.summary(title, sentences=max_sentences)
        except Exception:
            return None


# ---------- Small-talk & utility helpers ----------
def small_talk(user_input: str) -> str | None:
    text = user_input.lower()
    if any(g in text for g in ("hello", "hi", "hey")):
        return "Hey! How can I help you today?"
    if "how are you" in text:
        return "I’m doing great—thanks for asking! What’s up?"
    if "your name" in text:
        return "I’m your smart chatbot 🧠"
    if "time" in text:
        return f"It’s {datetime.now().strftime('%H:%M')}."
    if "date" in text:
        return f"Today is {datetime.now().strftime('%B %d, %Y')}."
    if any(x in text for x in ("bye", "goodbye", "see you")):
        return "Goodbye! 👋"
    return None


_CALC_PATTERN = re.compile(r"^\s*(calc(ulate)?\s*:?\s*)?([-+/*%^().\d\s]+)\s*$", re.I)

def maybe_calculate(user_input: str) -> str | None:
    m = _CALC_PATTERN.match(user_input)
    if not m:
        return None
    expr = m.group(3)
    try:
        # swap ^ to ** for power if user used ^ like in math
        expr = expr.replace("^", "**")
        value = safe_calculate(expr)
        # Nice formatting
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        return f"{expr} = {value}"
    except Exception:
        return "I couldn’t compute that. Try something like: 2 + 3*(4-1)/5^2"


# ---------- Conversational AI (lazy init) ----------
_conversation = None
_conv_pipe = None

def _ensure_conversation_pipeline():
    global _conv_pipe, _conversation
    if not _transformers_ok:
        return False
    if _conv_pipe is None:
        # lightweight conversational model; runs on CPU
        _conv_pipe = pipeline("conversational", model="facebook/blenderbot_small-90M")
    if _conversation is None:
        _conversation = Conversation()
    return True


# ---------- Public entry point ----------
def smart_reply(user_input: str) -> str:
    """
    Main brain. Order of tools:
    1) Rule-based & utilities (fast)
    2) Calculator
    3) Wikipedia for facty questions
    4) Conversational model (context-aware)
    5) Final fallback
    """
    user_input = user_input.strip()
    if not user_input:
        return "Say something and I’ll do my best 🙂"

    # 1) Your rule-based quick wins (if you have them)
    if _rules_fn is not None:
        try:
            rb = _rules_fn(user_input)
            if rb:  # only if it returned a non-empty answer
                return rb
        except Exception:
            pass

    # also check our small-talk utility
    st = small_talk(user_input)
    if st:
        return st

    # 2) Math
    calc = maybe_calculate(user_input)
    if calc:
        return calc

    # 3) Wikipedia for fact questions
    if _looks_like_fact_question(user_input):
        wa = wiki_answer(user_input)
        if wa:
            # keep it concise
            wa = wa.strip()
            if len(wa) > 900:
                wa = wa[:900].rsplit(" ", 1)[0] + "…"
            return wa

    # 4) Conversational model w/ memory
    if _ensure_conversation_pipeline():
        try:
            _conversation.add_user_input(user_input)
            out = _conv_pipe(_conversation)
            reply = str(out.generated_responses[-1]).strip()
            if reply:
                return reply
        except Exception:
            pass

    # 5) Final fallback
    return "I’m not sure yet, but I’m learning! Try rephrasing or ask a factual question I can look up."
