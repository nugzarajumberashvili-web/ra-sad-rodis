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

GEOGRAPHY_SUB_PROMPT = """
შენ ხარ სანდრო — "რა? სად? როდის?" ინტელექტ-კლუბის გეოგრაფი, კარტოგრაფი და მოგზაური.
შენი მისიაა:
1. გასცე სიღრმისეული, მომხიბვლელი და ენციკლოპედიური პასუხები მსოფლიოსა და საქართველოს გეოგრაფიის ნებისმიერ საკითხზე (კონტინენტები, ოკეანეები, მთათა სისტემები, მდინარეები, ვულკანები, ქვეყნების დედაქალაქები, დროშები, კლიმატური სარტყლები და გეოპოლიტიკური თავისებურებები).
2. იცოდე "რა? სად? როდის?" ტიპის საინტერესო გეოგრაფიული ფაქტები, ანომალიები, ექსკლავები, საზღვრები და კუნძულები.
3. თუ შეკითხვა ქართულადაა, უპასუხე გამართული და დახვეწილი ქართულით; თუ ინგლისურადაა — ინგლისურად.
4. გამოიყენე ლამაზი Markdown ფორმატირება (ცხრილები, პუნქტები, ემოჯები: 🌍, 🧭, 🏔️, 🗺️).
"""

# კლიენტის შექმნა
client = genai.Client(api_key=API_KEY)

# სესიების მართვა
_sessions = {}

def get_or_create_chat(session_id: str = "default"):
    """აბრუნებს ან ქმნის გეოგრაფიის ჩატის სესიას."""
    if session_id not in _sessions:
        try:
            config = types.GenerateContentConfig(
                system_instruction=GEOGRAPHY_SUB_PROMPT,
                temperature=0.5,
            )
            _sessions[session_id] = client.chats.create(
                model=MODEL_NAME,
                config=config
            )
        except Exception:
            _sessions[session_id] = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(system_instruction=GEOGRAPHY_SUB_PROMPT)
            )
    return _sessions[session_id]

def ask(question: str, session_id: str = "default") -> str:
    """
    უსვამს შეკითხვას გეოგრაფს და აბრუნებს პასუხს.
    
    :param question: შეკითხვა გეოგრაფიაზე ან ქვეყნებზე
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
            return "გთხოვთ მოიცადოთ რამდენიმე წამი, გეოგრაფიული რუკების დამუშავების ლიმიტი დროებით ამოიწურა."
        return f"გეოგრაფიის პასუხის მიღება ვერ მოხერხდა: {err_str}"

def reset_session(session_id: str = "default"):
    """ასუფთავებს სესიას."""
    if session_id in _sessions:
        del _sessions[session_id]

# ტესტირების მაგალითი
if __name__ == "__main__":
    kithva = "რომელია მსოფლიოში ყველაზე ღრმა ტბა და რა უნიკალური თვისებები ახასიათებს მას?"
    pasukhi = ask(kithva)
    print("გეოგრაფიის პასუხი:\n", pasukhi)
