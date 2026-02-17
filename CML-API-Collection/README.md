# Cisco Modeling Lab API - Bruno Collection

Eine vollständige Bruno Collection für die Cisco Modeling Lab (CML) REST API.

## Voraussetzungen

- [Bruno](https://www.usebruno.com/) installiert
- Zugang zu einem CML Server
- Gültige Zugangsdaten (Username/Password)

## Installation

1. Bruno öffnen
2. "Open Collection" wählen
3. Diesen Ordner (`CML-API-Collection`) auswählen
4. Die Collection wird geladen

## Konfiguration

### Environment-Variablen einrichten

Öffne die Environment-Datei unter `environments/Local.bru` und passe folgende Werte an:

```
vars {
  base_url: https://your-cml-server.com
  username: admin
  password: your-password
  token: 
}
```

- **base_url**: Die URL deines CML Servers (ohne abschließenden Slash)
- **username**: Dein CML Benutzername
- **password**: Dein CML Passwort
- **token**: Wird automatisch nach der Authentifizierung gesetzt

## Nutzung

### 1. Authentifizierung

Führe zuerst den Request `1-Authentication/Authenticate` aus. Der JWT Token wird automatisch in der Environment-Variable `token` gespeichert und für alle nachfolgenden Requests verwendet.

### 2. Collection-Struktur

Die Collection ist in folgende Bereiche unterteilt:

- **1-Authentication**: Authentifizierung und Token-Verwaltung
- **2-Labs**: Lab-Management (Create, Read, Update, Delete, Start, Stop, etc.)
- **3-Nodes**: Node-Management (Create, Read, Update, Delete, Start, Stop)
- **4-Links**: Link-Management zwischen Nodes
- **5-Interfaces**: Interface-Management
- **6-System**: System-Informationen und Diagnostics
- **7-Images**: Node- und Image-Definitionen
- **8-Users-Groups**: Benutzer- und Gruppenverwaltung

### 3. Typischer Workflow

1. **Authentifizierung**: `Authenticate` ausführen
2. **Lab erstellen**: `Create Lab` - die Lab ID wird automatisch gespeichert
3. **Nodes erstellen**: `Create Node` - die Node ID wird automatisch gespeichert
4. **Interfaces erstellen**: `Create Interface` für die Nodes
5. **Links erstellen**: `Create Link` zwischen Interfaces
6. **Lab starten**: `Start Lab`
7. **Lab stoppen**: `Stop Lab`
8. **Lab löschen**: `Delete Lab`

### 4. Variablen

Die Collection nutzt folgende Variablen, die automatisch gesetzt werden:

- `lab_id`: ID des zuletzt erstellten Labs
- `node_id`: ID des zuletzt erstellten Nodes
- `interface_id`: ID des zuletzt erstellten Interfaces
- `link_id`: ID des zuletzt erstellten Links

Diese Variablen werden in nachfolgenden Requests automatisch verwendet, können aber auch manuell überschrieben werden.

## API-Dokumentation

Die vollständige API-Dokumentation findest du auf deinem CML Server unter:

```
https://your-cml-server.com/api/v0/ui/
```

Oder im Browser unter: `Help > API Documentation`

## Verfügbare Node-Typen

Gängige Node-Definitionen:
- `iosv` - Cisco IOSv (Router)
- `iosxrv` - Cisco IOS XRv (Router)
- `iosxrv9000` - Cisco IOS XRv 9000 (Router)
- `nxosv` - Cisco NX-OSv (Switch)
- `asav` - Cisco ASAv (Firewall)
- `csr1000v` - Cisco CSR 1000v (Router)
- `server` - Generic Server
- `ubuntu` - Ubuntu Linux
- `alpine` - Alpine Linux
- `unmanaged_switch` - Unmanaged Switch
- `external_connector` - External Network Connector

Eine vollständige Liste erhältst du über: `7-Images/Get Node Definitions`

## Troubleshooting

### Token abgelaufen

Wenn du einen 401 Unauthorized Error erhältst, führe erneut `Authenticate` aus, um einen neuen Token zu erhalten.

### HTTPS Zertifikats-Fehler

Falls dein CML Server ein selbstsigniertes Zertifikat verwendet, musst du in Bruno die SSL-Verifizierung deaktivieren:
- Settings → SSL Verification → Disable

### Lab lässt sich nicht löschen

Stelle sicher, dass das Lab gestoppt ist (`Stop Lab`) bevor du es löschst.

## Weitere Informationen

- [Cisco Modeling Labs Documentation](https://developer.cisco.com/docs/modeling-labs/)
- [CML Python Client](https://developer.cisco.com/docs/virl2-client/)
- [Bruno Documentation](https://docs.usebruno.com/)

## Support

Bei Fragen oder Problemen:
- Cisco DevNet Community
- CML Support Channel
- GitHub Issues

## Version

Diese Collection ist kompatibel mit Cisco Modeling Labs 2.7+
