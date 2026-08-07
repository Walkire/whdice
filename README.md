# ⚔️ Warhammer Combat Simulator

A desktop GUI tool for simulating Warhammer 40K combat scenarios. Configure attacker weapons and defender units, run Monte Carlo simulations (100,000 iterations), and view statistical outcomes: average hits, wounds, damage, kills, and unit wipe probability.

## Features

- **Modern CustomTkinter UI** with dark mode, sidebar navigation, and multiple pages
- **Comprehensive weapon configuration** including special rules (Torrent, Blast, Lethal Hits, Devastating Wounds, Sustained Hits, Melta)
- **Defender templates** — save and load common unit profiles for quick comparison
- **Weapon list management** with add, delete, duplicate, and reorder
- **Statistical graphs** — damage distribution and kill probability charts (requires matplotlib)
- **Summary statistics** — average, median, min, max for wounds/kills/damage
- **Auto-save** — state persists between sessions
- **Undo** — Ctrl+Z reverts the last action
- **Theme toggle** — switch between dark, light, and system modes

## Requirements

- Python 3.8+
- `customtkinter >= 5.2.0`
- `matplotlib >= 3.7.0` (optional, for graphs)

## Getting Started

```bash
# Install dependencies
pip install customtkinter matplotlib

# Run the application
python app.py
```

## Usage

1. **Attacker** — configure weapon stats and abilities, then "Save as Weapon"
2. **Defender** — set toughness, save, wounds, model count, and modifiers
3. **Weapons** — view and manage your saved weapon list
4. **Results** — run the simulation and see per-weapon breakdowns
5. **Graphs** — visualize damage/kill distributions
6. **Templates** — save/load defender profiles for batch comparison
7. **Settings** — toggle theme and adjust simulation count

## Testing

```bash
# Run unit tests
python -m unittest tests/test_sim_functions.py
```

## Project Structure

```
├── app.py                  # New CustomTkinter entry point
├── run.py                  # Legacy Tkinter entry point
├── simulation.py           # Core simulation loop
├── sim_functions.py        # Pure simulation math (unchanged)
├── enums.py                # Enums for reroll types, modifiers
├── utils.py                # Dice notation parsing, helpers
├── ui/
│   ├── sidebar.py          # Sidebar navigation
│   ├── page_manager.py     # Page show/hide logic
│   ├── stats.py            # Summary statistics computation
│   ├── styles.py           # Shared font, spacing, color constants
│   ├── pages/              # One file per page
│   └── widgets/            # Reusable widget components
├── state/
│   ├── app_state.py        # Central state manager (no Tkinter deps)
│   ├── undo.py             # Undo stack
│   ├── autosave.py         # JSON persistence
│   └── template_manager.py # Template CRUD
├── classes/                # Legacy data classes (attacker, defender, binder)
├── templates/              # JSON defender profiles
└── tests/                  # Unit tests
```

## Build Executable

```bash
pyinstaller run.spec
```

## License

MIT
