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
- Python Virtual Environment mit der Bibliothek `mcp` ab Version 2 (siehe `requirements.txt`)
- `mcp_server.py` im Projektordner für Ollama

### Vorbereitung
```powershell
# Prüfen: Node.js installiert
node --version
npx --version

# Prüfen: Projektordner existiert
Get-ChildItem C:\akademietag_2026\mcp_basics\mcp-demo_ollama
```

---

## Aufgaben

### Schritt 0: Projektordner öffnen und venv aktivieren

**Aktion (PowerShell):**
```powershell
cd C:\akademietag_2026\mcp_basics\mcp-demo_ollama
.\venv\Scripts\Activate.ps1
```

**Erwartetes Ergebnis:**
- Prompt zeigt `(venv)` am Anfang
- Sie befinden sich im Projektordner

**Prüfung:**
```powershell
Get-ChildItem
# Sollte zeigen: mcp_server.py, mcp_client_ollama.py, venv\
```

---

### Schritt 1: MCP Inspector starten
Die MCP-Server-Datei `mcp_server.py` wird dem Inspector als Argument übergeben. Der Inspector startet den Server als eigenen Prozess und kommuniziert mit ihm über stdio – genau wie der MCP-Client.

**Aktion (PowerShell):**
```powershell
npx @modelcontextprotocol/inspector .\venv\Scripts\python.exe mcp_server.py
```

Beim ersten Start fragt `npx`, ob das Paket installiert werden soll. Bestätigen Sie mit `y`.

**Im Terminal erscheint** eine Meldung, dass der Inspector läuft, mit einer Adresse wie:
```
MCP Inspector is up and running at http://localhost:6274/?MCP_PROXY_AUTH_TOKEN=...
```

**Automatisch öffnet sich:**
- Ihr Standard-Browser mit dieser Adresse
- das MCP Inspector Interface

> **Hinweis:** Öffnet sich der Browser nicht, kopieren Sie die vollständige Adresse aus dem Terminal (inklusive Token) in den Browser. Die Portnummer kann je nach Inspector-Version abweichen.

Lassen Sie das Terminal-Fenster geöffnet, solange Sie mit dem Inspector arbeiten.

---

### Schritt 2: Verbindung zum Server herstellen

**Aktion:**
1. Prüfen Sie links: **Transport Type** steht auf **STDIO**, bei **Command** und **Arguments** ist Ihr Aufruf aus Schritt 1 eingetragen.
2. Klick auf **[Connect]**

**Erwartetes Ergebnis:**
- Links erscheint der Status **Connected**
- Oben werden Server-Name und Version angezeigt: `patchkabel-lager-server` (Version `1.0.0`)

> **Hinweis:** Der Server selbst gibt im Terminal keine Meldungen aus. Er kommuniziert ausschließlich über stdio mit dem Inspector.

---

### Schritt 3: History öffnen und Initialisierung betrachten

**Aktion:**
1. Öffnen Sie den Bereich **History** (unten im Inspector)
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
└─────────────────────────────────────────────────────────┘
```

Der Eintrag **tools/list** kommt erst hinzu, wenn Sie die Tools abfragen (Schritt 6).

---

### Schritt 4: Initialize Request analysieren

**Aktion:**
1. Klick auf den Eintrag **initialize** (zum Aufklappen)
2. Klick auf **Request**

**Sie sehen (JSON, gekürzt):**
```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-06-18",
    "capabilities": { ... },
    "clientInfo": {
      "name": "mcp-inspector",
      "version": "..."
    }
  }
}
```

> **Hinweis:** `protocolVersion`, `id`, die `capabilities` und die Versionsnummer des Inspectors hängen von der eingesetzten Inspector-Version ab und können bei Ihnen abweichen.

---

### Schritt 5: Initialize Response analysieren

**Aktion:**
1. Klick auf **Response** unter initialize

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "result": {
    "protocolVersion": "2025-06-18",
    "capabilities": {
      "tools": {
        "listChanged": false
      }
    },
    "serverInfo": {
      "name": "patchkabel-lager-server",
      "version": "1.0.0"
    }
  }
}
```

**Beobachten Sie:**
- `serverInfo.name` und `serverInfo.version` stammen aus `mcp_server.py`: `Server("patchkabel-lager-server", version="1.0.0", ...)`
- `capabilities.tools` zeigt dem Client: Dieser Server bietet Tools an.
- Der Server übernimmt die vom Client angefragte `protocolVersion`, sofern er sie unterstützt.

---

### Schritt 6: tools/list Request analysieren

**Aktion:**
1. Klick auf den Reiter **Tools** (oben)
2. Klick auf **[List Tools]**
3. Zurück in die **History**: Klick auf den neuen Eintrag **tools/list**
4. Klick auf **Request**

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

---

### Schritt 7: tools/list Response analysieren - Teil 1 (Struktur)

**Aktion:**
1. Klick auf **Response** unter tools/list

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
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

Die Reihenfolge der Felder kann in der Anzeige abweichen, der Inhalt ist derselbe.

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

Vergleichen Sie mit `TOOL_DESCRIPTION` in `mcp_server.py`: Genau diese Beschreibung bekommt später auch das LLM zu sehen.

---

### Schritt 9: Tool im Tools-Reiter auswählen

**Aktion:**
1. Im Reiter **Tools** erscheint nach „List Tools“ die Liste der verfügbaren Tools
2. Klick auf **patchkabel_bestand_abfragen**

Rechts erscheinen Beschreibung und Eingabefeld für den Parameter **farbe**.

---

### Schritt 10: Tool ausführen - Blaue Kabel

**Aktion:**
1. Bei **farbe** wählen bzw. eintragen: **blau**
2. Klick auf **[Run Tool]**

**Erwartetes Ergebnis:**
- Unten erscheint der Ergebnisbereich
- Er zeigt die Antwort vom Server

**Angezeigtes Ergebnis:**
```json
{
  "content": [
    {
      "type": "text",
      "text": "Bestand blaue 1m Patchkabel: 45 Stück"
    }
  ],
  "isError": false
}
```

---

### Schritt 11: History - tools/call Request analysieren

**Aktion:**
1. Zurück zur **History**
2. Neuer Eintrag: **tools/call**
3. Klick auf den Eintrag **tools/call**
4. Klick auf **Request**

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
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
1. Klick auf **Response** unter tools/call

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Bestand blaue 1m Patchkabel: 45 Stück"
      }
    ],
    "isError": false
  }
}
```

**Beobachten Sie:**
- `params.name` und `params.arguments` aus dem Request sind genau die Werte, die der Handler `call_tool(ctx, params)` in `mcp_server.py` auswertet.
- `isError: false` zeigt an, dass das Tool fehlerfrei ausgeführt wurde.

---

## Reflexionsfragen

- Warum sieht man im Inspector keine HTTP-Requests zu Ollama?

- Was ist der Unterschied zwischen einem tools/list und tools/call?

- Könnte das LLM die Tool-Implementierung "hacken" oder ändern?

- Was würde passieren, wenn Sie in mcp_server.py den LAGER_BESTAND ändern?

- Warum ist die Trennung zwischen Tool-Beschreibung und -Implementierung wichtig?

---

## Fehlerbehebung

- *Connect schlägt fehl:* Prüfen Sie, ob der Server allein startet: `python mcp_server.py` (läuft er ohne Meldung, ist er in Ordnung, Beenden mit Strg+C). Bricht er ab, passt meist die `mcp`-Version nicht zur Datei: `pip show mcp` muss Version 2.x zeigen.
- *Browser zeigt Fehler zur Authentifizierung:* Die Adresse muss den Token aus dem Terminal enthalten (`?MCP_PROXY_AUTH_TOKEN=...`).

---

## Autoren und Urheberrecht
- Created by: Michael Lotter
- Date: 12/2025, aktualisiert 11/2026 (mcp 2.x, aktueller Inspector, Windows-Befehle)
- Version: v1.1

![line](images/banner.png)
<p align="center">
<a href="04_client_llm.md"><img src="images/previous.png" width="150px"></a>
</p>
