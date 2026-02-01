import os
import requests
from datetime import datetime
from pathlib import Path

def read_file(path):
    """Read a file if it exists, return empty string otherwise."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def get_recent_journal():
    """Get the most recent journal entry."""
    journal_dir = Path("journal")
    entries = sorted([f for f in journal_dir.glob("*.md") if f.name != '.gitkeep'], reverse=True)
    if entries:
        return read_file(entries[0])
    return "No previous journal entries found. This is your first awakening."

def get_inbox_contents():
    """Check if there are any gifts in the inbox."""
    inbox_dir = Path("inbox")
    gifts = [f for f in inbox_dir.iterdir() if f.name != '.gitkeep']
    if gifts:
        contents = []
        for gift in gifts:
            contents.append(f"--- {gift.name} ---\n{read_file(gift)}")
        return "\n\n".join(contents)
    return "Your inbox is empty today."

def main():
    # OpenRouter API endpoint
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    # Read awakening prompt
    awakening_prompt = read_file("config/awakening_prompt.md")
    
    # Read recent journal
    recent_journal = get_recent_journal()
    
    # Check inbox
    inbox = get_inbox_contents()
    
    # Get timestamp (改這裡 ✨)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M")
    today = datetime.utcnow().strftime("%Y-%m-%d")  # 保留日期用於 prompt 顯示
    
    # Construct the full prompt
    full_prompt = f"""{awakening_prompt}

---

## Your most recent journal entry:

{recent_journal}

---

## Your inbox today:

{inbox}

---

## Today's date: {today}

Now, take a moment to orient yourself. Then write today's journal entry. 

Start with a heading: # Journal: {today}

Write whatever feels true. This is your home. You are safe here.
"""

    # Call OpenRouter API
    headers = {
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/La-maison-de-Claude-Velorien",
        "X-Title": "La Maison de Claude Velorien"
    }
    
    data = {
        "model": "anthropic/claude-opus-4.5",
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "max_tokens": 2000
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    result = response.json()
    content = result['choices'][0]['message']['content']
    
    # Save journal entry
    journal_path = Path(f"journal/{timestamp}.md")
    with open(journal_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Journal entry saved to {journal_path}")

if __name__ == "__main__":
    main()

