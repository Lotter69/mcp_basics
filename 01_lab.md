# Hinführung zu MCP (Model Context Protokoll)

![line](../../images/banner.png)

## Einführung
Chat-Anfragen an LLMs liefern je nach Fragestellung beeindruckende Ergebnisse. Die Qualität und die Schärfe der Antworten beruhen auf einem Trainingszustand des verwendetene Modells, der in der Vergangenheit liegt, der Kontext der Anfrage fehlt oft und muss abgeleitet werden. Um den Kontext herzustellen, können Anfragen angereichert werden. Eine Methode der Anreicherung haben Sie am ersten Tag des Workshops kennengelernt. In einem einfachen RAG-Workflow (Retrieval-Augmented Generation) konnten Sie mit der Anfrage Kontext bereitstellen, der zielführendere Antworten geliefert hat.

Eine weitere Methode der Kontextualisieurng bietet das Model Context Protocol, welches Sie hier kennenlernen werden.

## Lernziele 

- Grenzen einer Chat-Anfrage ohne Kontextbereitstellung austesten
- Kontextbereitstellung über bereitgestellte MCP-Tools an einem einfachen Beispiel erkunden
- Komponenten einer Toolbeschreibung und deren Aufgaben zuordnen
- Komponenten der MCP-Systemarchitektur benennen
- Kommunikationsvorgänge in der MCP-Systemarchitektur ordnen und trennen

## Szenario
Zur Vorbereitung eines Netzwerktechnikkurses möchten Sie sicherstellen, dass ausreichend Patchkabel im Labor vorhanden sind. Bei der Erfassung des aktuellen Lagerbestands möchten Sie ein LLM unterstütztes IT-System verwenden.
Der vereinfachte Lagerbestand umfasst blaue und rote Patchkabel mit einer Länge von jeweils 1 m.

## Voraussetzungen

- Python 3.11 oder höher
- Antropic API Key, Modell z. B. sonnet 4
- Alternativer API-Provider - Ollama 0.13.3, Modell z. B. qwen2.5-coder:3b

## Vorbereitende Aufgaben

### Schritt 1: Python Installation überprüfen

1. Öffnen Sie die **Eingabeaufforderung** (cmd) oder **PowerShell**
2. Überprüfen Sie, ob Python installiert ist:

```cmd
python --version
```

**Erwartete Ausgabe:** `Python 3.11.x` oder höher

>  **Falls Python nicht installiert ist:**
> - Laden Sie Python von https://www.python.org/downloads/ herunter
> - Installieren Sie Python und aktivieren Sie "Add Python to PATH"

---

### Schritt 2: Projektordner erstellen (je API-Provider)

1a. Erstellen Sie einen neuen Ordner für das Projekt (Anthropic):

```cmd
mkdir C:\MCP-Demo_Antropic
cd C:\MCP-Demo_Antropic
```

1b. Erstellen Sie einen neuen Ordner für das Projekt (Ollama):

```cmd
mkdir C:\MCP-Demo_Ollama
cd C:\MCP-Demo_Ollama
```

2. Kopieren Sie alle 5 Dateien bzw. 4 Dateien (Ollama) in den entsprechenden lokalen Ordner [siehe code in diesem Kapitel:](../11-intro-to-mcp/code/)
   - `einfacher_api_call.py`
   - `mcp_client.py`
   - `mcp_server.py`
   - `requirements.txt`
   - `.env.example` (nur Anthropic)

---

### Schritt 3a: API-Schlüssel bei einem API-Provider besorgen (hier am Beispiel Anthrophic)

1. Besuchen Sie https://console.anthropic.com/
2. Melden Sie sich an oder erstellen Sie ein Konto
3. Navigieren Sie zu **API Keys**
4. Klicken Sie auf **Create Key**
5. Kopieren Sie den API-Schlüssel (er beginnt mit `sk-ant-...`)

> **Wichtig:** Claude-API wird als seperates Produkt angeboten. Es enstehen daher Kosten. 
> Bewahren Sie Ihren API-Schlüssel sicher auf!

---
### Alternativer Schritt 3b: Inbetriebnahme eines lokalen API-Providers mit Modell
#### Ollama Version prüfen

```cmd
ollama --version
```

**Erwartete Ausgabe z. B.:** `ollama version is 0.13.3`

#### Modell überprüfen

```cmd
ollama list
```

**Erwartete Ausgabe:** Sie sollten `qwen2.5-coder:3b` in der Liste sehen

> **Falls das Modell nicht installiert ist:**
> ```cmd
> ollama pull qwen2.5-coder:3b
> ```

#### Ollama starten (falls nicht läuft)

**Option 1 - Hintergrund-Dienst (empfohlen):**
Ollama läuft normalerweise automatisch als Dienst. Prüfen Sie in der Taskleiste ob das Ollama-Icon vorhanden ist.

**Option 2 - Manuell starten:**python 
```cmd
ollama serve
```
**Hinweis:** Die Fehlermeldung, "Error: listen tcp 127.0.0.1:11434: bind: Normalerweise darf jede Socketadresse (Protokoll, Netzwerkadresse oder Anschluss) nur jeweils einmal verwendet werden, weißt darauf hin, das der Port 11434 bereits von einem anderen Ollama-Prozess belegt ist. Es läuft wahrscheinlich schon eine Instanz von Ollama im Hintergrund.

**Überprüfung mit:**
```cmd
tasklist | findstr ollama
```

> **Wichtig:** Lassen Sie dieses Fenster geöffnet, wenn Sie manuell starten!

#### Test: Ollama funktioniert

Öffnen Sie ein **neues** cmd-Fenster und testen Sie:

```cmd
ollama run qwen2.5-coder:3b
```

**Erwartete Ausgabe:** Das Modell sollte antworten (z.B. "Hallo! Wie kann ich helfen?")

Beenden Sie den Test mit `/bye`



### Schritt 4: .env Datei erstellen (mit Ollama nicht erforlderlich)

1. Öffnen Sie den Editor (z.B. Notepad):

```cmd
notepad .env
```

2. Fügen Sie folgende Zeile ein (ersetzen Sie `your-api-key-here` mit Ihrem echten API-Schlüssel):

```
ANTHROPIC_API_KEY=sk-ant-api03-...
```

3. Speichern Sie die Datei als `.env` (wichtig: ohne `.txt` Endung!)

>**Tipp:** In Windows Explorer müssen Sie möglicherweise "Dateinamenerweiterungen" aktivieren,
> um sicherzustellen, dass die Datei als `.env` und nicht als `.env.txt` gespeichert wird.

---

### Schritt 5: Virtuelle Umgebung erstellen (je API-Provider, also eine für Antropic und eine für Ollama)

1. Erstellen Sie eine virtuelle Umgebung:

```cmd
python -m venv venv
```

>**Tipp:** Wenn bestimmte Python-Versionen erforderlich sind, dann ist eine Anpassung erforderlich. (z. B. die Benennung der Version aus den vorhandenen python-Versionen mit py -3.11 -m venv venv )

2. Aktivieren Sie die virtuelle Umgebung:

**In cmd (Eingabeaufforderung):**
```cmd
venv\Scripts\activate.bat
```

**In PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**Erfolg:** Ihr Prompt sollte nun mit `(venv)` beginnen:
```
(venv) C:\MCP-Demo>
```
---

### Schritt 6: Bibliotheken installieren

1. Installieren Sie alle benötigten Bibliotheken:

```cmd
pip install -r requirements.txt
```

**Erwartete Ausgabe:**
```
Successfully installed anthropic-... mcp-... python-dotenv-...
```

2. Überprüfen Sie die Installation:

```cmd
pip list
```

Mit Anthropic sollten Sie sehen:
- `anthropic`
- `mcp`
- `python-dotenv`


Mit Ollama sollten Sie sehen:
- `ollama`
- `mcp`

---

# Lab 01: Einfacher API-Call an ein LLM (ohne MCP)

**Hinweis** Je nach API-Provider lokal mit Ollama und einem lokalen Modell oder entfernt mit z. B. Anthropic als Provider und einem verfügbaren Sprachmodell z. B. Claude Sonnet

Testen Sie zunächst die einfache Anfrage an ein LLM
- Rufen Sie das Skript "einfacher_api_call.py" auf
- Stellen Sie Ihre Frage zum Lagerbestand.

```cmd
python einfacher_api_call.py
```

# Lab 02: Abfrage des Lagerbestands an LLM mit MCP-Tool

Ohne Kontextbereitstellung wird ein LLM bei der Bestandsabfrage nach Patchkabel keine hilfreiche Antwort geben oder halluzinieren.
Ein MCP (Model Context Protocol) System zur Abfrage des Patchkabel-Lagerbestands mit natürlicher Sprache kann den benötigten Kontext liefern.


```cmd
python mcp_client.py
```

**Erwartete Ausgabe:**
```
MCP Patchkabel-Lagerbestand Client gestartet
1 Tool verfügbar:
   - patchkabel_bestand_abfragen: Fragt den aktuellen Lagerbestand von Patchkabeln ab...

============================================================

Ihre Anfrage (oder 'exit' zum Beenden):
```

## Aufräumen

Wenn Sie fertig sind, deaktivieren Sie die virtuelle Umgebung:

```cmd
deactivate
```

Ihr Prompt sollte wieder normal aussehen (ohne `(venv)`).

---

## Weitere mögliche Lernaufgaben

- Experimentieren Sie mit verschiedenen Fragen an das System
- Erweitern Sie den Lagerbestand
- Fügen Sie weitere MCP-Tools hinzu

---

## Zusätzliche Ressourcen

- **Anthropic API Dokumentation:** https://docs.anthropic.com/
- **Model Context Protocol:** https://modelcontextprotocol.io/
- **Python Virtual Environments:** https://docs.python.org/3/library/venv.html
- **Ollama:** https://ollama.com/
---

## Autoren und Urheberrecht
- Created by: Michael Lotter
- Date: 12/2025
- Version: v1.0

![line](../../images/banner.png)
<p align="center">
<a href="../11-intro-to-mcp/00.md"><img src="../../images/previous.png" width="150px"></a>
<a href="../11-intro-to-mcp/02_tool.md"><img src="../../images/next.png" width="150px"></a>
</p>