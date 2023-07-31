import customtkinter as ctk
import threading
import gc
import time


class Debug:
    def __init__(self) -> None:
        self.debug_info = {}

    def update_debug_info_DEBUG(self):
        self.debug_info["gc"] = gc.get_count()
        self.debug_info["version"] = "V0.2.2"

    def get_debug_info(self):
        return self.debug_info

class DebugDevPanel(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Debug Development Panel")
        self.geometry("400x300")

        # Create a label to display some information
        self.label = ctk.CTkLabel(self, text="Welcome to the Debug Dev Panel!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # Add buttons to perform actions or tests
        self.btn_action = ctk.CTkButton(self, text="Perform Action", command=self.perform_action)
        self.btn_action.pack(pady=10)

        self.btn_test = ctk.CTkButton(self, text="Run Test", command=self.run_test)
        self.btn_test.pack(pady=10)

        self.services = ctk.CTkButton(master=self, text='Services')
        self.services.pack(pady=10)

    def perform_action(self):
        # Implement the action you want to perform for the "Perform Action" button
        # Replace this with your actual action code
        print("Action performed!")

    def run_test(self):
        # Implement the test you want to run for the "Run Test" button
        # Replace this with your actual test code
        from core.base.tests import MultiTestClassRunner
        self.test_runner = MultiTestClassRunner()
        self.test_runner.run_tests()
        print("Test executed!")

class DebugGUI(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.debug = Debug()
        self.layout = {
            "gc": {
                "value": "test",
                "type": "memory"
            },
            "version": {
                "value": "test",
                "type": "other"
            }
        }

        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.font = ctk.ThemeManager.theme["CTkFont"]["family"]

        self.label = ctk.CTkLabel(master=self.frame, text="Debug", font=(self.font, 25, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=10)

        self.entry = ctk.CTkEntry(master=self.frame, placeholder_text="search", width=200)
        self.entry.grid(row=0, column=1, pady=10, sticky="e")

        self.more_button = ctk.CTkButton(master=self.frame, width=30, text='Dev Panel', command=self.open_dev_panel)
        self.more_button.grid(row=0, column=2, pady=10, sticky="e")

        self.option_type = ctk.CTkSegmentedButton(self.frame, values=["All", "memory", "other"], command=self.filter_list)
        self.option_type.set("All")
        self.option_type.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.scrollable_frame = ctk.CTkScrollableFrame(self.frame)
        self.scrollable_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="nsew")

        # Dictionary to hold references to individual frames for each item in the debug list
        self.item_frame = {}

        self.create_list()
        t = threading.Thread(target=self.display_debug_info)
        t.daemon = True
        t.start()

    def clear_list(self):
        for i in self.item_frame.values():
            i.pack_forget()

    def update_debug_info(self, key, value):
        self.layout[key]["value"] = value
        self.clear_list()
        self.create_list()

    def open_dev_panel(self):
        self.dev = DebugDevPanel(self)

    def filter_list(self, type_):
        if type_ == "All":
            for i in self.item_frame.values():
                i.pack(expand=True, fill="x", padx=5, pady=5)
            return 
        elif type_ == "memory":
            self.clear_list()
            for i in self.layout:
                if self.layout[i]["type"] == "memory":
                    self.item_frame[i].pack(expand=True, fill="x", padx=5, pady=5)
            return
        elif type_ == "other":
            self.clear_list()
            for i in self.layout:
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

    def display_debug_info(self):
        while True:
            self.debug.update_debug_info_DEBUG()
            new_info = self.debug.get_debug_info()
            for key in new_info:
                value = new_info[key]
                self.update_debug_info(str(key), str(value))
                self.filter_list(self.option_type.get())

            time.sleep(3)  # 1

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        self.button_1 = ctk.CTkButton(self, text="open toplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = DebugGUI(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it


if __name__ == '__main__':
    app = App()
    app.mainloop()
    debug = Debug()
    debug_gui = DebugGUI(debug)
