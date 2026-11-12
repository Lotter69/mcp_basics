#!/usr/bin/env python3
"""
Einfacher API-Call an lokales Ollama Modell
Verwendet: qwen2.5-coder:3b
"""
import ollama

def main():
    print("Ollama Chat gestartet")
    print("Modell: qwen2.5-coder:3b")
    print("Geben Sie 'exit' ein, um den Chat zu beenden")
    print("=" * 60)
    
    # Chat-Schleife
    while True:
        # Frage eingeben
        frage = input("\nIhre Frage: ").strip()
        
        # Beenden bei "exit"
        if frage.lower() == 'exit':
            print("\n Chat beendet. Auf Wiedersehen!")
            break
        
        # Leere Eingabe ignorieren
        if not frage:
            print("  Bitte geben Sie eine Frage ein.")
            continue
        
        # API-Call an Ollama
        print("\n Sende Anfrage an Ollama...")
        
        try:
            response = ollama.chat(
                model='qwen2.5-coder:3b',
                messages=[
                    {
                        'role': 'user',
                        'content': frage
                    }
                ]
            )
            
            # Antwort ausgeben
            print("\n Antwort:")
            print(response['message']['content'])
            print("-" * 60)
            
        except Exception as e:
            print(f"\n Fehler bei der Kommunikation mit Ollama: {e}")
            print("\nStellen Sie sicher, dass:")
            print("  1. Ollama läuft (ollama serve)")
            print("  2. Das Modell qwen2.5-coder:3b installiert ist")
            print("     (ollama pull qwen2.5-coder:3b)")
            print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Programm durch Strg+C beendet.")
    except Exception as e:
        print(f"\n Fehler: {e}\n")
