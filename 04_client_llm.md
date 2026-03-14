# Laborübung 1: Analyse der LLM-Kommunikation mit Wireshark

![line](images/banner.png)

## Lernziele

Nach Abschluss dieser Laborübung können Sie:

- Den Netzwerkverkehr zwischen MCP-Client und lokalem Ollama mitschneiden
- HTTP-Traffic auf dem Loopback-Interface mit Wireshark analysieren
- JSON-basierte API-Kommunikation im Klartext lesen
- Unterscheiden, welche Informationen ans LLM gesendet werden und welche lokal beim MCP-Server verbleiben
- Die Struktur von Ollama-API-Anfragen und -Antworten verstehen

---

## Voraussetzungen

### Software
- Wireshark installiert
- Ollama läuft
- Modell z. B. `qwen2.5-coder:3b` heruntergeladen
- Python Virtual Environment mit `ollama` und `mcp` Bibliotheken [siehe Hinführung zu MCP, Schritt 2, 1b](01_lab.md)
- `mcp_client_ollama.py` und `mcp_server.py` im Projektordner

### Vorbereitung
```bash
# Prüfen: Ollama läuft
ollama list

# Prüfen: Wireshark installiert
wireshark --version
```

---

## Aufgaben

### Schritt 0: Projektordner öffnen und venv aktivieren

**Aktion:**
```bash
cd /pfad/zu/mcp-demo_ollama
source venv/bin/activate
```

**Erwartetes Ergebnis:**
- Prompt zeigt `(venv)` am Anfang
- Sie befinden sich im Projektordner

**Prüfung:**
```bash
which python3
# Sollte zeigen: /pfad/zu/Ollama-MCP-Demo/venv/bin/python3
```

---

### Schritt 1: Wireshark starten und Loopback-Interface auswählen

**Aktion:**
1. Wireshark über Terminal oder Menü starten:
   ```bash
   sudo wireshark
   ```
   (sudo nötig für Paket-Capture)

2. Im Wireshark-Hauptfenster:
   - Suchen Sie nach **"Loopback: lo"** oder **"lo"** Interface
   - **Doppelklick** auf das Loopback-Interface

**Erwartetes Ergebnis:**
- Wireshark öffnet ein Capture-Fenster
- Pakete werden noch NICHT gefiltert angezeigt
- Status unten zeigt "Capturing from 'lo'"

**Screenshot-Punkt:** Wireshark mit aktivem Loopback-Capture

---

### Schritt 2: Capture-Filter setzen (Optional - für weniger Rauschen)

**Aktion:**
1. In Wireshark oben: **Capture → Capture Filters**
2. Oder direkt beim Start Filter eingeben: `tcp port 11434`

**Hinweis:** 
- Kann auch übersprungen werden
- Wir filtern später mit Display-Filter

---

### Schritt 3: MCP-Client vorbereiten (NICHT starten!)

**Aktion:**
```bash
# Neues Terminal-Fenster öffnen
# venv aktivieren
cd /pfad/zu/Ollama-MCP-Demo
source venv/bin/activate

# BEREIT HALTEN, aber NICHT ausführen:
python3 mcp_client_ollama.py
```


---

### Schritt 4: Wireshark-Capture starten

**Aktion:**
1. Zurück zu Wireshark
2. Falls noch nicht läuft: Klick auf **grünes Hai-Symbol** (Start Capture)
3. Pakete beginnen zu erscheinen


---

### Schritt 5: MCP-Client starten und Frage eingeben

**Aktion:**
```bash
python3 mcp_client_ollama.py
```

**Warten auf Prompt:**
```
Ollama MCP Patchkabel-Lagerbestand Client gestartet
Modell: qwen2.5-coder:3b
1 Tool verfügbar:
   - patchkabel_bestand_abfragen: Fragt den aktuellen Lagerbestand...

============================================================

Ihre Anfrage (oder 'exit' zum Beenden):
```

**Eingeben z. B.:**
```
Wie viele blaue Patchkabel haben wir auf Lager?
```
---

### Schritt 6: Wireshark-Capture stoppen

**Aktion:**
1. Zurück zu Wireshark
2. Klick auf **rotes Stopp-Symbol** (Stop Capture)

---

### Schritt 7: Display-Filter anwenden

**Aktion:**
1. In Wireshark oben im Filter-Feld eingeben:
   ```
   tcp.port == 11434 #Standardport für Ollama
   ```
2. Enter drücken oder auf Pfeil-Symbol klicken

---

### Schritt 8: HTTP-Request identifizieren

**Aktion:**
1. Suchen Sie in der Paketliste nach Zeile mit:
   - **Protocol:** HTTP
   - **Info:** `POST /api/chat HTTP/1.1`
   
2. Klicken Sie auf diese Zeile

**Hinweis:** Es gibt mindestens 2 POST-Requests:
- 1. Request: Mit Ihrer Frage
- 2. Request: Mit Tool-Ergebnis (für finale Antwort)

---

### Schritt 9: HTTP Stream folgen

**Aktion:**
1. **Rechtsklick** auf das HTTP POST-Paket
2. Wählen Sie: **Follow → TCP Stream** (oder HTTP Stream)

**Erwartetes Ergebnis:**
- Neues Fenster öffnet sich
- Zeigt vollständigen HTTP-Request und Response
- Farbcodiert (Rot = Request, Blau = Response)

---

### Schritt 10: Erste Anfrage analysieren (Benutzer-Frage)

**Im Stream-Fenster sehen Sie:**

**HTTP Request (Rot):**
```http
POST /api/chat HTTP/1.1
Host: localhost:11434
Content-Type: application/json
...

{
  "model": "qwen2.5-coder:3b",
  "messages": [
    {
      "role": "system",
      "content": "Du bist ein hilfreicher Assistent mit Zugriff auf Tools..."
    },
    {
      "role": "user",
      "content": "Wie viele blaue Patchkabel haben wir auf Lager?"
    }
  ]
}
```

**HTTP Response (Blau):**
```json
{
  "model": "qwen2.5-coder:3b",
  "message": {
    "role": "assistant",
    "content": "{\"tool\": \"patchkabel_bestand_abfragen\", \"farbe\": \"blau\"}"
  }
}
```
---

### Schritt 11: Zweite Anfrage analysieren (Mit Tool-Ergebnis)

**Aktion:**
1. Stream-Fenster schließen
2. In Paketliste: Nächsten HTTP POST finden
3. Wieder: **Follow → TCP Stream**

**Im Stream sehen Sie:**

**HTTP Request (Rot):**
```json
{
  "model": "qwen2.5-coder:3b",
  "messages": [
    {
      "role": "system",
      "content": "Du bist ein hilfreicher Assistent..."
    },
    {
      "role": "user",
      "content": "Wie viele blaue Patchkabel haben wir auf Lager?"
    },
    {
      "role": "assistant",
      "content": "{\"tool\": \"patchkabel_bestand_abfragen\", \"farbe\": \"blau\"}"
    },
    {
      "role": "user",
      "content": "Tool-Ergebnis: Bestand blaue 1m Patchkabel: 45 Stück\n\nBitte formuliere eine natürliche Antwort..."
    }
  ]
}
```

**HTTP Response (Blau):**
```json
{
  "message": {
    "role": "assistant",
    "content": "Im Lager befinden sich derzeit 45 Stück blaue 1m Patchkabel."
  }
}
```

---

### Schritt 11: Reflexion und weitere Experimente

- Was wird dem LLM mitgeteilt?

- Was bleibt auf der Seite zwischen MCP-Client und MCP-Server?

- Kann das LLM die Python-Implementierung des Tools sehen?

- Woher weiß das LLM, welche Parameter das Tool benötigt?

- Warum sehen wir die MCP-Kommunikation nicht in Wireshark?

- Was wäre der Unterschied, wenn wir Claude API statt Ollama nutzen würden?

---

**Zusätzliche Experimente:**

1. **Andere Frage stellen:**
   ```
   Zeige mir den gesamten Lagerbestand
   ```
   → Analysieren Sie die unterschiedlichen Parameter im Tool-Call

2. **Komplexere Frage:**
   ```
   Haben wir genug rote Kabel für eine Entnahme von 25 Stück?
   ```
   → Beobachten Sie, wie das LLM mit dem Ergebnis rechnet

3. **Frage ohne Tool:**
   ```
   Was ist ein Patchkabel?
   ```
   → Sehen Sie, ob ein Tool-Call gemacht wird (sollte nicht!)


---


**Weiter mit Laborübung 2: MCP-Inspector Analyse!** →

## Autoren und Urheberrecht
- Created by: Michael Lotter
- Date: 12/2025
- Version: v1.0

![line](images/banner.png)
<p align="center">
<a href="03_architecture.md"><img src="images/previous.png" width="150px"></a>
<a href="05_inspector.md"><img src="images/next.png" width="150px"></a>
</p>
