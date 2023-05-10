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
        
        self.name_frame = ctk.CTkFrame(parent, width=400, height=100, fg_color="#333333")
        self.name_frame.pack()
        self.first_name_label = ctk.CTkLabel(self.name_frame, text="John", font=("Segoe UI", 20), fg_color="#333333")
        #self.name_label.place(x=90, y=75)
        self.first_name_label.pack(side="left", padx=20)
        self.last_name_label = ctk.CTkLabel(self.name_frame, text="Doe", font=("Segoe UI", 20), fg_color="#333333")
        self.last_name_label.pack(side="left", padx=10)
        #self.name_label.grid(row=0, column=0, padx=20, pady=20, sticky="ew", columnspan=2)

        self.title_label = ctk.CTkLabel(parent, text="Software Developer", font=("Segoe UI", 14), fg_color="#333333")
        self.title_label.pack(pady=(20, 10))
        #self.title_label.configure(pady=7)
        #self.title_label.place(x=90, y=110)

        self.info_frame = ctk.CTkFrame(parent, width=400, height=300)
        self.info_frame.pack()
        self.title_info_label = ctk.CTkLabel(self.info_frame, text="Bio:", font=("Segoe UI", 10), fg_color="#333333", justify="left", wraplength=380, corner_radius=7)
        self.title_info_label.pack()
        #self.info_frame.place(x=50, y=200)
        self.info_label = ctk.CTkLabel(self.info_frame, text="<info>", font=("Segoe UI", 10), fg_color="#333333", justify="left", wraplength=380, corner_radius=6)
        self.info_label.pack()
        #self.info_label.pack(pady=20)

        self.skills_frame = ctk.CTkFrame(parent, width=400, height=100)
        #self.skills_frame.place(x=50, y=520)
        self.skills_frame.pack()
        self.skills_label = ctk.CTkLabel(self.skills_frame, text="Skills:", font=("Segoe UI", 14), fg_color="#333333", corner_radius=7)
        self.skills_label.pack()
        #self.skills_label = ctk.CTkLabel(self.skills_frame, text="Skills:", font=("Segoe UI", 14), fg_color="#333333", corner_radius=7)
        #self.skills_label.pack(side="left", padx=20)
        #self.skill1_label = ctk.CTkLabel(self.skills_frame, text="Python", font=("Segoe UI", 12), fg_color="#333333", corner_radius=7)
        #self.skill1_label.pack(side="left", padx=10)
        interests = ["Python programming", "Web development", "Data science"]
        for interest in interests:
            interest_label = ctk.CTkLabel(self.skills_frame, text="- " + interest, font=("Segoe UI", 12))
            interest_label.pack()
            
    def _load_profile(self):
        pass
        