import customtkinter as ctk

class ProfileClass(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        
        self.canvas = ctk.CTkCanvas(parent, width=500, height=150)
        self.canvas.pack()

        #self.profile_icon = ctk.CTkImage()
        self.profile_label = ctk.CTkLabel(parent)
        self.profile_label.place(x=30, y=60)

        self.name_label = ctk.CTkLabel(parent, text="John Doe", font=("Segoe UI", 20), fg_color="#333333")
        self.name_label.place(x=90, y=75)

        self.title_label = ctk.CTkLabel(parent, text="Software Developer", font=("Segoe UI", 14), fg_color="#333333")
        self.title_label.place(x=90, y=110)

        self.info_frame = ctk.CTkFrame(parent, width=400, height=300)
        self.info_frame.place(x=50, y=200)
        self.info_label = ctk.CTkLabel(self.info_frame, text="<info>", font=("Segoe UI", 10), fg_color="#333333", justify="left", wraplength=380)
        self.info_label.pack(pady=20)

        self.skills_frame = ctk.CTkFrame(parent, width=400, height=100)
        self.skills_frame.place(x=50, y=520)
        self.skills_label = ctk.CTkLabel(self.skills_frame, text="Skills:", font=("Segoe UI", 14), fg_color="#333333")
        self.skills_label.pack(side="left", padx=20)
        self.skill1_label = ctk.CTkLabel(self.skills_frame, text="Python", font=("Segoe UI", 12), fg_color="#333333")
        self.skill1_label.pack(side="left", padx=10)
        