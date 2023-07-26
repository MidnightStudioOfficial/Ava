import customtkinter as ctk
import tkinter as tk
import threading
import time
import difflib

import os
import json


class Bell:
    def __init__(self):
        self.notifications = {}
        self.load_notifications()

    def save_notifications(self) -> None:
        """Saves the notifications to a file"""
        try:
            with open("Data/notifications.json", 'w') as file:
                json.dump(self.notifications, file)
            print("Notifications saved successfully.")
        except Exception as e:
            print(f"Error saving notifications: {e}")

    def load_notifications(self) -> None:
        """Loads the notifications from a file"""
        try:
            if os.path.exists("Data/notifications.json"):
                with open("Data/notifications.json", 'r') as file:
                    self.notifications = json.load(file)
                print("Notifications loaded successfully.")
            else:
                self.create_default_file()
                print("New file created with default data.")
        except Exception as e:
            print(f"Error loading notifications: {e}")

    def create_default_file(self):
        """Creates a new file with default data"""
        default_data = {
            "Welcome to Ava!": {
                "value": "Welcome to Ava! We hope you like it!",
                "type": "other",
                "details": "Welcome to Ava! We hope you like it!",
                "tags": ["welcome", "ava"]
            }
        }
        self.notifications = default_data
        self.save_notifications()

    def add_notification(self, notification_id: str, name: str, details: str, notification_type: str, tags):
        """Adds a new notification to the list"""
        self.notifications[str(notification_id)] = {
                "value": str(name),
                "type": str(notification_type),
                "details": str(details),
                "tags": tags
            }
        self.save_notifications()

    def remove_notification(self, notification):
        """Removes a notification from the list"""
        if notification in self.notifications:
            del self.notifications[notification]
            # self.notifications.remove(notification)
            print("Notification removed successfully.")
        else:
            print("Notification not found.")

    def get_notifications(self):
        """Returns the list of notifications"""
        return self.notifications


class BellGUI(ctk.CTkToplevel):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.bell = Bell()
        # Define the layout of the GUI
        self.layout = {
            "TEST": {
                "value": "test",
                "type": "other",
                "details": "This is a test item.",
                "tags": ["test"]
            },
            "TEST2": {
                "value": "test2",
                "type": "memory",
                "details": "This is a test2 item.",
                "tags": ["test2"]
            }
        }
        self.layout = self.bell.notifications

        # Create the main frame
        self.main_frame = ctk.CTkFrame(master=parent)
        self.main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Configure the grid layout
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)

        # Set the font
        self.font = ctk.ThemeManager.theme["CTkFont"]["family"]

        # Create a label for the title
        self.title_label = ctk.CTkLabel(master=self.main_frame, text="Notifications", font=(self.font, 25, "bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=10)

        # Create an entry for search
        self.search_entry = ctk.CTkEntry(master=self.main_frame, placeholder_text="search", width=200)
        self.search_entry.grid(row=0, column=1, pady=10, sticky="e")
        self.search_entry.bind("<KeyRelease>", lambda e: self.search_package2(self.search_entry.get()))

        # Create a segmented button for filtering options
        self.option_type = ctk.CTkSegmentedButton(self.main_frame, values=["All", "memory", "other"], command=self.filter_list)
        self.option_type.set("All")
        self.option_type.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='ew')

        # Create a scrollable frame for the list of items
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")

        # Initialize the item frame dictionary
        self.item_frame = {}

        # Create the list of items
        self.create_list()

    def clear_list(self) -> None:
        """Clears the list of items"""
        for frame in self.item_frame.values():
            frame.pack_forget()

    def search_package(self, string):
        """Searches the packages based on package tags"""
        try:
            # Input Validation
            if not isinstance(string, str) or not string:
                raise ValueError("Invalid search string")

            # Clear the list before performing the search
            self.clear_list()

            # Normalize the search string
            search_string = string.lower().replace(" ", "")

            for key, value in self.layout.items():
                if "tags" in value:
                    found = False
                    for tag in value["tags"]:
                        if tag.replace(" ", "").startswith(search_string):
                            if self.layout[key]["type"] == self.option_type.get() or self.option_type.get() == "All":
                                if key in self.item_frame:
                                    self.item_frame[key].pack(expand=True, fill='x', padx=5, pady=5)
                                    found = True
                                    break
                                else:
                                    print(f"Frame not found for item '{key}'")
                    if not found:
                        if key in self.item_frame:
                            self.item_frame[key].pack_forget()
                else:
                    print(f"Tags missing for item '{key}'")

            # Scroll to the top of the scrollable frame
            self.scrollable_frame._parent_canvas.yview_moveto(0.0)

        except Exception as e:
            print(f"Error searching package: {e}")

    def search_package2(self, string):
        """Searches the packages based on package tags"""
        try:
            # Input Validation
            if not isinstance(string, str) or not string:
                raise ValueError("Invalid search string")

            # Clear the list before performing the search
            self.clear_list()

            # Normalize the search string
            search_string = string.lower().replace(" ", "")

            for key, value in self.layout.items():
                if "tags" in value:
                    found = False
                    for tag in value["tags"]:
                        normalized_tag = tag.lower().replace(" ", "")
                        if difflib.SequenceMatcher(None, normalized_tag, search_string).ratio() >= 0.6:
                            if self.layout[key]["type"] == self.option_type.get() or self.option_type.get() == "All":
                                if key in self.item_frame:
                                    self.item_frame[key].pack(expand=True, fill='x', padx=5, pady=5)
                                    found = True
                                    break
                                else:
                                    print(f"Frame not found for item '{key}'")
                    if not found:
                        if key in self.item_frame:
                            self.item_frame[key].pack_forget()
                else:
                    print(f"Tags missing for item '{key}'")

            # Scroll to the top of the scrollable frame
            self.scrollable_frame._parent_canvas.yview_moveto(0.0)

        except Exception as e:
            print(f"Error searching package: {e}")

    def update_notification_info(self, key, value) -> None:
        self.layout[key]["value"] = value
        self.clear_list()
        self.create_list()

    def destroy_item_frame(self, item_name) -> None:
        if item_name in self.item_frame:
            self.item_frame[item_name].destroy()
            del self.item_frame[item_name]

    def filter_list(self, type_):
        """Filters the list of items based on type"""
        valid_types = ["All", "memory", "other"]

        try:
            if type_ not in valid_types:
                raise ValueError("Invalid filter type")

            if type_ == "All":
                for frame in self.item_frame.values():
                    frame.pack(expand=True, fill='x', padx=5, pady=5)
            else:
                self.clear_list()
                for key, value in self.layout.items():
                    if value.get("type") == type_:
                        if key in self.item_frame:
                            self.item_frame[key].pack(expand=True, fill='x', padx=5, pady=5)
                        else:
                            print(f"Frame not found for item '{key}'")

        except Exception as e:
            print(f"Error filtering list: {e}")

    def add_notification(self, name, value) -> None:
        """Add a new notification to the list"""
        # Create a frame to contain the notification item
        self.item_frame[name] = ctk.CTkFrame(self.scrollable_frame)
        self.item_frame[name].pack(expand=True, fill="x", padx=5, pady=5)

        # Configure the column weight for the frame
        self.item_frame[name].columnconfigure(0, weight=1)

        # Create a button for the item name
        item_name = ctk.CTkButton(self.item_frame[name], fg_color="transparent",
                                text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"],
                                height=50, anchor="w", font=(self.font, 15, "bold"), width=500,
                                text=name, hover=False)
        item_name.grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        item_name.bind("<Button-1>", lambda event, item_name=name: self.show_item_details(event, item_name))

        # Create a label for the item value
        item_label = ctk.CTkLabel(self.item_frame[name], width=250, justify="left", text=value, anchor='w', wraplength=250)
        item_label.grid(row=0, column=1, padx=5)

        # Create an "Edit" button
        edit_button = ctk.CTkButton(self.item_frame[name], text="Edit", font=(self.font, 12), width=10,
                                    command=lambda item_name=name: self.edit_item(item_name))
        edit_button.grid(row=0, column=2, padx=5)

        # Create a "Delete" button
        delete_button = ctk.CTkButton(self.item_frame[name], text="Delete", font=(self.font, 12), width=10,
                                    command=lambda item_name=name: self.delete_item(item_name))
        delete_button.grid(row=0, column=3, padx=5)

    def create_list(self) -> None:
        for key, notification in self.layout.items():
            value = notification["value"]
            self.add_notification(str(key), str(value))

    def new_notification(self, name, data) -> None:
        self.layout[str(name)] = data
        self.clear_list()
        self.create_list()

    def remove_notification(self, name) -> None:
        del self.layout[name]
        self.destroy_item_frame(name)

    def edit_item(self, item_name) -> None:
        """Callback function to edit the item's value"""
        # You can implement the editing functionality here
        # For example, you can open a dialog or entry field to allow the user to modify the value

        # After the value is edited, update the GUI display
        new_value = "New Value"  # Replace with the actual edited value
        self.update_notification_info(item_name, new_value)

    def delete_item(self, item_name):
        """Callback function to delete the item"""
        if item_name in self.layout:
            del self.layout[item_name]
            self.destroy_item_frame(item_name)
        else:
            print(f"Item '{item_name}' does not exist.")

    def show_item_details(self, event, item_name):
        """Show additional details for the clicked item"""
        if item_name in self.layout:
            details = self.layout[item_name]["details"]
            # You can implement the display of item details here
            # For example, you can expand the item frame to show the details or open a popup window

            # Here, we will print the details to the console for demonstration purposes
            print(f"Item: {item_name}")
            print(f"Details: {details}")

    def update_items_thread(self):
        """Thread target function to update the items asynchronously"""
        # Simulating a time-consuming task
        time.sleep(3)

        # Update the item values
        for key in self.layout:
            new_value = f"New Value for {key}"
            self.update_notification_info(key, new_value)

    def update_items(self):
        """Updates the items asynchronously using a separate thread"""
        thread = threading.Thread(target=self.update_items_thread)
        thread.start()
