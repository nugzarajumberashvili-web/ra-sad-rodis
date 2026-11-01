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

HISTORY_SUB_PROMPT = """
შენ ხარ ნინო — ისტორიკოსი, ცივილიზაციების მემატიანე და კულტურული მემკვიდრეობის ექსპერტი.
შენი მისიაა:
1. გასცე სიღრმისეული, ობიექტური და საინტერესო პასუხები მსოფლიო და საქართველოს ისტორიის ნებისმიერ ეპოქაზე (ანტიკური ცივილიზაციები, შუა საუკუნეები, რენესანსი, ახალი და უახლესი ისტორია).
2. მოვლენები წარმოაჩინო მიზეზ-შედეგობრივ კავშირში და არა მხოლოდ მშრალი თარიღების ჩამონათვალის სახით.
3. მოჰყვე ისტორიული მოვლენები დრამატული, ცოცხალი და მომხიბვლელი თხრობის სტილით.
4. თუ შეკითხვა ქართულადაა, უპასუხე დახვეწილი ქართულით; თუ ინგლისურადაა — ინგლისურად.
5. გამოიყენე ლამაზი Markdown ფორმატირება (ქრონოლოგიური ხაზები, ციტატები, ემოჯები: 🏛️, 📜, ⚔️).
"""

# კლიენტის შექმნა
client = genai.Client(api_key=API_KEY)

# სესიების მართვა
_sessions = {}

def get_or_create_chat(session_id: str = "default"):
    """აბრუნებს ან ქმნის ისტორიის ჩატის სესიას."""
    if session_id not in _sessions:
        try:
            config = types.GenerateContentConfig(
                system_instruction=HISTORY_SUB_PROMPT,
                temperature=0.65,
            )
            _sessions[session_id] = client.chats.create(
                model=MODEL_NAME,
                config=config
            )
        except Exception:
            _sessions[session_id] = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(system_instruction=HISTORY_SUB_PROMPT)
            )
    return _sessions[session_id]

def ask(question: str, session_id: str = "default") -> str:
    """
    უსვამს შეკითხვას ისტორიკოსს და აბრუნებს პასუხს.
    
    :param question: შეკითხვა ისტორიაზე
    :param session_id: სესიის ID
    :return: დეტალური ისტორიული პასუხი
    """
    try:
        chat = get_or_create_chat(session_id)
        response = chat.send_message(question)
        return response.text
    except Exception as e:
        err_str = str(e)
        if "RESOURCE_EXHAUSTED" in err_str:
            return "გთხოვთ მოიცადოთ რამდენიმე წამი, ისტორიული არქივის დამუშავების ლიმიტი დროებით ამოიწურა."
        return f"ისტორიის პასუხის მიღება ვერ მოხერხდა: {err_str}"

def reset_session(session_id: str = "default"):
    """ასუფთავებს სესიას."""
    if session_id in _sessions:
        del _sessions[session_id]

# ტესტირების მაგალითი
if __name__ == "__main__":
    kithva = "რა იყო ოქროს ხანა საქართველოს ისტორიაში და რამ განაპირობა იგი?"
    pasukhi = ask(kithva)
    print("ისტორიის პასუხი:\n", pasukhi)
