"""
   #########  #####   #####   #########     #########   ###########   #########  ###########  ###########
  ###.....###..###   ..###   ###.....###   ###.....### .#...###...#  ###.....###..###.....###.#...###...#
 ###     ...  .###    .###  .###    .###  .###    .### .   .###  .  ###     ...  .###    .###.   .###  . 
.###          .###########  .###########  .###########     .###    .###          .##########     .###    
.###          .###.....###  .###.....###  .###.....###     .###    .###    ##### .###......      .###    
..###     ### .###    .###  .###    .###  .###    .###     .###    ..###  ..###  .###            .###    
 ..#########  #####   ##### #####   ##### #####   #####    #####    ..#########  #####           #####   
  .........  .....   ..... .....   ..... .....   .....    .....      .........  .....           .....    
🎨 Holi Chaat Personality Quiz
A chatbot that uses AI to match you with your perfect chaat based on your personality.

Workshop: How to run open-source AI models locally with Ollama
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
import colorsys

INACTIVITY_TIMEOUT = 60

# ============================================================
# MENU (from the vendor)
# ============================================================

MENU = {
    "Gol Gappe": {
        "description": "Crispy puris filled with spiced water, tamarind, and chickpeas. The classic street experience - fast, tangy, and exhilarating.",
        "vibe": "adventurous, playful, loves intensity and thrills"
    },
    "Samosa Chaat": {
        "description": "Crushed samosa topped with Amritsari choley (curried chickpeas), chutneys, and spices. Hearty, bold, and unapologetically indulgent.",
        "vibe": "bold, go-big-or-go-home, loves rich flavors"
    },
    "Bhaley Papdi": {
        "description": "Crispy papdi and soft bhaley (lentil fritters) with yogurt, chutneys, and spices. Balanced, layered, a little bit of everything.",
        "vibe": "balanced, thoughtful, appreciates complexity"
    },
    "Bun Choley": {
        "description": "Soft bun served with spiced choley. Comforting, filling, and perfect for sharing. The warm hug of chaat.",
        "vibe": "warm, social, here for comfort and connection"
    }
}

# ============================================================
# QUIZ QUESTIONS (Holi-themed!)
# ============================================================

QUESTIONS = [
    {
        "question": "Which Silsila character speaks to you most?",
        "options": [
            "A) Amit (Amitabh Bachchan): the passionate poet who lives for what sets his soul on fire",
            "B) Chandni (Rekha): bold, magnetic, and all-in no matter the cost",
            "C) Shekhar (Shashi Kapoor): steady, principled, always doing what's right",
            "D) Shobha (Jaya Bachchan): warmth, resilience, and love that holds everything together"
        ]
    },
    {
        "question": "It's Holi! What does your celebration look like?",
        "options": [
            "A) I'm out in the streets the moment it starts. No plan, just pure instinct.",
            "B) I organized the whole thing: pichkari stations, color buckets, a playlist. Go big or go home.",
            "C) Cards, chai, and a small circle of my favorite people. Low-key is the way.",
            "D) I cook for everyone and make sure the whole family is together."
        ]
    },
    {
        "question": "It's the week before Holi. How are you getting ready?",
        "options": [
            "A) I'm not. Showing up empty-handed and seeing what happens is the move.",
            "B) Buying supplies in bulk and planning a setup people will talk about for years.",
            "C) I've thought through my outfit, my playlist, and who I want to spend it with.",
            "D) Coordinating with everyone to make sure no one misses out."
        ]
    },
    {
        "question": "What's your favorite kind of Holi memory?",
        "options": [
            "A) Getting completely drenched out of nowhere. Pure chaos, pure joy.",
            "B) The feast afterwards. A table full of food, everyone eating together, nobody holding back.",
            "C) The smell of gulal and marigolds in the air right before everything started.",
            "D) Getting an unexpected call from someone far away, just to say Holi hai."
        ]
    }
]

# ============================================================
# SYSTEM PROMPT FOR THE AI
# ============================================================

MENU_TEXT = "\n".join([
    f"- {name}: {info['description']} (Best for: {info['vibe']})"
    for name, info in MENU.items()
])

SYSTEM_PROMPT = f"""You are a fun, warm chaat personality expert at a Holi celebration.

Based on the user's quiz answers, match them with ONE chaat from this menu:

{MENU_TEXT}

You MUST respond with valid JSON in this exact format:
{{
    "personality_title": "A fun 2-4 word title for their personality",
    "chaat": "Exact name from menu: Gol Gappe, Samosa Chaat, Bhaley Papdi, or Bun Choley",
    "why": "2-3 sentences explaining why this chaat matches their personality. Be specific to their answers. Make it fun and celebratory.",
    "fun_fact": "One fun fact about the 1981 Bollywood film Silsila - its making, the cast, or a memorable moment from the film"
}}

MATCHING GUIDE:
- Mostly A answers = High energy, thrill-seeker → Gol Gappe (the rush of the pani, the race to eat)
- Mostly B answers = Bold, maximalist → Samosa Chaat (go big, indulgent, no holding back)
- Mostly C answers = Thoughtful, appreciates nuance → Bhaley Papdi (layered, complex, rewarding)
- Mostly D answers = Warm, people-focused → Bun Choley (comfort food, sharing, togetherness)

If answers are mixed, use your judgment to find the best match based on their overall vibe.

Keep it celebratory - it's Holi!

Respond ONLY with the JSON object. No markdown, no code fences, no explanation - just the raw JSON."""

# ============================================================
# FUNCTION: Talk to Ollama
# ============================================================

def ask_ollama(prompt, model="llama3.2"):
    """
    Send a prompt to Ollama and get a response.
    Uses the Ollama HTTP API directly — works identically on Windows and macOS.
    """
    try:
        payload = json.dumps({
            "model": model,
            "prompt": prompt,
            "stream": False
        }).encode('utf-8')

        req = urllib.request.Request(
            "http://localhost:11434/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('response', '')
    except urllib.error.URLError:
        return "ERROR: Ollama not running. Start it with: ollama serve"
    except Exception as e:
        return f"ERROR: {str(e)}"

# ============================================================
# FUNCTION: Run the Quiz
# ============================================================

def run_quiz():
    """Run the 4-question personality quiz and collect answers."""
    
    print("\n" + "="*50)
    print("🎨 HOLI CHAAT PERSONALITY QUIZ 🎨")
    print("="*50)
    print("\nAnswer 4 quick questions to find your perfect chaat!\n")
    
    answers = []

    for i, q in enumerate(QUESTIONS, 1):
        print(f"\n--- Question {i} of {len(QUESTIONS)} ---")
        print(f"\n{q['question']}\n")

        for option in q['options']:
            print(f"  {option}")

        answers.append(read_answer("\nYour answer (A/B/C/D): "))

    return answers

# ============================================================
# FUNCTION: Get Chaat Match with AI
# ============================================================

def get_chaat_match(answers, max_retries=2):
    """Send quiz answers to the AI and get a chaat recommendation."""

    print("\n✨ Finding your perfect chaat match...\n")

    # Format the answers for the AI
    answer_text = "\n".join([
        f"Question {i+1}: {QUESTIONS[i]['question']}\nAnswer: {QUESTIONS[i]['options'][ord(answers[i])-ord('A')]}"
        for i in range(len(answers))
    ])

    # Create the full prompt
    full_prompt = f"""{SYSTEM_PROMPT}

USER'S QUIZ ANSWERS:
{answer_text}

Generate their chaat match as JSON:"""

    for _ in range(max_retries):
        response = ask_ollama(full_prompt)
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end > start:
            try:
                data = json.loads(response[start:end])
                if {'personality_title', 'chaat', 'why', 'fun_fact'}.issubset(data) and data['chaat'] in MENU:
                    return data
            except json.JSONDecodeError:
                pass

    return _fallback_result(answers)


def _fallback_result(answers):
    """Deterministic fallback when the AI response can't be parsed."""
    most_common = max(set(answers), key=answers.count)
    mapping = {
        'A': ('The Spontaneous Soul', 'Gol Gappe'),
        'B': ('The Bold Maximalist', 'Samosa Chaat'),
        'C': ('The Thoughtful One', 'Bhaley Papdi'),
        'D': ('The Warm Heart', 'Bun Choley'),
    }
    title, chaat = mapping[most_common]
    return {
        'personality_title': title,
        'chaat': chaat,
        'why': f"Your answers reveal a personality that perfectly matches {chaat}. Dive in and enjoy every bite!",
        'fun_fact': "Silsila (1981) was directed by Yash Chopra. The film's iconic title song 'Rang Barse' has become one of the most beloved Holi anthems of all time."
    }

# ============================================================
# FUNCTION: Display Results
# ============================================================

def display_results(data):
    """Display the chaat recommendation."""

    print("\n" + "="*50)
    print("🥳 YOUR HOLI CHAAT MATCH 🥳")
    print("="*50)

    print(f"\n✨ You are: {data['personality_title'].upper()} ✨")

    print(f"\n🍽️  Your chaat: {data['chaat'].upper()}")
    print(f"\n{MENU[data['chaat']]['description']}")

    print(f"\n💬 Why this is YOUR chaat:")
    print(f"   {data['why']}")

    print(f"\n💡 Fun fact: {data['fun_fact']}")

    print("\n" + "="*50)
    print(f"Ask the vendor for: {data['chaat'].upper()}")
    print("="*50)

    return data

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def wait_with_countdown(timeout=INACTIVITY_TIMEOUT):
    """Wait for any keypress, showing a live countdown. Returns on keypress or timeout."""
    if sys.platform == "win32":
        import msvcrt
        for remaining in range(timeout, 0, -1):
            sys.stdout.write(f"\r  Resetting in {remaining}s... (press any key to restart)  ")
            sys.stdout.flush()
            for _ in range(10):  # check 10x per second
                if msvcrt.kbhit():
                    msvcrt.getch()
                    print()
                    return
                time.sleep(0.1)
        print()
    else:
        import tty, termios, select
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            for remaining in range(timeout, 0, -1):
                sys.stdout.write(f"\r  Resetting in {remaining}s... (press any key to restart)  ")
                sys.stdout.flush()
                if select.select([sys.stdin], [], [], 1.0)[0]:
                    sys.stdin.read(1)
                    print()
                    return
            print()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def flush_input():
    """Discard any buffered keystrokes so queued input doesn't bleed into the next read."""
    if sys.platform == "win32":
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    else:
        import termios
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

def read_answer(prompt):
    """Wait for a single A/B/C/D keypress with no timeout or countdown. Returns char."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    if sys.platform == "win32":
        import msvcrt
        while True:
            ch = msvcrt.getwch().upper()
            if ch in ('A', 'B', 'C', 'D'):
                sys.stdout.write(ch + '\n')
                sys.stdout.flush()
                return ch
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                ch = sys.stdin.read(1).upper()
                if ch in ('A', 'B', 'C', 'D'):
                    sys.stdout.write(ch + '\n')
                    sys.stdout.flush()
                    return ch
                elif ch == '\x03':  # Ctrl+C
                    raise KeyboardInterrupt
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def clear_screen():
    """Clear the terminal screen. Works on Windows and macOS."""
    os.system('cls' if sys.platform == "win32" else 'clear')

def rainbow_print(text):
    """Print text with a rainbow gradient, or plain if truecolor isn't supported."""
    truecolor = os.environ.get('COLORTERM', '').lower() in ('truecolor', '24bit')
    lines = text.split('\n')
    if not truecolor:
        print(text)
        return
    max_width = max((len(line) for line in lines), default=1)
    for line in lines:
        out = ''
        for x, ch in enumerate(line):
            hue = x / max_width
            r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
            out += f'\033[38;2;{int(r*255)};{int(g*255)};{int(b*255)}m{ch}'
        print(out + '\033[0m')

# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    """Run the complete chaat quiz experience."""

    rainbow_print("""
   #########  #####   #####   #########     #########   ###########   #########  ###########  ###########
  ###.....###..###   ..###   ###.....###   ###.....### .#...###...#  ###.....###..###.....###.#...###...#
 ###     ...  .###    .###  .###    .###  .###    .### .   .###  .  ###     ...  .###    .###.   .###  .
.###          .###########  .###########  .###########     .###    .###          .##########     .###
.###          .###.....###  .###.....###  .###.....###     .###    .###    ##### .###......      .###
..###     ### .###    .###  .###    .###  .###    .###     .###    ..###  ..###  .###            .###
 ..#########  #####   ##### #####   ##### #####   #####    #####    ..#########  #####           #####
  .........  .....   ..... .....   ..... .....   .....    .....      .........  .....           .....

""")
    print("A ChaatBot powered by open-source AI (Ollama)")

    # Step 1: Run the quiz
    answers = run_quiz()

    # Step 2: Get chaat match from AI
    response = get_chaat_match(answers)

    # Step 3: Display results
    display_results(response)

    print("\nHappy Holi! 🎨\n")
    print("\n" + "="*50)
    print("Press any key to start over...")
    print("="*50)
    flush_input()
    wait_with_countdown()
    clear_screen()

# ============================================================
# RUN THE PROGRAM
# ============================================================

if __name__ == "__main__":
    # Ensure UTF-8 output for emoji support on Windows
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    while True:
        main()
