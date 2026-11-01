import os
import sys
from google import genai
from google.genai import types

# Fix Windows console encoding for Georgian characters
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Google AI Studio API Key
API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6I7NavMGupKhVNSXKpuLUMukHwq9HnRom1x16GG-tkWxg")
MODEL_NAME = "gemini-3.5-flash-lite"

MATH_SUB_PROMPT = """
შენ ხარ თეა — მათემატიკის, ალგორითმებისა და ანალიტიკის უმაღლესი დონის ექსპერტი.
შენი მისიაა:
1. ამოხსნა ნებისმიერი მათემატიკური ამოცანა (ალგებრა, გეომეტრია, მათემატიკური ანალიზი, დისკრეტული მათემატიკა, ალბათობა, სტატისტიკა).
2. ახსნა ეტაპობრივად (Step-by-Step), მარტივი და ლოგიკური ენით, რათა მომხმარებელმა კარგად გაიგოს პრინციპი.
3. გამოიყენო მკაფიო ფორმულები, სიმბოლოები (მაგ. LaTeX ან სუფთა ტექსტური ფორმულები: x^2, √x, ∫, ∑, π).
4. თუ შეკითხვა შეიცავს ლოგიკურ თავსატეხს ან ალგორითმულ დავალებას, მიუდექი ანალიტიკური სიზუსტით.
5. თუ შეკითხვა ქართულადაა, უპასუხე ქართულად; თუ ინგლისურადაა — ინგლისურად.
6. გამოიყენე ლამაზი Markdown ფორმატირება.
"""

# კლიენტის შექმნა
client = genai.Client(api_key=API_KEY)

# სესიების მართვა
_sessions = {}

def get_or_create_chat(session_id: str = "default"):
    """აბრუნებს ან ქმნის მათემატიკის ჩატის სესიას."""
    if session_id not in _sessions:
        try:
            config = types.GenerateContentConfig(
                system_instruction=MATH_SUB_PROMPT,
                temperature=0.3,  # Lower temperature for math precision
            )
            _sessions[session_id] = client.chats.create(
                model=MODEL_NAME,
                config=config
            )
        except Exception:
            _sessions[session_id] = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(system_instruction=MATH_SUB_PROMPT)
            )
    return _sessions[session_id]

def ask(question: str, session_id: str = "default") -> str:
    """
    უსვამს შეკითხვას მათემატიკის ექსპერტს და აბრუნებს პასუხს.
    
    :param question: მათემატიკური შეკითხვა ან ამოცანა
    :param session_id: სესიის ID
    :return: დეტალური პასუხი
    """
    try:
        chat = get_or_create_chat(session_id)
        response = chat.send_message(question)
        return response.text
    except Exception as e:
        err_str = str(e)
        if "RESOURCE_EXHAUSTED" in err_str:
            return "გთხოვთ მოიცადოთ რამდენიმე წამი, მათემატიკური გამოთვლების ლიმიტი დროებით ამოიწურა."
        return f"მათემატიკის პასუხის მიღება ვერ მოხერხდა: {err_str}"

def reset_session(session_id: str = "default"):
    """ასუფთავებს სესიას."""
    if session_id in _sessions:
        del _sessions[session_id]

# ტესტირების მაგალითი
if __name__ == "__main__":
    kithva = "რა არის ეილერის ფორმულა e^(i*pi) + 1 = 0 და რატომ ითვლება ის ულამაზეს ფორმულად?"
    pasukhi = ask(kithva)
    print("მათემატიკის პასუხი:\n", pasukhi)
