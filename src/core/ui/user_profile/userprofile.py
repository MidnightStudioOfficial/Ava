import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import json


class ProfileClass(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.profile_data = None

        # Load and resize the image
        image = Image.open("Data/assets/ava.jfif")
        image = image.resize((50, 50))  # Adjust the size as needed

        # Create a circular mask for the button
        mask = Image.new("L", (50, 50), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 50, 50), fill=255)

        # Apply the circular mask to the image
        image.putalpha(mask)

        # Create a PhotoImage from the modified image
        photo = ImageTk.PhotoImage(image)

        self.canvas = ctk.CTkFrame(parent, width=500, height=150)  # ctk.CTkCanvas
        self.canvas.pack_propagate(False)  # Prevent resizing of the canvas
        self.canvas.pack()

        self.profile_label = ctk.CTkLabel(self.canvas, image=photo, text="")
        self.profile_label.pack(pady=(0, 78), side="top")  # padx=30, pady=60

        self.name_frame = ctk.CTkFrame(
            parent, width=400, height=100, fg_color="#333333"
        )
        self.name_frame.pack(padx=10, pady=10, expand=True, fill="both")
        self.first_name_label = ctk.CTkLabel(
            self.name_frame, text="John", font=("Segoe UI", 20), fg_color="#333333"
        )
        self.first_name_label.pack(side="left", padx=20)
        self.last_name_label = ctk.CTkLabel(
            self.name_frame, text="Doe", font=("Segoe UI", 20), fg_color="#333333"
        )
        self.last_name_label.pack(side="left", padx=10)

        self.title_label = ctk.CTkLabel(
            parent, text="Software Developer", font=("Segoe UI", 14), fg_color="#333333"
        )
        self.title_label.pack(pady=(20, 10))

        # self.info_badges_frame = ctk.CTkFrame(parent, width=400, height=300)

        self.info_frame = ctk.CTkFrame(parent, width=400, height=300)
        self.info_frame.pack(padx=10, pady=10, expand=True, fill="both")
        self.title_info_label = ctk.CTkLabel(
            self.info_frame,
            text="Bio:",
            font=("Segoe UI", 10),
            fg_color="#333333",
            justify="left",
            wraplength=380,
            corner_radius=7,
        )
        self.title_info_label.pack()
        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="%(bio_info)",
            font=("Segoe UI", 10),
            fg_color="#333333",
            justify="left",
            wraplength=380,
            corner_radius=6,
        )
        self.info_label.pack()

        self.skills_frame = ctk.CTkFrame(parent, width=400, height=100)
        self.skills_frame.pack_propagate(False)  # Prevent resizing of the canvas
        self.skills_frame.pack(padx=10, pady=10, fill="both")  # , expand=True
        self.skills_label = ctk.CTkLabel(
            self.skills_frame,
            text="Skills:",
            font=("Segoe UI", 14),
            fg_color="#333333",
            corner_radius=7,
        )
        self.skills_label.pack()

        # User Achievements Section
        achievements_frame = ctk.CTkFrame(parent)
        # achievements_frame.grid(row=2, column=0, pady=(0, 10), sticky="w", padx=10)
        achievements_frame.pack()

        achievement_label = ctk.CTkLabel(
            achievements_frame, text="Achievements:", font=("Arial", 12, "bold")
        )
        achievement_label.pack(anchor=ctk.W, pady=(10, 5))

        # User Badges
        badges_frame = ctk.CTkFrame(achievements_frame)
        badges_frame.pack()

        badge_images = [
            "Data/assets/ava.jfif",
            "Data/assets/ava.jfif",
            "Data/assets/ava.jfif",
        ]

        for i, badge_path in enumerate(badge_images):
            badge = Image.open(badge_path)
            badge = badge.resize((30, 30), Image.ANTIALIAS)
            badge = ImageTk.PhotoImage(badge)

            badge_label = ctk.CTkLabel(badges_frame, image=badge, text="")
            badge_label.pack(padx=5)
            # badge_label.grid(row=0, column=i, padx=5)

        self._load_profile()
        self._set_profile()

    def _load_profile(self):
        try:
            with open("Data/profile/profile.json", "r") as f:
                data = json.load(f)
                self.profile_data = data
        except FileNotFoundError:
            print("File not found")
        except json.JSONDecodeError:
            print("Invalid JSON syntax")

    def _set_profile(self):
        interests = self.profile_data["interests"]
        for interest in interests:
            interest_label = ctk.CTkLabel(
                self.skills_frame, text="- " + interest, font=("Segoe UI", 12)
            )
            interest_label.pack()
