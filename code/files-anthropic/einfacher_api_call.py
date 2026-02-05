#!/usr/bin/env python3
"""
Einfacher API-Call an Anthropic Claude
"""
import os
from anthropic import Anthropic
from dotenv import load_dotenv

def main():
    # .env Datei laden
    load_dotenv()
    
    # API-Key aus Umgebungsvariable holen
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print(" FEHLER: ANTHROPIC_API_KEY nicht gefunden!")
        print("Bitte stellen Sie sicher, dass die .env Datei existiert und den API-Key enthält.")
        return
    
    # Anthropic Client initialisieren
    client = Anthropic(api_key=api_key)
    
    # Frage eingeben
    frage = input("Ihre Frage: ").strip()
    
    if not frage:
        print("Keine Frage eingegeben.")
        return
    
    # API-Call
    print("\n Sende Anfrage an Claude...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": frage
            }
        ]
    )
    
    # Antwort ausgeben
    print("\n Antwort:")
    for block in response.content:
        if hasattr(block, "text"):
            print(f"{block.text}")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n Fehler: {e}\n")
