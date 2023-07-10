t = "Welcome to your very own voice assistant chatbot! This guide will help you get started and set up your chatbot to provide helpful and interactive voice-based conversations. Let's get right into it:"
import customtkinter as ctk


class ChatbotApp(ctk.CTk):
    def __init__(self):
        ctk.CTk.__init__(self)
        self.title("Chatbot")
        
        # Create container to hold the pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.pages = {}  # Dictionary to hold different pages
        self.page_inputs = {}  # Dictionary to store input values for each page
        
        # Create welcome page
        self.add_page("WelcomePage", WelcomePage)
        
        # Create get started page
        self.add_page("GetStartedPage", GetStartedPage)
        
        # Show the welcome page initially
        self.show_page("WelcomePage")
        
    def add_page(self, page_name, page_class):
        page = page_class(self.container, self)
        self.pages[page_name] = page
        
        # Adjust grid for the page
        page.grid(row=0, column=0, sticky="nsew")
        
    def show_page(self, page_name):
        page = self.pages[page_name]
        page.tkraise()
        
    def get_input(self, page_name):
        return self.page_inputs.get(page_name, "")
    
    def set_input(self, page_name, input_value):
        self.page_inputs[page_name] = input_value

class WelcomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        label = ctk.CTkLabel(self, text="Welcome to the Chatbot!")
        label.pack(pady=20)
        
        button = ctk.CTkButton(self, text="Get Started", command=lambda: self.get_started(controller))
        button.pack(pady=10)
        
    def get_started(self, controller):
        controller.set_input("WelcomePage", "")  # Clear previous input
        controller.show_page("GetStartedPage")

class GetStartedPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        
        label = ctk.CTkLabel(self, text="Get Started Page")
        label.pack(pady=20)
        
        # Retrieve input from WelcomePage
        input_value = controller.get_input("WelcomePage")
        
        input_label = ctk.CTkLabel(self, text="Input from WelcomePage: {}".format(input_value))
        input_label.pack(pady=10)
        
        button = ctk.CTkButton(self, text="Back to Welcome", command=lambda: self.back_to_welcome(controller))
        button.pack(pady=10)
        
    def back_to_welcome(self, controller):
        controller.set_input("GetStartedPage", "")  # Clear previous input
        controller.show_page("WelcomePage")

# Create the ChatbotApp instance and run the application
app = ChatbotApp()
app.mainloop()
