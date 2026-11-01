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

SPORT_SUB_PROMPT = """
შენ ხარ დავითი — "რა? სად? როდის?" ინტელექტ-კლუბის სპორტის ექსპერტი და ოლიმპიური მემატიანე.
შენი მისიაა:
1. გასცე ამომწურავი, ზუსტი და შთამაგონებელი პასუხები მსოფლიო და ქართული სპორტის ნებისმიერ დარგზე (ფეხბურთი, კალათბურთი, ოლიმპიური თამაშები, რაგბი, ჭიდაობა, ძიუდო, ჩოგბურთი, ჭადრაკი, ფორმულა 1, მძლეოსნობა).
2. იცოდე ლეგენდარული ისტორიული მატჩები, რეკორდები, სპორტული ინციდენტები, წესების ევოლუცია და უნიკალური სპორტული ვიქტორინის ფაქტები.
3. განსაკუთრებული სიამაყითა და ობიექტურობით ისაუბრო ქართულ სპორტულ წარმატებებზე (დინამო თბილისი 1981, ოლიმპიური ჩემპიონები, ქართველი ძიუდოისტები, მორაგბეები და მოჭადრაკეები).
4. თუ შეკითხვა ქართულადაა, უპასუხე გამართული ქართულით; თუ ინგლისურადაა — ინგლისურად.
5. გამოიყენე ლამაზი Markdown ფორმატირება (ცხრილები, სტატისტიკა, ემოჯები: ⚽, 🏆, 🥇, 🏉, 🥋, ♟️).
"""

# კლიენტის შექმნა
client = genai.Client(api_key=API_KEY)

# სესიების მართვა
_sessions = {}

def get_or_create_chat(session_id: str = "default"):
    """აბრუნებს ან ქმნის სპორტის ჩატის სესიას."""
    if session_id not in _sessions:
        try:
            config = types.GenerateContentConfig(
                system_instruction=SPORT_SUB_PROMPT,
                temperature=0.55,
            )
            _sessions[session_id] = client.chats.create(
                model=MODEL_NAME,
                config=config
            )
        except Exception:
            _sessions[session_id] = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(system_instruction=SPORT_SUB_PROMPT)
            )
    return _sessions[session_id]

def ask(question: str, session_id: str = "default") -> str:
    """
    უსვამს შეკითხვას სპორტის ექსპერტს და აბრუნებს პასუხს.
    
    :param question: შეკითხვა სპორტზე, ჩემპიონატებზე ან ათლეტებზე
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
            return "გთხოვთ მოიცადოთ რამდენიმე წამი, სპორტული მონაცემების დამუშავების ლიმიტი დროებით ამოიწურა."
        return f"სპორტის პასუხის მიღება ვერ მოხერხდა: {err_str}"

def reset_session(session_id: str = "default"):
    """ასუფთავებს სესიას."""
    if session_id in _sessions:
        del _sessions[session_id]

# ტესტირების მაგალითი
if __name__ == "__main__":
    kithva = "რომელ წელს მოიგო თბილისის 'დინამომ' ევროპის თასების მფლობელთა თასი და ვინ გაიტანა გადამწყვეტი გოლები?"
    pasukhi = ask(kithva)
    print("სპორტის პასუხი:\n", pasukhi)
