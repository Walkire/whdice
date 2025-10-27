⚔️ Warhammer Combat Simulator
A GUI-based simulation tool for Warhammer 40K combat scenarios. This Python application allows users to configure attacker and defender units, simulate combat interactions, and view detailed statistical outcomes.

🧰 Features
- **Tkinter GUI** with organized input frames for attackers and defenders
- **Comprehensive weapon configuration** including special rules (Torrent, Blast, Lethal Hits, etc.)
- **Advanced modifiers** for rerolls, damage reduction, and wound modifications
- **Weapon list management** with drag-and-drop reordering and save/delete functionality
- **Statistical simulation** running 100,000 iterations for accurate results
- **Detailed results display** with summary table and expandable weapon details
- **Unit wipe probability** calculations

📦 Requirements
- Python 3.8+
- Standard library only (tkinter, random, re, unittest)

🚀 Getting Started
1. Clone the repository
2. Navigate to the root directory
3. Run the application:
   ```
   python run.py
   ```

🖥️ Usage
1. **Configure Attacker**: Set weapon stats (attacks, hit score, strength, AP, damage) and modifiers
2. **Configure Defender**: Set unit stats (toughness, save, wounds, model count) and defensive modifiers
3. **Save Weapons**: Add multiple weapon configurations to simulate combined attacks
4. **Run Simulation**: Execute 100,000 iterations to get statistical results
5. **Analyze Results**: View summary table and click weapons for detailed breakdowns

🎯 Weapon Features
- **Basic Stats**: Attacks (dice notation supported), WS/BS, Strength, AP, Damage
- **Special Rules**: Torrent, Blast, Lethal Hits, Devastating Wounds, Sustained Hits
- **Rerolls**: Hit rerolls, wound rerolls, damage rerolls (all/ones)
- **Modifiers**: +1 to hit/wound, critical hit/wound thresholds

🛡️ Defender Features
- **Core Stats**: Toughness, Save, Invulnerable Save, Wounds, Model Count
- **Defensive Abilities**: Feel No Pain, +1 Save modifier
- **Damage Reduction**: Minus one damage, halve damage, nullify one attack
- **Wound Reduction**: Conditional -1 to wound based on strength comparison

🧪 Simulation Logic
The simulator processes combat in Warhammer 40K order:
1. **Attacks**: Roll for number of attacks (with Blast bonus)
2. **Hit Rolls**: Calculate hits with rerolls and critical hits
3. **Special Hit Effects**: Apply Sustained Hits and Lethal Hits
4. **Wound Rolls**: Calculate wounds with strength vs toughness
5. **Special Wound Effects**: Apply Devastating Wounds
6. **Save Rolls**: Apply armor saves, AP, and invulnerable saves
7. **Damage**: Roll damage with rerolls and apply reduction
8. **Feel No Pain**: Apply FNP saves to final damage
9. **Kill Calculation**: Track model kills and unit wipe probability

🧪 Testing
Run the test suite:
```
python -m unittest tests/test_sim_functions.py
```

📁 Project Structure
```
whdice/
├── classes/           # Core data classes
│   ├── attacker.py   # Attacker unit configuration
│   ├── defender.py   # Defender unit configuration
│   ├── binder.py     # Tkinter variable binding
│   └── data.py       # Data container class
├── tests/            # Unit tests
├── enums.py          # Enumeration definitions
├── sim_functions.py  # Core simulation logic
├── utils.py          # Utility functions
└── run.py           # Main application entry point
```

📄 License
This project is licensed under the MIT License.

🙋‍♂️ Contributing
Feel free to fork the repo and submit pull requests. For major changes, open an issue first to discuss your ideas.
