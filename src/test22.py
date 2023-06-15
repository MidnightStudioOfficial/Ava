import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image

class UserProfilePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.title("User Profile")
        self.master.geometry("400x400")
        self.master.resizable(False, False)
        self.master.configure(background="#f2f2f2")

    def create_widgets(self):
        # Main Frame
        frame = ctk.CTkFrame(self.master)
        frame.pack(fill=tk.BOTH, padx=20, pady=20)

        # Profile Cover Photo
        cover_photo_path = "Data/assets/Welcome.png"  # Replace with the path to your cover photo
        cover_photo = Image.open(cover_photo_path)
        cover_photo = cover_photo.resize((400, 150), Image.ANTIALIAS)
        cover_photo = ImageTk.PhotoImage(cover_photo)

        cover_label = tk.Label(frame, image=cover_photo)
        cover_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Profile Information Section
        info_frame = ctk.CTkFrame(frame)
        info_frame.grid(row=1, column=0, pady=(0, 10), sticky="w", padx=10)

        profile_pic = tk.Label(info_frame, text="Profile Picture", bg="#ffffff", fg="#333333", font=("Arial", 12, "bold"))
        profile_pic.pack(anchor=tk.W, pady=(10, 5))

        name_label = tk.Label(info_frame, text="John Doe", bg="#ffffff", fg="#333333", font=("Arial", 14, "bold"))
        name_label.pack(anchor=tk.W, pady=(0, 10))

        # User Achievements Section
        achievements_frame = ctk.CTkFrame(frame)
        achievements_frame.grid(row=2, column=0, pady=(0, 10), sticky="w", padx=10)

        achievement_label = tk.Label(achievements_frame, text="Achievements:", bg="#ffffff", fg="#333333", font=("Arial", 12, "bold"))
        achievement_label.pack(anchor=tk.W, pady=(10, 5))

        # User Badges
        badges_frame = ctk.CTkFrame(achievements_frame)
        badges_frame.pack(anchor=tk.W, padx=10)

        badge_images = [
            # Add paths to badge images here
        ]

        for i, badge_path in enumerate(badge_images):
            badge = Image.open(badge_path)
            badge = badge.resize((30, 30), Image.ANTIALIAS)
            badge = ImageTk.PhotoImage(badge)

            badge_label = tk.Label(badges_frame, image=badge)
            badge_label.grid(row=0, column=i, padx=5)

        # Edit Profile Section
        edit_frame = ctk.CTkFrame(frame)
        edit_frame.grid(row=3, column=0, pady=(20, 0), sticky="w", padx=10)

        edit_heading = tk.Label(edit_frame, text="Edit Profile", bg="#ffffff", fg="#333333", font=("Arial", 14, "bold"))
        edit_heading.pack(anchor=tk.W, pady=(10, 5))

        # Edit Profile Fields
        # Add your code here to create the necessary fields for editing the profile information

        # Save Changes Button
        save_button = tk.Button(edit_frame, text="Save Changes", width=12, bg="#2196f3", fg="#ffffff", font=("Arial", 10, "bold"))
        save_button.pack(side=tk.LEFT, padx=5)

        # Logout Button
        logout_button = tk.Button(edit_frame, text="Logout", width=10, bg="#f44336", fg="#ffffff", font=("Arial", 10, "bold"))
        logout_button.pack(side=tk.LEFT, padx=5)

# Create the main Tkinter window
root = ctk.CTk()

# Styling
#root.ctk_style.configure("CTkFrame", background="#f2f2f2")

# Create the user profile page
profile_page = UserProfilePage(root)

# Run the Tkinter event loop
root.mainloop()
