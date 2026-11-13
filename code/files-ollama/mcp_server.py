#!/usr/bin/env python3
"""
MCP Server für Patchkabel-Lagerbestand
Stellt 1 Tool bereit: Bestand abfragen
Benötigt: mcp 2.x (siehe requirements.txt)
"""
import asyncio
from mcp.server import Server
from mcp.types import Tool, TextContent, ListToolsResult, CallToolResult
from mcp.server.stdio import stdio_server

# Hardcodierter Lagerbestand
LAGER_BESTAND = {
    "blau_1m": 45,
    "rot_1m": 32
}


# =============================================================================
# TOOL: PATCHKABEL BESTAND ABFRAGEN
# =============================================================================

# MCP Tool-Beschreibung
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

# Beispiel-Argumente:
# {"farbe": "blau"}
# {"farbe": "rot"}
# {"farbe": "gesamt"}

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


# =============================================================================
# MCP SERVER SETUP
# =============================================================================

async def list_tools(ctx, params) -> ListToolsResult:
    """
    Gibt die Liste aller verfügbaren Tools zurück.
    Diese Funktion wird vom MCP Client aufgerufen (tools/list).
    """
    return ListToolsResult(tools=[TOOL_DESCRIPTION])


async def call_tool(ctx, params) -> CallToolResult:
    """
    Verarbeitet Tool-Aufrufe vom MCP Client (tools/call).
    Ruft die entsprechende Tool-Funktion basierend auf dem Namen auf.

    Args:
        params.name: Name des aufzurufenden Tools
        params.arguments: Dictionary mit den Tool-Argumenten

    Returns:
        CallToolResult mit TextContent (MCP Response)
    """
    name = params.name
    arguments = params.arguments or {}

    if name == "patchkabel_bestand_abfragen":
        result = patchkabel_bestand_abfragen(
            farbe=arguments["farbe"]
        )
        return CallToolResult(content=[TextContent(type="text", text=result)])

    else:
        raise ValueError(f"Unbekanntes Tool: {name}")


# Server-Instanz erstellen und die beiden Funktionen als Handler registrieren
server = Server(
    "patchkabel-lager-server",
    version="1.0.0",
    on_list_tools=list_tools,
    on_call_tool=call_tool,
)


async def main():
    """Server über stdio starten"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
