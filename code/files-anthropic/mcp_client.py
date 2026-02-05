#!/usr/bin/env python3
"""
MCP Client mit natürlicher Spracheingabe
Nutzt Claude API und verbindet sich mit dem MCP Server
"""
import asyncio
import json
import os
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

async def main():
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
    
    # Verbindung zum MCP Server aufbauen
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Server initialisieren
            await session.initialize()
            
            # Verfügbare Tools abrufen
            tools_result = await session.list_tools()
            available_tools = tools_result.tools
            
            print(" MCP Patchkabel-Lagerbestand Client gestartet")
            print(f" {len(available_tools)} Tool verfügbar:")
            for tool in available_tools:
                print(f"   - {tool.name}: {tool.description}")
            print("\n" + "="*60)
            
            # Hauptschleife für Benutzereingaben
            while True:
                user_input = input("\n Ihre Anfrage (oder 'exit' zum Beenden): ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'beenden']:
                    print(" Auf Wiedersehen!")
                    break
                
                if not user_input:
                    continue
                
                # Tools für Claude vorbereiten
                claude_tools = []
                for tool in available_tools:
                    claude_tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    })
                
                # Anfrage an Claude senden
                print("\n Verarbeite Anfrage...")
                messages = [{"role": "user", "content": user_input}]
                
                # Erste Anfrage an Claude
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1000,
                    tools=claude_tools,
                    messages=messages
                )
                
                # Tool-Aufrufe verarbeiten
                while response.stop_reason == "tool_use":
                    # Tool-Aufrufe aus der Antwort extrahieren
                    tool_results = []
                    
                    for block in response.content:
                        if block.type == "tool_use":
                            tool_name = block.name
                            tool_args = block.input
                            
                            print(f" Führe Tool aus: {tool_name}")
                            print(f"   Parameter: {json.dumps(tool_args, ensure_ascii=False)}")
                            
                            # Tool auf dem MCP Server aufrufen
                            result = await session.call_tool(tool_name, tool_args)
                            
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result.content[0].text
                            })
                    
                    # Konversation mit Tool-Ergebnissen fortsetzen
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({"role": "user", "content": tool_results})
                    
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=1000,
                        tools=claude_tools,
                        messages=messages
                    )
                
                # Finale Antwort ausgeben
                print("\n Antwort:")
                for block in response.content:
                    if hasattr(block, "text"):
                        print(f"   {block.text}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n Fehler: {e}\n")
