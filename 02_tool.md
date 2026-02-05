# Sachwissen - Werkzeugkasten des MCP-Servers

![line](../../images/banner.png)


## Grundaufbau des verwendeten MCP-Servers

Jedes MCP Tool besteht aus drei Komponenten:

1. **MCP Tool-Beschreibung** - Definiert das Tool für den Client (MCP-Standard und funktional)
2. **Beispiel-Argumente** - Dokumentiert die möglichen Parameter eines Aufrufs (Entwickler-Kommentare und optional)
3. **Tool-Funktion** - Implementiert die Logik (MCP-Standard und funktional)

## Teil A - Der Werkzeugkasten/das Tool im Detail

### 1. MCP Tool-Beschreibung

```python
TOOL_DESCRIPTION = Tool(
    name="patchkabel_bestand_abfragen",
    description="Fragt den aktuellen Lagerbestand von Patchkabeln ab. Zeigt Bestände von blauen und roten 1m Patchkabeln sowie den Gesamtbestand an.",
    inputSchema={
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
)
```

#### Wichtige Elemente:

**`name`**: Eindeutiger Identifier des Tools
- Wird vom Client verwendet um das Tool aufzurufen
- Sollte beschreibend sein (z.B. `patchkabel_bestand_abfragen`)

**`description`**: Beschreibung für das LLM
- Erklärt dem LLM wann das Tool verwendet werden soll
- Sollte klar und detailliert sein
- LLM nutzt diese Info zur Entscheidung

**`inputSchema`**: JSON Schema für Parameter
- Standard JSON Schema Format
- Definiert welche Parameter das Tool erwartet

```python
inputSchema = {
    "type": "object",              # Hauptobjekt
    "properties": { ... },         # Liste aller Eigenschaften/Parameter
    "required": ["farbe"]          # Pflichtfelder, hier ist "Farbe" eine Pflichtangabe
}
```
Eigenschaften in der Liste
- `type`: Datentyp (string, number, integer, boolean, etc.), Farbe muss Text sein
- `description`: Erklärung des Parameters
- `enum`: Begrenzt erlaubte Werte (hier: nur blau, rot, gesamt)

### 2. Beispiel-Argumente

```python
# {"farbe": "blau"}
# {"farbe": "rot"}
# {"farbe": "gesamt"}
```

Diese Kommentare dokumentieren für den Entwickler:
- Wie das Tool aufgerufen werden kann
- Welche Werte erwartet werden

### 3. Tool-Funktion

```python
def patchkabel_bestand_abfragen(farbe: str) -> str:
    """
    Tool-Funktion: Fragt Patchkabel-Bestand ab
    
    Args:
        farbe: Die Farbe des abzufragenden Patchkabels (blau/rot/gesamt)
    
    Returns:
        Formatierter String mit dem Bestandsinformationen
    """
    if farbe == "blau":
        bestand = LAGER_BESTAND["blau_1m"]
        return f"Bestand blaue 1m Patchkabel: {bestand} Stück"
    
    elif farbe == "rot":
        bestand = LAGER_BESTAND["rot_1m"]
        return f"Bestand rote 1m Patchkabel: {bestand} Stück"
    
    elif farbe == "gesamt":
        blau = LAGER_BESTAND["blau_1m"]
        rot = LAGER_BESTAND["rot_1m"]
        gesamt = blau + rot
        return (f"Lagerbestand 1m Patchkabel:\n"
                f"  - Blau: {blau} Stück\n"
                f"  - Rot: {rot} Stück\n"
                f"  - Gesamt: {gesamt} Stück")
    
    else:
        return f"Unbekannte Farbe: {farbe}"
```

#### Besonderheiten:

- **Type Hints**: `farbe: str` → `str` für Klarheit, farbe muss ein string sein und die Funktion gibt einen string zurück
- **Docstring**: Beschreibt dem Entwickler was die Funktion macht. Das LLM verwertet die Tool-Beschreibung.
- **Funktion/Programmlogik**: Implementiert die eigentliche Funktionalität
- **Verschiedene Modi**: Unterstützt einzelne Farben und Gesamtansicht
- **Fehlerbehandlung**: `else` für ungültige Eingaben, obwohl MCP-inputSchema bereits ungültige Eingaben verhindert.

## Teil B - Das MCP-Server-Setup

## Genutzte MCP-Handler-Typen (hier *list_tools()* und *call_tool()* vom Typ Tool)

**Definition:** Handler sind Funktionen, die auf Anfragen warten und darauf reagieren.

weitere [Handler-Typen](https://modelcontextprotocol.io/specification/2025-11-25/server)

### list_tools()
**Bedeutung:** Wichtig für die Initialisierungsphase zwischen Client udn Server, damit dem Client bekannt ist was der Server anbietet.


```python
@server.list_tools() 
# -> Decorator: Ein Decorator ist eine Funktion, die eine andere Funktion einbettet. Registriert diese Funktion als Tool-Auflister

async def list_tools() -> list[Tool]:       #-> Diese Funktion ist asynchron. 
                                            # Während eine Funktion auf Daten wartet (z.B. Datenbank), kann der
                                            # Server andere Anfragen bearbeiten
                                            # Muss mit "await" aufgerufen werden
    """Gibt alle verfügbaren Tools zurück"""
    return [TOOL_DESCRIPTION]               # Hier ein Element einer Liste, können auch mehrere Elemente (Tools sein))
    # Ablauf
    # 1. Die Liste wird vom MCP-Server als JSON serialisiert
    # 2. Wird über STDIO (Standard Input/Output) an Client gesendet
    # 3. Client empfängt: {"tools": [{"name": "patchkabel_bestand_abfragen", ...}]}
    # 4. Client zeigt dem LLM: "Du kannst dieses Tool nutzen: ..."
```

Diese Funktion wird vom Client aufgerufen um zu erfahren welche Tools auf dem Server zur Verfügung gestellt werden.


### call_tool()
**Bedeutung:** Wichtig bei der Tool-Ausführung des Clients, nachdem das LLM Werkzeugauswahl vorgenommen und dem Client mitgeteilt hat.

```python
@server.call_tool()                                      # Registriert diese Funktion als Tool-Aufrufer
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Ruft das entsprechende Tool auf"""
    
    if name == "patchkabel_bestand_abfragen":           # Vergleich von geforderten Tool-Namen aus Client LLM-Kommunikation und vorhandenem Tool-Namen in Tool-Beschreibung des Servers
        result = patchkabel_bestand_abfragen(
            farbe=arguments["farbe"]
        )
        return [TextContent(type="text", text=result)]
    
    else:
        raise ValueError(f"Unbekanntes Tool: {name}")
```

**Ablauf:**
1. Der Handler des Servers empfängt: name="patchkabel_bestand_abfragen", arguments={"farbe": "blau"}
2. if name == "patchkabel_bestand_abfragen": → TRUE
3. result = patchkabel_bestand_abfragen(farbe="blau")
    → ruft die Tool-Funktion auf
    → result = "Bestand blaue 1m Patchkabel: 42 Stück"
4. return [TextContent(type="text", text="Bestand blaue 1m Patchkabel: 42 Stück")]
    → Gibt MCP-formatiertes Ergebnis zurück
5. MCP-Server sendet Antwort an Client
6. LLM erhält das Ergebnis
7. LLM antwortet User: "Ihr Lagerbestand zeigt 42 blaue 1m Patchkabel"

**Wichtige Ergänzungen:**
1. Die Funktion muss eine Liste zurückgeben: [TextContent(...)]
2. Bei mehreren Tools wären Bedingungen if/elif/else enthalten:

```python
if name == "tool1":
    ...
elif name == "tool2":
    ...
elif name == "tool3":
    ...
else:
    raise ValueError(...)
```

##  Datenfluss

```
1. Client ruft list_tools() auf
   → Server antwortet mit [TOOL_DESCRIPTION]

2. Benutzer stellt Frage
   → Client sendet an Claude API mit Tool-Definition

3. Claude entscheidet Tool zu nutzen
   → Claude gibt zurück: tool_use mit name="patchkabel_bestand_abfragen" 
                        und arguments={"farbe": "blau"}

4. Client ruft call_tool() auf
   → Server führt patchkabel_bestand_abfragen(farbe="blau") aus

5. Server gibt Ergebnis zurück
   → "Bestand blaue 1m Patchkabel: 45 Stück"

6. Client sendet Ergebnis an Claude
   → Claude formuliert finale Antwort für Benutzer
```

## Zusammenfassung

Ein MCP Tool besteht aus:

1. **Tool-Beschreibung** (JSON) - Was kann das Tool?
2. **Funktion** (Python) - Wie funktioniert es?
3. **MCP-Handler** (Server) - Womit soll der Server dienen?


## Autoren und Urheberrecht
- Created by: Michael Lotter
- Date: 12/2025
- Version: v1.0

![line](../../images/banner.png)
<p align="center">
<a href="../11-intro-to-mcp/01_lab.md"><img src="../../images/previous.png" width="150px"></a>
<a href="../11-intro-to-mcp/03_architecture.md"><img src="../../images/next.png" width="150px"></a>
</p>