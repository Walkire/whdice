"""Template Library Page — browse, create, edit, delete, duplicate defender templates."""

import customtkinter

from state.app_state import AppState
from state.template_manager import TemplateManager
from ui.styles import (
    FONT_TITLE, FONT_SECTION, FONT_SMALL, BUTTON_HEIGHT_SMALL, PAGE_PAD_X,
    COLOR_DANGER, COLOR_DANGER_HOVER, COLOR_MUTED_TEXT,
)


class TemplatePage(customtkinter.CTkFrame):
    """Page for managing defender unit templates.

    Displays a scrollable list of templates with actions: load, edit, delete, duplicate.
    Users can also create new templates from the current defender config.
    """

    def __init__(self, master, state: AppState, template_manager: TemplateManager = None,
                 on_load_template=None, **kwargs):
        super().__init__(master, corner_radius=0, fg_color="transparent", **kwargs)
        self._state = state
        self._tm = template_manager or TemplateManager()
        self._on_load_template = on_load_template
        self._template_frames: list = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Top bar ---
        top_bar = customtkinter.CTkFrame(self, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="ew", padx=PAGE_PAD_X, pady=(PAGE_PAD_X, 4))

        title = customtkinter.CTkLabel(
            top_bar, text="Template Library",
            font=customtkinter.CTkFont(size=FONT_TITLE[1], weight=FONT_TITLE[2]),
        )
        title.pack(side="left")

        self._create_btn = customtkinter.CTkButton(
            top_bar,
            text="+ Save Current Defender",
            command=self._create_template,
            height=BUTTON_HEIGHT_SMALL,
        )
        self._create_btn.pack(side="right")

        # --- Scrollable template list ---
        self._scroll_frame = customtkinter.CTkScrollableFrame(self)
        self._scroll_frame.grid(row=1, column=0, sticky="nsew", padx=PAGE_PAD_X, pady=(4, PAGE_PAD_X))
        self._scroll_frame.grid_columnconfigure(0, weight=1)

        # Empty state label
        self._empty_label = customtkinter.CTkLabel(
            self._scroll_frame,
            text="No templates saved yet.\nSave the current defender configuration to create one.",
            text_color=("gray50", "gray60"),
        )

        # Initial render
        self._rebuild_list()

    def _rebuild_list(self) -> None:
        """Rebuild the template list from disk."""
        for frame in self._template_frames:
            frame.destroy()
        self._template_frames.clear()

        templates = self._tm.list_templates()

        if not templates:
            self._empty_label.grid(row=0, column=0, pady=40)
            return

        self._empty_label.grid_remove()

        for idx, tpl in enumerate(templates):
            row_frame = self._build_template_row(idx, tpl)
            row_frame.grid(row=idx, column=0, sticky="ew", pady=(0, 6))
            self._template_frames.append(row_frame)

    def _build_template_row(self, idx: int, tpl: dict) -> customtkinter.CTkFrame:
        """Build a single template row with info and action buttons."""
        row = customtkinter.CTkFrame(self._scroll_frame)
        row.grid_columnconfigure(0, weight=1)

        # Template info
        info_frame = customtkinter.CTkFrame(row, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=6)

        name = tpl.get("name", "Unnamed")
        filename = tpl.get("_filename", "")

        name_label = customtkinter.CTkLabel(
            info_frame, text=name,
            font=customtkinter.CTkFont(size=FONT_SECTION[1], weight=FONT_SECTION[2]),
        )
        name_label.pack(anchor="w")

        # Stats summary line
        stats_text = (
            f"T{tpl.get('toughness', '?')} "
            f"Sv{tpl.get('save', '?')}+ "
            f"W{tpl.get('wounds', '?')} "
            f"× {tpl.get('model_count', '?')} models"
        )
        if tpl.get("invuln") and tpl["invuln"] > 0:
            stats_text += f"  Inv{tpl['invuln']}+"
        if tpl.get("feel_no_pain") and tpl["feel_no_pain"] > 0:
            stats_text += f"  FNP{tpl['feel_no_pain']}+"

        stats_label = customtkinter.CTkLabel(
            info_frame, text=stats_text,
            text_color=COLOR_MUTED_TEXT,
            font=customtkinter.CTkFont(size=FONT_SMALL[1]),
        )
        stats_label.pack(anchor="w")

        # Action buttons
        btn_frame = customtkinter.CTkFrame(row, fg_color="transparent")
        btn_frame.grid(row=0, column=1, padx=(4, 8), sticky="e")

        load_btn = customtkinter.CTkButton(
            btn_frame, text="Load", width=60, height=BUTTON_HEIGHT_SMALL,
            command=lambda f=filename: self._load_template(f),
        )
        load_btn.pack(side="left", padx=2)

        dup_btn = customtkinter.CTkButton(
            btn_frame, text="Duplicate", width=72, height=BUTTON_HEIGHT_SMALL,
            fg_color="transparent", border_width=1,
            text_color=("gray10", "gray90"),
            command=lambda f=filename: self._duplicate_template(f),
        )
        dup_btn.pack(side="left", padx=2)

        del_btn = customtkinter.CTkButton(
            btn_frame, text="Delete", width=60, height=BUTTON_HEIGHT_SMALL,
            fg_color=COLOR_DANGER[0], hover_color=COLOR_DANGER_HOVER[0],
            command=lambda f=filename: self._delete_template(f),
        )
        del_btn.pack(side="left", padx=2)

        return row

    def _create_template(self) -> None:
        """Save the current defender config as a new template."""
        data = dict(self._state.defender)
        # Use a dialog to ask for name
        dialog = customtkinter.CTkInputDialog(
            text="Enter a name for this template:",
            title="New Template",
        )
        name = dialog.get_input()
        if not name or not name.strip():
            return
        data["name"] = name.strip()
        self._tm.create_template(data)
        self._rebuild_list()

    def _load_template(self, filename: str) -> None:
        """Load a template into the defender state."""
        templates = self._tm.list_templates()
        for tpl in templates:
            if tpl.get("_filename") == filename:
                # Remove internal keys before loading into state
                load_data = {k: v for k, v in tpl.items() if not k.startswith("_")}
                self._state.update_defender(**load_data)
                if self._on_load_template:
                    self._on_load_template()
                return

    def _duplicate_template(self, filename: str) -> None:
        """Duplicate an existing template."""
        self._tm.duplicate_template(filename)
        self._rebuild_list()

    def _delete_template(self, filename: str) -> None:
        """Delete a template."""
        self._tm.delete_template(filename)
        self._rebuild_list()
