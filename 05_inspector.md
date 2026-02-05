# Laborübung 2: Analyse der MCP-Kommunikation mit dem Inspector

![line](images/banner.png)

## Lernziele

Nach Abschluss dieser Laborübung können Sie:

- Den MCP Inspector installieren und starten
- Eine Verbindung zwischen Inspector und MCP Server herstellen
- Die MCP-Initialisierung analysieren und den Server-Namen identifizieren
- Verfügbare Tools mit vollständigem Schema auflisten (tools/list)
- Tool-Aufrufe durchführen und die Request-Response-Struktur verstehen (tools/call)
- Die Unterschiede zwischen Tool-Beschreibung (für LLM) und Tool-Implementierung (im Server) erkennen
- Die MCP-Communication-History interpretieren

---

## Voraussetzungen

### Software
- Node.js installiert (für npx)
- Python Virtual Environment mit `mcp` Bibliothek
- `mcp_server.py` im Projektordner für Ollama

### Vorbereitung
```bash
# Prüfen: Node.js installiert
node --version
npx --version

# Prüfen: Projektordner existiert
ls -la /pfad/zu/mcp-demo_ollama
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
ls -la
# Sollte zeigen: mcp_server.py, mcp_client_ollama.py, venv/
```

---

### Schritt 1: MCP Inspector starten

**Aktion:**
```bash
npx @modelcontextprotocol/inspector ./venv/bin/python3 mcp_server.py
```

**Alternative (falls python3 nicht funktioniert):**
```bash
npx @modelcontextprotocol/inspector python3 mcp_server.py
```

**Automatisch öffnet sich:**
- Ihr Standard-Browser
- URL: `http://localhost:5173`
- MCP Inspector Interface

---

### Schritt 2: Verbindung zum Server herstellen

**Aktion:**
1. Klick auf **[Connect]** Button

**Im Terminal sehen Sie:**
```
MCP Server initialized
Client connected
```
---

### Schritt 3: History-Tab öffnen und Initialisierung betrachten

**Aktion:**
1. Klick auf **"History"** Tab (falls nicht schon aktiv)
2. Suchen Sie den ersten Eintrag: **initialize**

**Sie sehen:**
```
┌─────────────────────────────────────────────────────────┐
│  History                                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ▼ initialize                                           │
│    Request                                              │
│    Response                                             │
│                                                         │
│  ▼ tools/list                                           │
│    Request                                              │
│    Response                                             │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

### Schritt 4: Initialize Request analysieren

**Aktion:**
1. Klick auf **"initialize"** Eintrag (zum Aufklappen)
2. Klick auf **"Request"**

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "roots": {
        "listChanged": true
      }
    },
    "clientInfo": {
      "name": "mcp-inspector",
      "version": "0.1.0"
    }
  }
}

---

### Schritt 5: Initialize Response analysieren

**Aktion:**
1. Klick auf **"Response"** unter initialize

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "patchkabel-lager-server",
      "version": "1.0.0"
    }
  }
}
```
---

### Schritt 6: tools/list Request analysieren

**Aktion:**
1. In History: Klick auf **"tools/list"** Eintrag
2. Klick auf **"Request"**

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list"
}
```

---

### Schritt 7: tools/list Response analysieren - Teil 1 (Struktur)

**Aktion:**
1. Klick auf **"Response"** unter tools/list

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {
        "name": "patchkabel_bestand_abfragen",
        "description": "Fragt den aktuellen Lagerbestand von Patchkabeln ab. Zeigt Bestände von blauen und roten 1m Patchkabeln sowie den Gesamtbestand an.",
        "inputSchema": {
          "type": "object",
          "properties": {
            "farbe": {
              "type": "string",
              "description": "Die Farbe des Patchkabels (blau, rot, oder gesamt für alle)",
              "enum": ["blau", "rot", "gesamt"]
            }
          },
          "required": ["farbe"]
        }
      }
    ]
  }
}
```
---

### Schritt 8: tools/list Response analysieren - Teil 2 (InputSchema)

**Fokussieren Sie auf den inputSchema-Teil:**

```json
"inputSchema": {
  "type": "object",
  "properties": {
    "farbe": {
      "type": "string",
      "description": "Die Farbe des Patchkabels...",
      "enum": ["blau", "rot", "gesamt"]
    }
  },
  "required": ["farbe"]
}
```

---

### Schritt 09: Tools-Tab öffnen und Tool ausführen

**Aktion:**
1. Klick auf **"Tools"** Tab (oben)
2. Sie sehen eine Liste verfügbarer Tools
3. Klick auf **"patchkabel_bestand_abfragen"**


---

### Schritt 10: Tool ausführen - Blaue Kabel

**Aktion:**
1. Im Dropdown **"farbe"** wählen: **blau**
2. Klick auf **[Execute]** Button

**Erwartetes Ergebnis:**
- Unten erscheint Result-Bereich
- Zeigt Antwort vom Server

**Result angezeigt:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Bestand blaue 1m Patchkabel: 45 Stück"
    }
  ]
}
```

---

### Schritt 11: History - tools/call Request analysieren

**Aktion:**
1. Zurück zum **"History"** Tab
2. Neuer Eintrag sollte erschienen sein: **tools/call**
3. Klick auf **"tools/call"** Eintrag
4. Klick auf **"Request"**

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "patchkabel_bestand_abfragen",
    "arguments": {
      "farbe": "blau"
    }
  }
}
```

---

### Schritt 12: tools/call Response analysieren

**Aktion:**
1. Klick auf **"Response"** unter tools/call

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Bestand blaue 1m Patchkabel: 45 Stück"
      }
    ]
  }
}
```

---

## Reflexionsfragen

- Warum sieht man im Inspector keine HTTP-Requests zu Ollama?

- Was ist der Unterschied zwischen einem tools/list und tools/call?**
   
- Könnte das LLM die Tool-Implementierung "hacken" oder ändern?
   
- Was würde passieren, wenn Sie in mcp_server.py den LAGER_BESTAND ändern?**
   
- Warum ist die Trennung zwischen Tool-Beschreibung und -Implementierung wichtig?**

---

## Autoren und Urheberrecht
- Created by: Michael Lotter
- Date: 12/2025
- Version: v1.0

![line](images/banner.png)
<p align="center">
<a href="04_client_llm.md"><img src="images/previous.png" width="150px"></a>
</p>
