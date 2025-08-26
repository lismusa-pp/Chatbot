"""
smart_engine.py
All-in-one smart chatbot brain with context memory.
Features:
- Math solver
- Rule-based responses
- Wikipedia factual answers (robust, pronoun-aware)
- Transformer AI fallback
"""

import re
import datetime
import random

# ---------------- Wikipedia ----------------
_wikipedia_ok = False
try:
    import wikipedia
    wikipedia.set_lang("en")
    _wikipedia_ok = True
except Exception:
    wikipedia = None

_last_wiki_topic = None  # stores last main topic for pronoun follow-ups

# ---------------- Transformers ----------------
_transformers_ok = False
try:
    from transformers import pipeline, Conversation
    _transformers_ok = True
except Exception:
    pipeline = None
    Conversation = None

_conv_pipe = None
_conversation = None

def _ensure_conversation():
    global _conv_pipe, _conversation
    if not _transformers_ok:
        return False
    if _conv_pipe is None:
        _conv_pipe = pipeline("conversational", model="facebook/blenderbot_small-90M")
    if _conversation is None:
        _conversation = Conversation()
    return True

# ---------------- Rule-based ----------------
def rule_based_response(user_input: str):
    text = user_input.lower()
    if any(g in text for g in ("hello", "hi", "hey")):
        return "Hello! How can I help you today?"
    if "how are you" in text:
        return "I’m just a bot, doing great! How about you?"
    if "your name" in text:
        return "I’m your smart chatbot 🙂"
    if "time" in text:
        now = datetime.datetime.now().strftime("%H:%M")
        return f"The current time is {now}"
    if "date" in text:
        today = datetime.date.today().strftime("%B %d, %Y")
        return f"Today is {today}"
    if "joke" in text:
        jokes = [
            "Why don’t skeletons fight each other? They don’t have the guts!",
            "Why did the computer go to the doctor? Because it caught a virus.",
            "Why do cows wear bells? Because their horns don’t work!"
        ]
        return random.choice(jokes)
    if "bye" in text:
        return "Goodbye!"
    return None

# ---------------- Math solver ----------------
def solve_math(user_input: str):
    pattern = r"([\d\.\s\+\-\*/\^\(\)]+)"
    matches = re.findall(pattern, user_input)
    results = []
    for expr in matches:
        expr = expr.strip()
        if not expr:
            continue
        expr = expr.replace("^", "**")
        try:
            result = eval(expr, {"__builtins__": {}})
            results.append(f"{expr} = {result}")
        except:
            continue
    if results:
        return " | ".join(results)
    return None

# ---------------- Wikipedia handler ----------------
def looks_like_fact_question(text: str) -> bool:
    return bool(re.match(r"^(who|what|when|where|why|how|tell me about|define)", text, re.I))

import wikipedia
import re

_last_wiki_topic = None

def get_wiki_response(user_input: str):
    global _last_wiki_topic

    if not wikipedia:
        return None

    # Clean input
    text = user_input.strip()
    text = re.sub(r"[?!.]", "", text)  # remove punctuation

    # Replace pronouns with last topic
    if _last_wiki_topic:
        text = re.sub(r"\b(he|she|it|they)\b", _last_wiki_topic, text, flags=re.I)

    # Extract main entity from question
    match = re.search(r"(who|what|when|where|tell me about|define)\s+(.+)", text, re.I)
    if match:
        topic_candidate = match.group(2).strip()
    else:
        topic_candidate = text

    # Wikipedia search
    try:
        results = wikipedia.search(topic_candidate, results=1)  # only first result
        if results:
            page_title = results[0]
            summary = wikipedia.summary(page_title, sentences=2)
            _last_wiki_topic = page_title
            return summary
    except Exception as e:
        return f"(Wikipedia failed: {str(e)})"

    return None


# ---------------- Public API ----------------
def smart_reply(user_input: str):
    user_input = user_input.strip()
    if not user_input:
        return "Say something and I’ll do my best 🙂"

    # 1. Math
    math_answer = solve_math(user_input)
    if math_answer:
        return math_answer

    # 2. Rule-based
    rule_answer = rule_based_response(user_input)
    if rule_answer:
        return rule_answer

    # 3. Wikipedia factual questions
    if looks_like_fact_question(user_input):
        wiki_answer = get_wiki_response(user_input)
        if wiki_answer:
            return wiki_answer

    # 4. Transformer fallback
    if _ensure_conversation():
        try:
            _conversation.add_user_input(user_input)
            out = _conv_pipe(_conversation)
            reply = str(out.generated_responses[-1]).strip()
            if reply:
                return reply
        except:
            pass

    return "I’m not sure yet, but I’m learning!"
