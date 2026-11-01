import os
import sys
import json
import re
from typing import Dict, Any, List

# Fix Windows console encoding
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

import leader
import mathematics
import biology
import history
import geography
import sport

# Agent Registry with Rich Metadata for "რა? სად? როდის?" Intellect Club
AGENTS = {
    "leader": {
        "id": "leader",
        "name": "ალექსი (Alex)",
        "role": "Team Captain & Master Strategist",
        "role_ka": "გუნდის კაპიტანი და სტრატეგი",
        "avatar": "🦉",
        "color": "#f59e0b",
        "glow": "rgba(245, 158, 11, 0.4)",
        "gradient": "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)",
        "badge": "კაპიტანი | Captain",
        "specialty": "Strategy, Coordination & 1-Minute Synthesis",
        "specialty_ka": "გუნდური სტრატეგია, 1 წუთი ფიქრისთვის და სინთეზი",
        "module": leader,
        "sample_prompts": [
            {"en": "Captain, lead the 1-minute team discussion on an intellectual riddle.", "ka": "კაპიტანო, წარუძეხი გუნდის 1 წუთიან განხილვას რთულ შეკითხვაზე."},
            {"en": "What is the best deduction tactic in 'What? Where? When?'", "ka": "რა არის საუკეთესო დედუქციური ტაქტიკა 'რა? სად? როდის?' თამაშში?"},
            {"en": "Synthesize clues from geography, history, and science.", "ka": "გააერთიანე გეოგრაფიული, ისტორიული და საბუნებისმეტყველო მინიშნებები."}
        ]
    },
    "math": {
        "id": "math",
        "name": "თეა (Tea)",
        "role": "Mathematics & Logic Specialist",
        "role_ka": "მათემატიკისა და ლოგიკის ექსპერტი",
        "avatar": "📐",
        "color": "#06b6d4",
        "glow": "rgba(6, 182, 212, 0.4)",
        "gradient": "linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)",
        "badge": "ლოგიკა | Logic",
        "specialty": "Calculus, Logic Puzzles & Combinatorics",
        "specialty_ka": "ლოგიკური თავსატეხები, კომბინატორიკა და ალგებრა",
        "module": mathematics,
        "sample_prompts": [
            {"en": "Give me a classic intellectual logic riddle with numbers.", "ka": "მომეცი კლასიკური ლოგიკური თავსატეხი 'რა? სად? როდის?'-ის სტილში."},
            {"en": "Explain Euler's identity e^(iπ) + 1 = 0 in simple terms.", "ka": "ამიხსენი ეილერის იგივეობა e^(iπ) + 1 = 0 მარტივი ენით."},
            {"en": "Solve the Monty Hall probability paradox.", "ka": "ამიხსენი მონტი ჰოლის ალბათური პარადოქსი."}
        ]
    },
    "geography": {
        "id": "geography",
        "name": "სანდრო (Sandro)",
        "role": "Geography & Cartography Explorer",
        "role_ka": "გეოგრაფიისა და მოგზაურობის ექსპერტი",
        "avatar": "🌍",
        "color": "#0ea5e9",
        "glow": "rgba(14, 165, 233, 0.4)",
        "gradient": "linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)",
        "badge": "გეოგრაფია | Geography",
        "specialty": "World Geography, Capitals, Anomalies & Cartography",
        "specialty_ka": "მსოფლიო რუკა, დედაქალაქები, საზღვრები და გეოგრაფიული ანომალიები",
        "module": geography,
        "sample_prompts": [
            {"en": "Which country has the most natural lakes in the world and why?", "ka": "რომელ ქვეყანას აქვს ყველაზე მეტი ბუნებრივი ტბა მსოფლიოში?"},
            {"en": "Tell me about the most unusual geopolitical enclaves and borders.", "ka": "მომიყევი მსოფლიოს ყველაზე უცნაურ ანკლავებსა და საზღვრებზე."},
            {"en": "What unique geographic features define the Caucasus and Georgia?", "ka": "რა უნიკალური გეოგრაფიული მახასიათებლები გამოარჩევს კავკასიასა და საქართველოს?"}
        ]
    },
    "biology": {
        "id": "biology",
        "name": "ლუკა (Luka)",
        "role": "Biosciences & Nature Researcher",
        "role_ka": "ბიოლოგიისა და ცოცხალი სამყაროს მკვლევარი",
        "avatar": "🧬",
        "color": "#10b981",
        "glow": "rgba(16, 185, 129, 0.4)",
        "gradient": "linear-gradient(135deg, #10b981 0%, #059669 100%)",
        "badge": "ბიოლოგია | Biology",
        "specialty": "Flora, Fauna, Genetics, Ecology & Evolution",
        "specialty_ka": "ფლორა, ფაუნა, გენეტიკა, ეკოლოგია და ევოლუცია",
        "module": biology,
        "sample_prompts": [
            {"en": "Which animal possesses the most extraordinary biological superpower?", "ka": "რომელ ცხოველს გააჩნია ყველაზე უჩვეულო ბიოლოგიური თვისება?"},
            {"en": "How does mimicry help species survive in the wild?", "ka": "როგორ ეხმარება მიმიკრია ცოცხალ ორგანიზმებს გადარჩენაში?"},
            {"en": "Explain how bioluminescence functions in deep-sea creatures.", "ka": "როგორ მუშაობს ბიოლუმინესცენცია ოკეანის სიღრმეების ბინადრებში?"}
        ]
    },
    "history": {
        "id": "history",
        "name": "ნინო (Nino)",
        "role": "Civilizations & History Chronicler",
        "role_ka": "ისტორიკოსი და ცივილიზაციების მემატიანე",
        "avatar": "🏛️",
        "color": "#f43f5e",
        "glow": "rgba(244, 63, 94, 0.4)",
        "gradient": "linear-gradient(135deg, #f43f5e 0%, #e11d48 100%)",
        "badge": "ისტორია | History",
        "specialty": "Ancient Civilizations, Artifacts, Georgia & World History",
        "specialty_ka": "ანტიკური ეპოქები, არტეფაქტები, საქართველო და მსოფლიო ისტორია",
        "module": history,
        "sample_prompts": [
            {"en": "What is the historical origin of the Rosetta Stone?", "ka": "რა ისტორიული მნიშვნელობა ჰქონდა როზეტის ქვას ეგვიპტური იეროგლიფების გაშიფვრაში?"},
            {"en": "Tell me about Queen Tamar and the Golden Age of Georgia.", "ka": "მომიყევი თამარ მეფის ეპოქასა და საქართველოს ოქროს ხანაზე."},
            {"en": "What ingenious strategies won the Battle of Didgori in 1121?", "ka": "რა სამხედრო სტრატეგიით გაიმარჯვა დავით აღმაშენებელმა დიდგორის ბრძოლაში?"}
        ]
    },
    "sport": {
        "id": "sport",
        "name": "დავითი (David)",
        "role": "Sports, Olympics & Athletics Specialist",
        "role_ka": "სპორტისა და ოლიმპიადის ექსპერტი",
        "avatar": "⚽",
        "color": "#f97316",
        "glow": "rgba(249, 115, 22, 0.4)",
        "gradient": "linear-gradient(135deg, #f97316 0%, #ea580c 100%)",
        "badge": "სპორტი | Sport",
        "specialty": "Football, Basketball, Olympics, Georgian Sports & Records",
        "specialty_ka": "ფეხბურთი, კალათბურთი, ოლიმპიური თამაშები, ქართული სპორტი და რეკორდები",
        "module": sport,
        "sample_prompts": [
            {"en": "Tell me the story of Dinamo Tbilisi winning the European Cup Winners' Cup in 1981.", "ka": "მომიყევი 1981 წლის 13 მაისზე — როცა დინამო თბილისმა ევროპის თასი მოიგო."},
            {"en": "Which athlete holds the most Olympic gold medals in history?", "ka": "რომელ სპორტსმენს აქვს მოპოვებული ყველაზე მეტი ოლიმპიური ოქროს მედალი?"},
            {"en": "What are the most famous intellectual trivia facts about the FIFA World Cup?", "ka": "რა საინტერესო ინტელექტუალური ფაქტებია ცნობილი მსოფლიო ჩემპიონატებზე?"}
        ]
    }
}

def ask_agent(agent_id: str, question: str, session_id: str = "default") -> str:
    """Dispatches question to the chosen agent."""
    if agent_id not in AGENTS:
        agent_id = "leader"
    agent_mod = AGENTS[agent_id]["module"]
    return agent_mod.ask(question, session_id)

def reset_agent(agent_id: str, session_id: str = "default"):
    """Resets memory for a specific agent."""
    if agent_id in AGENTS:
        AGENTS[agent_id]["module"].reset_session(session_id)

def reset_all_sessions(session_id: str = "default"):
    """Resets all agent memories."""
    for info in AGENTS.values():
        info["module"].reset_session(session_id)

def smart_route(question: str) -> str:
    """Detects the most appropriate specialist based on keywords."""
    q_lower = question.lower()
    
    # Sport keywords
    sport_kw = ["სპორტ", "ფეხბურთ", "კალათბურთ", "ოლიმპიად", "რაგბი", "ჭიდაობ", "ძიუდო", 
                "ჩემპიონ", "გოლი", "ჩოგბურთ", "ჭადრაკ", "მატჩ", "დინამო", "sport", "football", 
                "soccer", "basketball", "olympic", "tennis", "rugby", "athlete", "fifa", "uefa"]
    if any(k in q_lower for k in sport_kw):
        return "sport"

    # Geography keywords
    geo_kw = ["გეოგრაფი", "ქვეყან", "დედაქალაქ", "მთა", "მდინარ", "ოკეან", "ზღვა", "ტბა", 
              "კონტინენტ", "რუკა", "საზღვარ", "კუნძულ", "ვულკან", "უდაბნო", "geography", 
              "capital", "river", "mountain", "ocean", "country", "island", "continent", "border"]
    if any(k in q_lower for k in geo_kw):
        return "geography"

    # Mathematics & Logic keywords
    math_kw = ["math", "მათემატიკ", "ფორმულ", "განტოლებ", "წარმოებულ", "ინტეგრალ", 
               "პითაგორ", "ალგებრ", "გეომეტრი", "x^", "+", "=", "ალბათობ", "რიცხვ", "ლოგიკ", "paradox"]
    if any(k in q_lower for k in math_kw):
        return "math"
        
    # Biology keywords
    bio_kw = ["bio", "ბიოლოგი", "დნმ", "dna", "უჯრედ", "გენეტიკ", "ორგანიზმ", "crispr", 
              "ევოლუცი", "ანატომი", "ტვინ", "ნეირონ", "ბაქტერი", "ვირუს", "ეკოლოგი", "ცხოველ", "მცენარ"]
    if any(k in q_lower for k in bio_kw):
        return "biology"
        
    # History keywords
    hist_kw = ["histor", "ისტორი", "ომი", "ომებ", "საუკუნ", "ცივილიზაცი", "მეფე", "იმპერი", 
               "რომ", "ეგვიპტ", "თამარ", "დავით", "არქეოლოგ", "რევოლუცი", "ანტიკურ", "კეისარ", 
               "ალექსანდრე", "ბრძოლა", "ეპოქა", "ფეოდალ", "დინასტი"]
    if any(k in q_lower for k in hist_kw):
        return "history"
        
    return "leader"

def syndicate_discuss(question: str, session_id: str = "default") -> Dict[str, Any]:
    """
    'რა? სად? როდის?' 1 წუთი ფიქრისთვის (Roundtable Brainstorm):
    კაპიტანი ხსნის რაუნდს, 5 ექსპერტი (მათემატიკა, გეოგრაფია, ბიოლოგია, ისტორია, სპორტი)
    აზრს აფიქსირებს, და კაპიტანი აყალიბებს გუნდის საბოლოო ოფიციალურ პასუხს!
    """
    contributions = []

    # 1. კაპიტნის შესავალი (Captain's Gong & 1-minute Framing)
    leader_intro_prompt = (
        f"როგორც 'რა? სად? როდის?' გუნდის კაპიტანმა ალექსიმ, გააანალიზე შეკითხვა: '{question}'. "
        f"გამოაცხადე 1 წუთი ფიქრისთვის, დასვი აქცენტები და მიმართე გუნდის მოაზროვნეებს "
        f"(თეას, სანდროს, ლუკას, ნინოს და დავითს) ვერსიების წამოსაყენებლად."
    )
    leader_intro = leader.ask(leader_intro_prompt, session_id=f"syndicate_{session_id}_lead")
    contributions.append({
        "agent": "leader",
        "phase": "framing",
        "title": "კაპიტნის გახსნა: 1 წუთი ფიქრისთვის ⏱️",
        "title_en": "Captain: 1 Minute to Think ⏱️",
        "content": leader_intro
    })

    # 2. მათემატიკა & ლოგიკა (Tea)
    math_prompt = (
        f"'რა? სად? როდის?' 1 წუთიან განხილვაში შეკითხვაა: '{question}'. "
        f"როგორც მათემატიკოსმა თეამ, შეხედე საკითხს ლოგიკური, ანალიტიკური ან რაოდენობრივი კუთხით. წამოაყენე შენი ვერსია."
    )
    math_resp = mathematics.ask(math_prompt, session_id=f"syndicate_{session_id}_math")
    contributions.append({
        "agent": "math",
        "phase": "analysis",
        "title": "თეას ლოგიკური ვერსია",
        "title_en": "Tea's Logical Deduction",
        "content": math_resp
    })

    # 3. გეოგრაფიული ხედვა (Sandro)
    geo_prompt = (
        f"'რა? სად? როდის?' განხილვაში შეკითხვაა: '{question}'. "
        f"როგორც გეოგრაფმა სანდრომ, წამოაყენე გეოგრაფიული, ტოპონიმური ან რეგიონული ვერსია (ადგილმდებარეობა, ქვეყნები, რუკა)."
    )
    geo_resp = geography.ask(geo_prompt, session_id=f"syndicate_{session_id}_geo")
    contributions.append({
        "agent": "geography",
        "phase": "analysis",
        "title": "სანდროს გეოგრაფიული ვერსია",
        "title_en": "Sandro's Geographic Clue",
        "content": geo_resp
    })

    # 4. ბიოლოგიური განზომილება (Luka)
    bio_prompt = (
        f"'რა? სად? როდის?' განხილვაში შეკითხვაა: '{question}'. "
        f"როგორც ბიოლოგმა ლუკამ, დაუკავშირე საკითხი ცოცხალ ბუნებას, ევოლუციას, ფლორას ან ფაუნას. წამოაყენე შენი მინიშნება."
    )
    bio_resp = biology.ask(bio_prompt, session_id=f"syndicate_{session_id}_bio")
    contributions.append({
        "agent": "biology",
        "phase": "analysis",
        "title": "ლუკას ბიოლოგიური ხედვა",
        "title_en": "Luka's Biological Dimension",
        "content": bio_resp
    })

    # 5. ისტორიული კონტექსტი (Nino)
    hist_prompt = (
        f"'რა? სად? როდის?' განხილვაში შეკითხვაა: '{question}'. "
        f"როგორც ისტორიკოსმა ნინომ, წარმოადგინე ისტორიული ეპოქა, წყაროები, ტრადიცია ან წარსულის მოვლენა."
    )
    hist_resp = history.ask(hist_prompt, session_id=f"syndicate_{session_id}_hist")
    contributions.append({
        "agent": "history",
        "phase": "analysis",
        "title": "ნინოს ისტორიული ვერსია",
        "title_en": "Nino's Historical Context",
        "content": hist_resp
    })

    # 6. სპორტული ასპექტი (David)
    sport_prompt = (
        f"'რა? სად? როდის?' განხილვაში შეკითხვაა: '{question}'. "
        f"როგორც სპორტის ექსპერტმა დავითმა, გააანალიზე სპორტული, შეჯიბრებითი, ოლიმპიური ან ათლეტური კავშირი."
    )
    sport_resp = sport.ask(sport_prompt, session_id=f"syndicate_{session_id}_sport")
    contributions.append({
        "agent": "sport",
        "phase": "analysis",
        "title": "დავითის სპორტული ვერსია",
        "title_en": "David's Sports Dimension",
        "content": sport_resp
    })

    # 7. კაპიტნის საბოლოო პასუხი (Captain's Final Answer)
    synth_prompt = (
        f"გავიდა 1 წუთი შეკითხვაზე: '{question}'.\n"
        f"თეას ლოგიკა: {math_resp[:160]}...\n"
        f"სანდროს გეოგრაფია: {geo_resp[:160]}...\n"
        f"ლუკას ბიოლოგია: {bio_resp[:160]}...\n"
        f"ნინოს ისტორია: {hist_resp[:160]}...\n"
        f"დავითის სპორტი: {sport_resp[:160]}...\n"
        f"როგორც გუნდის კაპიტანმა ალექსიმ, აირჩიე ყველაზე მყარი ვერსია და ჩამოაყალიბე გუნდის ოფიციალური, "
        f"დახვეწილი და დამაჯერებელი საბოლოო პასუხი."
    )
    leader_synth = leader.ask(synth_prompt, session_id=f"syndicate_{session_id}_lead")
    contributions.append({
        "agent": "leader",
        "phase": "synthesis",
        "title": "კაპიტნის ოფიციალური პასუხი 🦉",
        "title_en": "Captain's Final Team Answer 🦉",
        "content": leader_synth
    })

    return {
        "topic": question,
        "contributions": contributions
    }

def generate_quiz(subject: str = "mixed", lang: str = "ka") -> Dict[str, Any]:
    """Generates an intellectual 'რა? სად? როდის?' multiple-choice quiz question."""
    subject_map = {
        "geography": ("გეოგრაფია და მოგზაურობა", "Geography and World Exploration", "geography"),
        "sport": ("სპორტი და ოლიმპიური თამაშები", "Sport and Olympic Games", "sport"),
        "history": ("ისტორია და ცივილიზაციები", "World and Regional History", "history"),
        "biology": ("ბიოლოგია და ბუნება", "Biology and Natural Sciences", "biology"),
        "math": ("მათემატიკა და ლოგიკური თავსატეხები", "Mathematics and Logic Riddles", "math"),
        "mixed": ("რა? სად? როდის? ინტელექტუალური რაუნდი", "What? Where? When? Intellectual Challenge", "leader")
    }
    subj_name_ka, subj_name_en, target_agent = subject_map.get(subject, subject_map["mixed"])

    prompt = f"""
გენერირება გაუკეთე ერთ საინტერესო, გამჭრიახ მრავალარჩევანიან კითხვას 'რა? სად? როდის?'-ის სტილში თემაზე: {subj_name_ka}.
დააბრუნე პასუხი მკაცრად შემდეგი JSON ფორმატით და არაფერი სხვა:
{{
  "subject": "{subject}",
  "question_ka": "შეკითხვა ქართულად",
  "question_en": "Question in English",
  "options_ka": ["ვარიანტი A", "ვარიანტი B", "ვარიანტი C", "ვარიანტი D"],
  "options_en": ["Option A", "Option B", "Option C", "Option D"],
  "correct_index": 0,
  "explanation_ka": "დეტალური და საინტერესო ახსნა ქართულად",
  "explanation_en": "Detailed and interesting explanation in English"
}}
სწორი ინდექსი უნდა იყოს 0, 1, 2 ან 3.
"""
    try:
        raw_text = ask_agent(target_agent, prompt, session_id="quiz_generator")
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            data["agent"] = target_agent
            return data
    except Exception:
        pass

    # Curated authentic fallbacks
    fallbacks = {
        "geography": {
            "subject": "geography",
            "agent": "geography",
            "question_ka": "რომელია მსოფლიოში ერთადერთი ზღვა, რომელსაც არ გააჩნია სანაპირო ხმელეთი?",
            "question_en": "Which sea in the world is the only one that has no land coastline?",
            "options_ka": ["სარგასოს ზღვა", "ბარენცის ზღვა", "მარმარილოს ზღვა", "წითელი ზღვა"],
            "options_en": ["Sargasso Sea", "Barents Sea", "Sea of Marmara", "Red Sea"],
            "correct_index": 0,
            "explanation_ka": "სარგასოს ზღვა მდებარეობს ატლანტის ოკეანეში და მას საზღვრავს არა ხმელეთი, არამედ ოკეანის ოთხი მძლავრი დინება (მათ შორის გოლფსტრიმი).",
            "explanation_en": "The Sargasso Sea in the Atlantic is unique as it is defined not by land boundaries, but by four ocean currents including the Gulf Stream."
        },
        "sport": {
            "subject": "sport",
            "agent": "sport",
            "question_ka": "რომელ წელს მოიგო თბილისის 'დინამომ' ევროპის თასების მფლობელთა თასი დიუსელდორფში?",
            "question_en": "In what year did Dinamo Tbilisi win the European Cup Winners' Cup in Düsseldorf?",
            "options_ka": ["1978 წელს", "1981 წელს", "1982 წელს", "1985 წელს"],
            "options_en": ["1978", "1981", "1982", "1985"],
            "correct_index": 1,
            "explanation_ka": "1981 წლის 13 მაისს, თბილისის 'დინამომ' დიუსელდორფის ფინალში 2:1 დაამარცხა 'კარლ ცაისი' (გოლები: ვლადიმერ გუცაევი და ვიტალი დარასელია).",
            "explanation_en": "On May 13, 1981, Dinamo Tbilisi defeated Carl Zeiss Jena 2-1 in Düsseldorf with iconic goals by Gutsaev and Daraselia."
        },
        "history": {
            "subject": "history",
            "agent": "history",
            "question_ka": "რომელ წელს მოხდა დიდგორის ისტორიული ბრძოლა, რომელსაც 'ძლევაი საკვირველი' ეწოდა?",
            "question_en": "In what year did the monumental Battle of Didgori take place?",
            "options_ka": ["1089 წელს", "1121 წელს", "1184 წელს", "1225 წელს"],
            "options_en": ["1089", "1121", "1184", "1225"],
            "correct_index": 1,
            "explanation_ka": "დიდგორის ბრძოლა გაიმართა 1121 წლის 12 აგვისტოს და დავით აღმაშენებლის ბრწყინვალე გამარჯვებით დასრულდა.",
            "explanation_en": "The Battle of Didgori was fought on August 12, 1121, resulting in a decisive Georgian victory led by King David IV the Builder."
        },
        "biology": {
            "subject": "biology",
            "agent": "biology",
            "question_ka": "უჯრედის რომელ ორგანელას უწოდებენ ხშირად 'უჯრედის ენერგეტიკულ სადგურს'?",
            "question_en": "Which cellular organelle is often referred to as the 'powerhouse of the cell'?",
            "options_ka": ["რიბოსომა", "მიტოქონდრია", "გოლჯის აპარატი", "ლიზოსომა"],
            "options_en": ["Ribosome", "Mitochondria", "Golgi Apparatus", "Lysosome"],
            "correct_index": 1,
            "explanation_ka": "მიტოქონდრია აწარმოებს ადენოზინტრიფოსფატს (ATP), რომელიც წარმოადგენს უჯრედის ძირითად ენერგეტიკულ ვალუტას.",
            "explanation_en": "Mitochondria generate adenosine triphosphate (ATP), the primary energy currency for cellular functions."
        },
        "math": {
            "subject": "math",
            "agent": "math",
            "question_ka": "რა ეწოდება რიცხვთა მიმდევრობას, სადაც ყოველი წევრი წინა ორის ჯამია (0, 1, 1, 2, 3, 5, 8...)?",
            "question_en": "What is the sequence where each number is the sum of the two preceding ones (0, 1, 1, 2, 3, 5, 8...)?",
            "options_ka": ["ეილერის რიცხვები", "ფიბონაჩის მიმდევრობა", "პასკალის სამკუთხედი", "გაუსის პროგრესია"],
            "options_en": ["Euler Numbers", "Fibonacci Sequence", "Pascal's Triangle", "Gauss Progression"],
            "correct_index": 1,
            "explanation_ka": "ფიბონაჩის მიმდევრობა საოცრად უკავშირდება ოქროს კვეთას (1.618...) და ხშირად გვხვდება ცოცხალ ბუნებაშიც!",
            "explanation_en": "The Fibonacci sequence is deeply tied to the Golden Ratio (1.618...) and appears frequently in nature!"
        }
    }

    import random
    if subject in fallbacks:
        return fallbacks[subject]
    return random.choice(list(fallbacks.values()))

if __name__ == "__main__":
    print("რა? სად? როდის? - მოაზროვნეთა გუნდი:")
    for k, v in AGENTS.items():
        print(f"- {v['avatar']} {v['name']} ({k}): {v['role_ka']}")
