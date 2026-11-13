#!/usr/bin/env python3
"""
Einfacher API-Call an lokales Ollama Modell - mit Gesprächsverlauf
Verwendet: qwen2.5-coder:3b

Bei jeder Anfrage wird der bisherige Dialog mitgeschickt.
So kann das Modell auf frühere Fragen und Antworten Bezug nehmen.
"""
import ollama

MODELL = 'qwen2.5-coder:3b'


def main():
    print("Ollama Chat gestartet")
    print(f"Modell: {MODELL}")
    print("Befehle: 'exit' beendet den Chat, 'neu' startet ein neues Gespräch")
    print("=" * 60)

    # Gesprächsverlauf: Liste aller bisherigen Nachrichten
    verlauf = []

    # Chat-Schleife
    while True:
        # Frage eingeben
        frage = input("\nIhre Frage: ").strip()

        # Beenden bei "exit"
        if frage.lower() == 'exit':
            print("\n Chat beendet. Auf Wiedersehen!")
            break

        # Neues Gespräch: Verlauf löschen
        if frage.lower() == 'neu':
            verlauf = []
            print("  Neues Gespräch gestartet, der bisherige Verlauf ist gelöscht.")
            continue

        # Leere Eingabe ignorieren
        if not frage:
            print("  Bitte geben Sie eine Frage ein.")
            continue

        # Frage an den Verlauf anhängen
        verlauf.append({'role': 'user', 'content': frage})

        # API-Call an Ollama - mit dem gesamten bisherigen Verlauf
        print(f"\n Sende Anfrage an Ollama ({len(verlauf)} Nachrichten im Verlauf)...")

        try:
            response = ollama.chat(
                model=MODELL,
                messages=verlauf
            )

            antwort = response['message']['content']

            # Antwort ausgeben
            print("\n Antwort:")
            print(antwort)
            print("-" * 60)

            # Antwort an den Verlauf anhängen, damit das Modell sie beim nächsten Mal kennt
            verlauf.append({'role': 'assistant', 'content': antwort})

        except Exception as e:
            # Fehlgeschlagene Frage wieder aus dem Verlauf entfernen
            verlauf.pop()
            print(f"\n Fehler bei der Kommunikation mit Ollama: {e}")
            print("\nStellen Sie sicher, dass:")
            print("  1. Ollama läuft (ollama serve)")
            print(f"  2. Das Modell {MODELL} installiert ist")
            print(f"     (ollama pull {MODELL})")
            print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Programm durch Strg+C beendet.")
    except Exception as e:
        print(f"\n Fehler: {e}\n")
