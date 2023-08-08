import customtkinter as ctk
import core.base.global_vars as global_vars
from core.ui.widgets.CTkScrollableDropdown.ctk_scrollable_dropdown import CTkScrollableDropdown
from core.ui.widgets.CTkToolTip.ctk_tooltip import CTkToolTip
from core.controllers.settings.settings_controller import SettingsController


# self.root1 = ctk.CTkFrame(parent, fg_color="transparent")
# self.root2 = ctk.CTkFrame(parent)
# self.root3 = ctk.CTkFrame(parent)

# # Grid all frames to the same cell in the grid layout
# # This will cause the frames to overlap each other
# for f in (self.root1, self.root2, self.root3):
#     f.grid(row=0, column=0, sticky='news')
# self.settings_frame = ctk.CTkFrame(self.root1, height=100, fg_color="transparent", bg_color='#dfdfdf')

# self.settings_frame.pack(expand=False)

#self.root1.tkraise()

class SettingsUI(ctk.CTkFrame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.parent = parent
        self.top_buttons_var = ctk.StringVar(value="Chat")
        self.chat_bubble_switch_var = ctk.StringVar(value="off")
        self.controller = SettingsController(settings_file="Data/settings.json")
        self.controller.load_settings()
        self.frames = [
            ("frame_1", "Chat"),
            ("frame_2", "Model"),
            ("frame_3", "Theme"),
            ("frame_4", "Other")
        ]
        self.__create_widgets()

    def __create_widgets(self):
        self.main_settings_frame = ctk.CTkFrame(self.parent, fg_color="transparent", bg_color='#dfdfdf')
        self.main_settings_frame.pack(expand=True)

        self.tab_view = ctk.CTkTabview(master=self.main_settings_frame)
        self.tab_view.pack(side=ctk.TOP)
        self.tab_view.add("Chat")
        self.tab_view.add("Model")
        self.tab_view.add("Theme")
        self.tab_view.add("Other")

        self.tab_view.set("Chat")  # set currently visible tab

        # Create frames and labels using loops
        for frame_name, label_text in self.frames:
            frame = ctk.CTkFrame(master=self.tab_view.tab(str(label_text)))
            frame.pack(pady=20, padx=10, fill='x', expand=True)

            label = ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(family='Lucida Console', size=15, weight="bold"))
            label.pack(ipady=4)

            # Assign the created frame to an attribute with the corresponding frame name
            setattr(self, frame_name, frame)

        self.chat_bubble_enable = ctk.CTkSwitch(self.frame_1, text="New chat bubble", command=self.chat_bubble_enable_event,
                                 variable=self.chat_bubble_switch_var, onvalue="on", offvalue="off")
        self.chat_bubble_enable.pack() # ipady=10

        # Initialize a StringVar to hold the state of the segmented button
        self.segemented_button_var = ctk.StringVar(value=self.controller.get_setting(key="theme", default="blue"))

        # Create a segmented button widget with three values: "blue", "green", "dark-blue"
        self.segemented_button = ctk.CTkSegmentedButton(self.frame_3, values=["blue", "green", "dark-blue"],
                                                     command=self.theme_segmented_button_callback,
                                                     variable=self.segemented_button_var)
        self.segemented_button.pack()  # Pack the segmented button onto the frame

        # Create a button to reset training data
        self.reset_train_button = ctk.CTkButton(self.frame_1, border_width=0, text="Reset training data")
        self.reset_train_button.pack() # Pack the reset training button onto the frame

        # Create an entry widget to input "Window Style" text
        self.entry = ctk.CTkEntry(self.frame_3, width=240, placeholder_text="Window Style")
        self.entry.pack(fill='x', padx=10, pady=10)  # Pack the entry widget onto the frame

        # Create a scrollable dropdown widget for selecting a window style
        self.style_dropdown = CTkScrollableDropdown(self.entry, values=global_vars.STYLES_LIST, command=self.style_dropdown_click,
                            autocomplete=True) # Using autocomplete
        self.style_dropdown_tooltip = CTkToolTip(self.entry, delay=0.7, message=str(global_vars.TOOLTIP_MESSAGES["style_dropdown"]))
        self.entry.insert(0, 'Window Style')  # Insert default text to the entry widget

        label = ctk.CTkLabel(self.frame_1, text="Chat Bubble Corner Radius", font=ctk.CTkFont(family='Sans Serif', size=13, weight="bold"))
        label.pack(ipady=2)
        # Create a slider widget with a range from 0 to 100
        self.slider_1 = ctk.CTkSlider(master=self.frame_1, from_=0, to=100)

        self.slider_1.pack(padx=10) # pady=10,

        #self.bottomFrame1 = ctk.CTkFrame(self.main_settings_frame, height=100, fg_color="transparent", bg_color='#dfdfdf')

        # Pack the bottomFrame1 to fill the X direction and be placed at the bottom of its parent widget
        #self.bottomFrame1.pack(fill=ctk.X, side=ctk.BOTTOM)

        #self.top_buttons = ctk.CTkSegmentedButton(self.main_settings_frame, values=["Chat", "Model", "Theme", "Other"], variable=self.top_buttons_var)
        #self.top_buttons.pack()

    def chat_bubble_enable_event(self):
        pass

    def theme_segmented_button_callback(self, value):
        self.controller.set_setting(key="theme", value=value)

    def style_dropdown_click(self):
        pass
