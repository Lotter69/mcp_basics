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

**Im Terminal erscheint** eine Meldung mit der Adresse des Inspectors (`http://localhost:…`).

**Automatisch öffnet sich:**
- Ihr Standard-Browser mit dieser Adresse
- das MCP Inspector Interface

> **Hinweis:** Öffnet sich der Browser nicht, kopieren Sie die vollständige Adresse aus dem Terminal in den Browser (gegebenenfalls inklusive Token). Ist die venv aktiviert, funktioniert auch der kürzere Aufruf `npx @modelcontextprotocol/inspector python mcp_server.py`.

Lassen Sie das Terminal-Fenster geöffnet, solange Sie mit dem Inspector arbeiten.

---

### Schritt 2: Verbindung zum Server herstellen

Im Inspector sehen Sie unter **Servers** eine Karte für Ihren Server. Sie trägt den Namen des Startbefehls (**python**), den Typ **STDIO – Standard I/O** und den Befehl `python mcp_server.py`. Der Status steht auf **Disconnected**.

> Der graue Hinweis **„Read-only session“** besagt nur, dass der Server direkt beim Start übergeben wurde und in der Oberfläche nicht dauerhaft gespeichert wird. Für die Übung spielt das keine Rolle.

**Aktion:**
1. Klick auf den **Schalter** rechts neben **Disconnected** in der Server-Karte

**Erwartetes Ergebnis:**
- Der Status wechselt auf **Connected**, oben rechts erscheint zusätzlich die Dauer des Verbindungsaufbaus (z. B. „Connected (882ms)“)
- Oben links steht jetzt der Name des Servers: **patchkabel-lager-server**
- In der Server-Karte erscheint die ausgehandelte Protokollversion, z. B. **MCP 2025-11-25**

> **Hinweis:** Der Server selbst gibt im Terminal keine Meldungen aus. Er kommuniziert ausschließlich über stdio mit dem Inspector. Eigene Ausgaben des Servers (z. B. Fehlermeldungen) zeigt der Reiter **Console** rechts.

---

### Schritt 3: Nachrichtenverlauf betrachten

Rechts im Reiter **Protocol** listet der Bereich **Messages** alle Nachrichten zwischen Inspector (Client) und Server auf. Mit der Sortierung oben (**Newest First**) können Sie auf die älteste Nachricht zuerst umstellen.

**Sie sehen drei Einträge, jeweils mit der Richtung CLIENT → SERVER:**

| Reihenfolge | Nachricht | Bedeutung |
|---|---|---|
| 1 | **initialize** | Client und Server stellen sich vor und einigen sich auf die Protokollversion |
| 2 | **notifications/initialized** | Client meldet: „Initialisierung abgeschlossen, bereit“ – eine Benachrichtigung ohne Antwort |
| 3 | **tools/list** | Client fragt die verfügbaren Tools ab – der Inspector erledigt das beim Verbinden automatisch |

Bei **initialize** und **tools/list** stehen rechts die Antwortzeit und **OK**: Der Server hat geantwortet. **notifications/initialized** hat keine Antwort, weil eine Benachrichtigung (Notification) keine erwartet.

> **Merke:** Die ersten beiden Nachrichten bilden die **Initialisierung** (Lebenszyklus der Verbindung), ab der dritten beginnt die eigentliche **Arbeit** mit den Fähigkeiten des Servers.

---

### Schritt 4: Initialize Request analysieren

**Aktion:**
1. Klappen Sie den Eintrag **initialize** auf (Pfeil-Symbol rechts im Eintrag)
2. Sehen Sie sich die Anfrage (Request) an

**Sie sehen (JSON, gekürzt):**
```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-11-25",
    "capabilities": { ... },
    "clientInfo": {
      "name": "...",
      "version": "..."
    }
  }
}
```

> **Hinweis:** `id`, `capabilities` und die Angaben in `clientInfo` hängen von der eingesetzten Inspector-Version ab und können bei Ihnen abweichen.

---

### Schritt 5: Initialize Response analysieren

**Aktion:**
1. Sehen Sie sich im aufgeklappten Eintrag **initialize** die Antwort (Response) an

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 0,
  "result": {
    "protocolVersion": "2025-11-25",
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
- `serverInfo.name` und `serverInfo.version` stammen aus `mcp_server.py`: `Server("patchkabel-lager-server", version="1.0.0", ...)`. Der Name erscheint auch oben links im Inspector.
- `capabilities.tools` zeigt dem Client: Dieser Server bietet Tools an.
- `protocolVersion` ist die ausgehandelte Version, die auch in der Server-Karte angezeigt wird.

---

### Schritt 6: tools/list Request analysieren

**Aktion:**
1. Klappen Sie den Eintrag **tools/list** auf
2. Sehen Sie sich die Anfrage an

**Sie sehen (JSON):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

Je nach Inspector-Version steht zusätzlich ein leeres `"params": {}` darin.

---

### Schritt 7: tools/list Response analysieren - Teil 1 (Struktur)

**Aktion:**
1. Sehen Sie sich im aufgeklappten Eintrag **tools/list** die Antwort an

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

### Schritt 9: Tool im Reiter Tools auswählen

**Aktion:**
1. Klick oben in der Mitte auf den Reiter **Tools** (neben **Servers**)
2. Wählen Sie in der Liste **patchkabel_bestand_abfragen**

Es erscheinen die Beschreibung des Tools und ein Eingabefeld für den Parameter **farbe**.

---

### Schritt 10: Tool ausführen - Blaue Kabel

**Aktion:**
1. Bei **farbe** wählen bzw. eintragen: **blau**
2. Tool über die Schaltfläche zum Ausführen starten (z. B. **Run Tool**)

**Erwartetes Ergebnis:**
- Es erscheint das Ergebnis des Servers

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

### Schritt 11: tools/call Request analysieren

**Aktion:**
1. Rechts unter **Protocol → Messages** ist ein neuer Eintrag hinzugekommen: **tools/call**
2. Klappen Sie ihn auf und sehen Sie sich die Anfrage an

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
1. Sehen Sie sich im aufgeklappten Eintrag **tools/call** die Antwort an

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

- *Schalter springt nicht auf Connected:* Prüfen Sie, ob der Server allein startet: `python mcp_server.py` (läuft er ohne Meldung, ist er in Ordnung, Beenden mit Strg+C). Bricht er ab, passt meist die `mcp`-Version nicht zur Datei: `pip show mcp` muss Version 2.x zeigen.
- *Browser zeigt Fehler zur Authentifizierung:* Verwenden Sie die vollständige Adresse aus dem Terminal (gegebenenfalls inklusive Token).
- *Fehlermeldungen des Servers:* Reiter **Console** rechts neben **Protocol** öffnen.

---

## Autoren und Urheberrecht
- Created by: Michael Lotter
- Date: 12/2025, aktualisiert 11/2026 (mcp 2.x, aktueller Inspector, Windows-Befehle)
- Version: v1.1

![line](images/banner.png)
<p align="center">
<a href="04_client_llm.md"><img src="images/previous.png" width="150px"></a>
</p>
