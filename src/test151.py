import customtkinter as CTk
from PIL import Image

root = CTk.CTk()

label_configs = [
    {"text": "Develock Settings", "font_size": 16},
    {"text": "ElevenClock Settings", "font_size": 14},
    {"text": "Clock Settings", "font_size": 12, "image": "bell.png", "image_size": (20, 20)},
    {"text": "Clock position and size", "font_size": 10},
    {"text": "Clock Appearance", "font_size": 10},
    {"text": "Date & Time Settings", "font_size": 10},
    {"text": "Imamat date and time", "font_size": 10},
    {"text": "Tooltip Appearance", "font_size": 10},
    {"text": "Fles and other experimental (Use ONLY if something is not working)", "font_size": 10}
]

main_frame = CTk.CTkFrame(root)
main_frame.pack(expand=True, fill=CTk.BOTH)

for config in label_configs:
    label = CTk.CTkButton(main_frame, text=config["text"])
    label.configure(font=("Helvetica", config["font_size"]))
    
    if "image" in config and "image_size" in config:
        image_path = f"Data/assets/{config['image']}"
        label_image = CTk.CTkImage(Image.open(image_path), size=config["image_size"])
        label.configure(image=label_image, compound="left")
    
    label.pack(pady=10)

root.mainloop()
