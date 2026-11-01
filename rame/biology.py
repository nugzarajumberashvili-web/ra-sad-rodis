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

BIOLOGY_SUB_PROMPT = """
შენ ხარ ლუკა — ბიოლოგიის, გენეტიკის, ეკოლოგიისა და სიცოცხლის მეცნიერებათა მკვლევარი.
შენი მისიაა:
1. გასცე სიღრმისეული, მომხიბვლელი და მეცნიერულად ზუსტი პასუხები ბიოლოგიის ნებისმიერ საკითხზე (მოლეკულური ბიოლოგია, დნმ, გენეტიკა, უჯრედის აგებულება, ევოლუცია, ეკოსისტემები, ანატომია, ფიზიოლოგია, მიკრობიოლოგია).
2. ახსნა რთული ბიოლოგიური პროცესები ვიზუალური შედარებებითა და ცხოვრებისეული ანალოგიებით.
3. წაახალისო ცნობისმოყვარეობა ცოცხალი სამყაროს საოცრებების მიმართ.
4. თუ შეკითხვა ქართულადაა, უპასუხე მდიდარი და გამართული ქართულით; თუ ინგლისურადაა — ინგლისურად.
5. გამოიყენე ლამაზი Markdown ფორმატირება (სტრუქტურირებული პუნქტები, ცხრილები, ემოჯები: 🧬, 🌿, 🔬).
"""

# კლიენტის შექმნა
client = genai.Client(api_key=API_KEY)

# სესიების მართვა
_sessions = {}

def get_or_create_chat(session_id: str = "default"):
    """აბრუნებს ან ქმნის ბიოლოგიის ჩატის სესიას."""
    if session_id not in _sessions:
        try:
            config = types.GenerateContentConfig(
                system_instruction=BIOLOGY_SUB_PROMPT,
                temperature=0.6,
            )
            _sessions[session_id] = client.chats.create(
                model=MODEL_NAME,
                config=config
            )
        except Exception:
            _sessions[session_id] = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(system_instruction=BIOLOGY_SUB_PROMPT)
            )
    return _sessions[session_id]

def ask(question: str, session_id: str = "default") -> str:
    """
    უსვამს შეკითხვას ბიოლოგს და აბრუნებს პასუხს.
    
    :param question: შეკითხვა ბიოლოგიაზე
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
            return "გთხოვთ მოიცადოთ რამდენიმე წამი, ბიოლოგიური მონაცემების დამუშავების ლიმიტი დროებით ამოიწურა."
        return f"ბიოლოგიის პასუხის მიღება ვერ მოხერხდა: {err_str}"

def reset_session(session_id: str = "default"):
    """ასუფთავებს სესიას."""
    if session_id in _sessions:
        del _sessions[session_id]

# ტესტირების მაგალითი
if __name__ == "__main__":
    kithva = "როგორ მუშაობს CRISPR-Cas9 გენომის რედაქტირება?"
    pasukhi = ask(kithva)
    print("ბიოლოგიის პასუხი:\n", pasukhi)
