import customtkinter as ctk
import tkinter as tk
import threading
import time

class bell:
    def __init__(self) -> None:
        pass
        

class BellGUI(ctk.CTkToplevel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.bell = bell()
        # Define the layout of the GUI
        self.layout = {
            "TEST": {
                "value": "test",
                "type": "other",
                "details": "This is a test item."
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
        self.label = ctk.CTkLabel(master=self.frame, text="Notifications", font=(self.font,25,"bold"))
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
        self.scrollable_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(0,10), sticky="nsew")
        
        # Initialize the item frame dictionary
        self.item_frame = {}
        
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
        """ add new notification to the list """
        self.item_frame[name] = ctk.CTkFrame(self.scrollable_frame)
        self.item_frame[name].pack(expand=True, fill="x", padx=5, pady=5)
        

        self.item_frame[name].columnconfigure(0, weight=1)
        item_name = ctk.CTkButton(self.item_frame[name], fg_color="transparent",
                                            text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"],
                                            height=50, anchor="w", font=(self.font, 15, "bold"), width=500,
                                            text=name, hover=False)
        item_name.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        item_name.bind("<Button-1>", lambda event, item_name=name: self.show_item_details(event, item_name))
        
        item_label = ctk.CTkLabel(self.item_frame[name], width=250, justify="left", text=value, anchor="w", wraplength=250)
        item_label.grid(row=0, column=1, padx=5)
        # Create an "Edit" button
        edit_button = ctk.CTkButton(self.item_frame[name], text="Edit", font=(self.font, 12), width=10,
                                    command=lambda item_name=name: self.edit_item(item_name))
        edit_button.grid(row=0, column=2, padx=5)

        # Create a "Delete" button
        delete_button = ctk.CTkButton(self.item_frame[name], text="Delete", font=(self.font, 12), width=10,
                                      command=lambda item_name=name: self.delete_item(item_name))
        delete_button.grid(row=0, column=3, padx=5)
        
    def create_list(self):
        for key in self.layout:
            value = self.layout[key]["value"]
            self.add_item(str(key), str(value))
            
    def edit_item(self, item_name):
        """Callback function to edit the item's value"""
        # You can implement the editing functionality here
        # For example, you can open a dialog or entry field to allow the user to modify the value

        # After the value is edited, update the GUI display
        new_value = "New Value"  # Replace with the actual edited value
        self.update_debug_info(item_name, new_value)

    def delete_item(self, item_name):
        """Callback function to delete the item"""
        # You can implement the deletion functionality here
        # For example, you can ask for confirmation or remove the item from the list directly

        # After the item is deleted, update the GUI display
        del self.layout[item_name]
        self.clear_list()
        self.create_list()
        
    def show_item_details(self, event, item_name):
        """Show additional details for the clicked item"""
        details = self.layout[item_name]["details"]
        # You can implement the display of item details here
        # For example, you can expand the item frame to show the details or open a popup window

        # Here, we will print the details to the console for demonstration purposes
        print(f"Item: {item_name}")
        print(f"Details: {details}")
            