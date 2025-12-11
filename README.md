# AltBlocker 🔒

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![Version](https://img.shields.io/badge/version-v0.3.0-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

En lille, kraftfuld utility til Windows, der blokerer venstre Alt-tasten. Perfekt hvis utilsigtede Alt-tryk er et problem, og du vil have ro i workflowet.

---

## Features

- **Blokerer venstre Alt fra start** - Alt-tasten er deaktiveret som standard
- **System tray integration** med rød/grøn statusikon
- **Live status tooltip** - "Alt blokeret" eller "Alt aktiv"
- **Config-fil (JSON)** der husker indstillinger mellem sessioner
- **Start med Windows** via Task Scheduler (kræver admin)
- **Start minimeret til tray** styret af flueben
- **Moderne dark theme UI** - elegant og brugervenlig grænseflade
- **Semantisk versionering** indlejret i exe via PyInstaller

---

## Installation

1. Download den seneste `.exe` fra [Releases](https://github.com/qitsuk/AltBlocker/releases)
2. Kør programmet (ingen installation nødvendig)
3. Første gang du aktiverer "Start med Windows", skal du køre som **administrator**

---

## Byg fra kildekode

### Prerequisites

- Python 3.12 eller nyere
- Windows 10/11

### Build steps

```bash
# Klon repo
git clone https://github.com/<dit-brugernavn>/AltBlocker.git
cd AltBlocker

# Opret Virtuelt Python Miljø
python -m venv {virtual env name}

# Aktiver det virtuelle miljø
# Windows:
# - Powershell:
  .\{virtual env name}\Scripts\Activate.ps1

# - Commandline:
  .\{virtual env name}\Scripts\activate.bat

# Linux:
  source {virtual env name}/bin/activate

# Installer dependencies
pip install -r requirements.txt

# Byg exe med PyInstaller
pyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." --name "AltBlocker" --version-file version.txt main.py
```

Din `.exe` vil være tilgængelig i `dist/` mappen.

---

## Konfiguration

### Filplacering
`alt_blocker_config.json` gemmes automatisk i samme mappe som programmet.

### Felter

```json
{
  "start_with_windows": false,
  "start_minimized": false
}
```

- **`start_with_windows`** - Opretter/sletter Task Scheduler-opgaven
- **`start_minimized`** - Starter minimeret i systembakken

**Tip:** Hvis du ændrer config manuelt, skal det være gyldig JSON (brug `true`/`false`, ingen kommentarer).

---

## Admin-krav

"Start med Windows" kræver administratorrettigheder for at oprette en Task Scheduler-opgave.

- Hvis appen ikke kører som admin, deaktiveres checkboksen automatisk
- Tooltip vises: *"Kræver administratorrettigheder. Start programmet som admin for at aktivere."*

---

## Dependencies

```
keyboard
pystray
Pillow
```

Se `requirements.txt` for specifikke versioner.

---

## Semantisk versionering

Vi følger [SemVer](https://semver.org/):

- **MAJOR** - Inkompatible ændringer
- **MINOR** - Nye funktioner (bagudkompatible)
- **PATCH** - Bugfixes

**Aktuel version:** `v0.3.0`

---

## Releases

Se seneste builds under [GitHub Releases](https://github.com/<dit-brugernavn>/AltBlocker/releases)

---

## Hvordan virker det?

1. **Blokering** - Bruger `keyboard`-biblioteket til at intercepte og blokere Alt-tasten
2. **System tray** - `pystray` håndterer tray-ikonet med live statusopdateringer
3. **Autostart** - Windows Task Scheduler bruges til at starte programmet ved login
4. **Persistence** - JSON config-fil sikrer indstillinger huskes mellem sessioner

---

## Troubleshooting

### Alt-tasten blokeres ikke
- Kør programmet som administrator
- Tjek at "Alt blokeret" vises i GUI'en
- Genstart programmet

### "Start med Windows" virker ikke
- Højreklik på `.exe` og vælg "Kør som administrator"
- Aktiver checkboksen igen
- Verificer Task Scheduler-opgaven i Windows Task Scheduler

### Config-fil findes ikke
- Programmet opretter automatisk filen ved første kørsel
- Hvis den slettes, genoprettes den med standardværdier

---

## License

MIT License - se [LICENSE](LICENSE) for detaljer.

---

## Bidrag

Pull requests er velkomne! For større ændringer, åbn venligst et issue først for at diskutere hvad du gerne vil ændre.

---

## Kontakt

Har du spørgsmål eller forslag? Opret et [issue](https://github.com/<dit-brugernavn>/AltBlocker/issues) på GitHub.

---

**Lavet med ❤️ til alle der er trætte af utilsigtede Alt-tryk**
