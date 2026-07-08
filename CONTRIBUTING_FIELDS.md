# Adding a New Field to Attackers or Defenders

This guide walks through adding a new stat or modifier field to the attacker or defender configuration.

## Overview

A field flows through four layers:

1. **State defaults** — `state/app_state.py`
2. **UI panel** — `ui/widgets/attacker_panel.py` or `ui/widgets/defender_panel.py`
3. **Simulation engine** — `sim_functions.py` (if it affects combat math)
4. **Templates** — existing JSON files in `templates/` (defender fields only)

## Step-by-Step: Adding an Attacker Field

### 1. Add to state defaults

In `state/app_state.py`, add the field to `ATTACKER_DEFAULTS`:

```python
ATTACKER_DEFAULTS = {
    ...
    "my_new_field": False,  # or an int, str, etc.
}
```

### 2. Add to the AttackerPanel UI

In `ui/widgets/attacker_panel.py`, add the field to one of the sections:

**For a checkbox (boolean):**

Add an entry to `modifier_checks`:
```python
modifier_checks = [
    ...
    ("my_new_field", "My New Modifier", ATTACKER_DEFAULTS["my_new_field"]),
]
```

**For a text/number entry:**

Add an entry to `core_stats`:
```python
core_stats = [
    ...
    ("my_new_field", "My Field:", "entry", None, ATTACKER_DEFAULTS["my_new_field"]),
]
```

**For a dropdown:**

```python
("my_new_field", "My Field:", "dropdown", ["Option1", "Option2"], ATTACKER_DEFAULTS["my_new_field"]),
```

### 3. Update `get_values()` if needed

If the field is numeric, add it to the integer conversion block:
```python
for int_key in ("score", "strength", "ap", ..., "my_new_field"):
```

If it's a boolean checkbox, add it to the boolean block:
```python
for bool_key in ("plus_hit", "plus_wound", "my_new_field"):
```

### 4. Wire into simulation (if it affects combat)

In `sim_functions.py`, access the field from the attacker `Data` object:

```python
def calculate_hits(attacker, ...):
    if attacker.my_new_field:
        # apply modifier
```

The `Data` class (in `classes/data.py`) automatically exposes dict keys as attributes.

### 5. Done

The auto-save and undo systems automatically handle any field present in the state dict — no extra wiring needed.

---

## Step-by-Step: Adding a Defender Field

### 1. Add to state defaults

In `state/app_state.py`, add the field to `DEFENDER_DEFAULTS`:

```python
DEFENDER_DEFAULTS = {
    ...
    "my_new_field": 0,
}
```

### 2. Add to the DefenderPanel UI

In `ui/widgets/defender_panel.py`, same approach as attacker:

- Checkbox → add to `modifier_checks`
- Entry → add to `core_stats`
- Dropdown → add to `core_stats` with `"dropdown"` type and options list

### 3. Update `get_values()` conversion blocks

Same pattern as attacker — add to the int or bool conversion blocks as appropriate.

### 4. Wire into simulation

In `sim_functions.py`, access via the defender `Data` object:

```python
def calculate_saves(defender, ...):
    if defender.my_new_field:
        # apply modifier
```

### 5. Update templates (optional)

If you want existing templates to support the new field, add it to each JSON file in `templates/`. Otherwise, `TemplateManager` will load templates without it and the UI will use the default from `DEFENDER_DEFAULTS`.

---

## Tips

- **Enums**: If the field has a fixed set of values, define an enum in `enums.py` and use its `.value` strings as dropdown options.
- **Dice notation**: If the field accepts dice notation (like `"2d6"`), store it as a string. The `utils.py` module has `parse_dice()` for evaluation at simulation time.
- **No Tkinter in state**: The state layer must remain free of Tkinter types. All values should be plain Python (int, float, str, bool, list, dict).
- **Testing**: Add a test case in `tests/test_sim_functions.py` that mocks dice rolls and verifies the new field's effect on combat math.
