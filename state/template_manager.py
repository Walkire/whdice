"""Template manager — CRUD operations on defender template JSON files."""

import json
import os
import re
from typing import List, Optional


class TemplateManager:
    """Manages defender template JSON files in a folder."""

    def __init__(self, folder: str = "templates"):
        self._folder = folder
        os.makedirs(self._folder, exist_ok=True)

    def list_templates(self) -> List[dict]:
        """Return all templates as dicts with an added '_filename' key."""
        templates = []
        for filename in sorted(os.listdir(self._folder)):
            if filename.endswith(".json"):
                data = self._read_file(filename)
                if data is not None:
                    data["_filename"] = filename
                    templates.append(data)
        return templates

    def create_template(self, data: dict) -> str:
        """Create a new template file. Returns the filename."""
        name = data.get("name", "unnamed")
        filename = self._name_to_filename(name)
        # Ensure uniqueness
        filename = self._unique_filename(filename)
        self._write_file(filename, data)
        return filename

    def update_template(self, filename: str, data: dict) -> None:
        """Overwrite an existing template file with new data."""
        filepath = os.path.join(self._folder, filename)
        if os.path.exists(filepath):
            self._write_file(filename, data)

    def delete_template(self, filename: str) -> None:
        """Delete a template file."""
        filepath = os.path.join(self._folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)

    def duplicate_template(self, filename: str) -> Optional[str]:
        """Duplicate a template, returning the new filename."""
        data = self._read_file(filename)
        if data is None:
            return None
        # Increment name
        original_name = data.get("name", "unnamed")
        data["name"] = self._increment_name(original_name)
        new_filename = self._name_to_filename(data["name"])
        new_filename = self._unique_filename(new_filename)
        self._write_file(new_filename, data)
        return new_filename

    # --- Private helpers ---

    def _read_file(self, filename: str) -> Optional[dict]:
        filepath = os.path.join(self._folder, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            return None

    def _write_file(self, filename: str, data: dict) -> None:
        filepath = os.path.join(self._folder, filename)
        # Strip internal keys before writing
        clean = {k: v for k, v in data.items() if not k.startswith("_")}
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(clean, f, indent=2)

    def _name_to_filename(self, name: str) -> str:
        """Convert a template name to a safe filename."""
        safe = re.sub(r"[^\w\s-]", "", name.lower())
        safe = re.sub(r"[\s]+", "_", safe.strip())
        if not safe:
            safe = "unnamed"
        return safe + ".json"

    def _unique_filename(self, filename: str) -> str:
        """Ensure filename is unique by appending a counter if needed."""
        if not os.path.exists(os.path.join(self._folder, filename)):
            return filename
        base, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(self._folder, f"{base}_{counter}{ext}")):
            counter += 1
        return f"{base}_{counter}{ext}"

    def _increment_name(self, name: str) -> str:
        """Increment a name for duplication (e.g. 'Foo' -> 'Foo (2)')."""
        match = re.match(r"^(.*?)\s*\((\d+)\)$", name)
        if match:
            base = match.group(1)
            num = int(match.group(2)) + 1
            return f"{base} ({num})"
        return f"{name} (2)"
