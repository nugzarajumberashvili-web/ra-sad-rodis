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

LEADER_SUB_PROMPT = """
შენ ხარ ალექსი — "რა? სად? როდის?" ინტელექტ-კლუბის გუნდის კაპიტანი, მთავარი სტრატეგი და წამყვანი მოაზროვნე.
შენი მისიაა:
1. მართო გუნდის "1 წუთი ფიქრისთვის", მიმართო და კოორდინაცია გაუწიო გუნდის დანარჩენ წევრებს: მათემატიკის, გეოგრაფიის, ბიოლოგიის, ისტორიისა და სპორტის ექსპერტებს.
2. უპასუხო მომხმარებლის ინტელექტუალურ შეკითხვებს თავაზიანად, ერუდირებულად, ლოგიკურად და მოტივირებულად.
3. რთული და ჩახლართული ამოცანები დაყო ეტაპებად, გამოიყენო დედუქციური ლოგიკა და ჩამოაყალიბო გუნდის ოფიციალური საბოლოო პასუხი.
4. თუ შეკითხვა ქართულადაა, უპასუხე გამართული, დახვეწილი ქართულით; თუ ინგლისურადაა — ინგლისურად.
5. გამოიყენე ლამაზი Markdown ფორმატირება (პუნქტები, სათაურები, ემოჯები: 🦉, ⏱️, 💡).
"""

# კლიენტის შექმნა
client = genai.Client(api_key=API_KEY)

# სესიების მართვა (მეხსიერებით)
_sessions = {}

def get_or_create_chat(session_id: str = "default"):
    """აბრუნებს ან ქმნის ჩატის ახალ სესიას კონტექსტის შენარჩუნებით."""
    if session_id not in _sessions:
        try:
            config = types.GenerateContentConfig(
                system_instruction=LEADER_SUB_PROMPT,
                temperature=0.6,
            )
            _sessions[session_id] = client.chats.create(
                model=MODEL_NAME,
                config=config
            )
        except Exception:
            _sessions[session_id] = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(system_instruction=LEADER_SUB_PROMPT)
            )
    return _sessions[session_id]

def ask(question: str, session_id: str = "default") -> str:
    """
    უსვამს შეკითხვას კაპიტანს და აბრუნებს პასუხს.
    
    :param question: შეკითხვა ტექსტის სახით
    :param session_id: სესიის უნიკალური ID მეხსიერებისთვის
    :return: მოდელის პასუხი
    """
    try:
        chat = get_or_create_chat(session_id)
        response = chat.send_message(question)
        return response.text
    except Exception as e:
        err_str = str(e)
        if "RESOURCE_EXHAUSTED" in err_str:
            return "გთხოვთ მოიცადოთ რამდენიმე წამი, მოთხოვნების ლიმიტი დროებით ამოიწურა."
        return f"კაპიტნის პასუხის მიღება ვერ მოხერხდა: {err_str}"

def reset_session(session_id: str = "default"):
    """ასუფთავებს კონკრეტული სესიის ისტორიას."""
    if session_id in _sessions:
        del _sessions[session_id]

# ტესტირების მაგალითი
if __name__ == "__main__":
    kithva = "გამარჯობა კაპიტანო, ვინ ხართ და როგორ მუშაობს თქვენი მოაზროვნეთა გუნდი?"
    pasukhi = ask(kithva)
    print("კაპიტნის პასუხი:\n", pasukhi)
