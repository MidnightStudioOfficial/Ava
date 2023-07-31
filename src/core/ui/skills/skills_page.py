import customtkinter as ctk
import tkinter as tk

from core.skill.skill import Skills


class skill:
    def __init__(self) -> None:
        self.debug_info = {}
        self.skills = Skills("Data")
        # load skill sample data
        self.training_sentences = []
        self.training_labels = []
        self.labels = []
        self.responses = []

    def update_debug_info_DEBUG(self):
        self.debug_info["Music"] = "TEST"
        self.debug_info["Story"] = "TEST"

    def get_debug_info(self):
        return self.debug_info

    def get_skills_intent(self):
        for intent, skill in self.skills.skills.items():
            for sample in skill.samples:
                self.training_sentences.append(sample)
                self.training_labels.append(intent)
            if intent not in self.labels:
                self.labels.append(intent)
        return self.training_sentences, self.training_labels

    def get_skills(self):
        for intent, skill in self.skills.skills.items():
            for sample in skill.samples:
                self.training_sentences.append(sample)
                self.training_labels.append(intent)
            if intent not in self.labels:
                self.labels.append(intent)
        return self.labels


class SkillGUI(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.skill = skill()
        # Define the layout of the GUI
        self.layout = {
            "Music": {
                "value": "test",
                "type": "other"
            },
            "Story": {
                "value": "test",
                "type": "other"
            }
        }

        # Create the main frame
        self.frame = ctk.CTkFrame(master=parent)
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Configure the grid layout
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

        # Set the font
        self.font = ctk.ThemeManager.theme["CTkFont"]["family"]

        # Create a label for the title
        self.label = ctk.CTkLabel(master=self.frame, text="Skills", font=(self.font, 25, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=10)

        # Create an entry for search
        self.entry = ctk.CTkEntry(master=self.frame, placeholder_text="search", width=200)
        self.entry.grid(row=0, column=1, pady=10, sticky="e")

        # Create a segmented button for filtering options
        self.option_type = ctk.CTkSegmentedButton(self.frame, values=["All", "memory", "other"], command=self.filter_list)
        self.option_type.set("All")
        self.option_type.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Create a scrollable frame for the list of items
        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame)
        self.scrollable_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")

        # Initialize the item frame dictionary
        self.item_frame = {}
        labels = self.skill.get_skills()

        for s in labels:
            self.layout[str(s)] = {
                "value": "test",
                "type": "other"
            }

        # Create the list of items
        self.create_list()

    def clear_list(self):
        """Clears the list of items"""
        for i in self.item_frame.values():
            i.pack_forget()

    def update_debug_info(self, key, value):
        self.layout[key]["value"] = value
        self.clear_list()
        self.create_list()

    def filter_list(self, type_):
        """Filters the list of items based on type"""
        if type_ == "All":
            for i in self.item_frame.values():
                i.pack(expand=True, fill="x", padx=5, pady=5)
            return
        elif type_ == "memory":
            self.clear_list()
            for i in self.layout.keys():
                if self.layout[i]["type"] == "memory":
                    self.item_frame[i].pack(expand=True, fill="x", padx=5, pady=5)
            return
        elif type_ == "other":
            self.clear_list()
            for i in self.layout.keys():
                if self.layout[i]["type"] == "other":
                    self.item_frame[i].pack(expand=True, fill="x", padx=5, pady=5)
            return

        self.clear_list()

    def add_item(self, name, value):
        """add new package to the list"""
        self.item_frame[name] = ctk.CTkFrame(self.scrollable_frame)
        self.item_frame[name].pack(expand=True, fill="x", padx=5, pady=5)

        self.item_frame[name].columnconfigure(0, weight=1)
        item_name = ctk.CTkButton(self.item_frame[name], fg_color="transparent",
                                            text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"],
                                            height=50, anchor="w", font=(self.font, 15, "bold"), width=500,
                                            text=name, hover=False)
        item_name.grid(row=0, column=0, sticky="ew", pady=5, padx=5)

        item_label = ctk.CTkLabel(self.item_frame[name], width=250, justify="left", text=value, anchor="w", wraplength=250)
        item_label.grid(row=0, column=1, padx=5)

    def create_list(self):
        for key in self.layout:
            value = self.layout[key]["value"]
            self.add_item(str(key), str(value))
