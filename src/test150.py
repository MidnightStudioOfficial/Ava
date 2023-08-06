import customtkinter as CTk
from PIL import Image

root = CTk.CTk()

# Create the main frame
main_frame = CTk.CTkFrame(root)
main_frame.pack(expand=True, fill=CTk.BOTH)

# Add the Develock Settings label
develock_settings_label = CTk.CTkLabel(main_frame, text="Develock Settings")
develock_settings_label.configure(font=("Helvetica", 16))
develock_settings_label.pack(pady=10)

# Add the ElevenClock Settings label
elevenclock_settings_label = CTk.CTkLabel(main_frame, text="ElevenClock Settings")
elevenclock_settings_label.configure(font=("Helvetica", 14))
elevenclock_settings_label.pack(pady=10)

# Add the Clock Settings label
clock_image = CTk.CTkImage(Image.open("Data/assets/bell.png"), size=(20, 20))
clock_settings_label = CTk.CTkLabel(main_frame, text="Clock Settings", image=clock_image, compound="left")
clock_settings_label.configure(font=("Helvetica", 12))
clock_settings_label.pack(pady=10)

# Add the Clock position and size label
clock_position_and_size_label = CTk.CTkLabel(main_frame, text="Clock position and size")
clock_position_and_size_label.configure(font=("Helvetica", 10))
clock_position_and_size_label.pack(pady=10)

# Add the Clock Appearance label
clock_appearance_label = CTk.CTkLabel(main_frame, text="Clock Appearance")
clock_appearance_label.configure(font=("Helvetica", 10))
clock_appearance_label.pack(pady=10)

# Add the Date & Time Settings label
date_and_time_settings_label = CTk.CTkLabel(main_frame, text="Date & Time Settings")
date_and_time_settings_label.configure(font=("Helvetica", 10))
date_and_time_settings_label.pack(pady=10)

# Add the Imamat date and time label
imamat_date_and_time_label = CTk.CTkLabel(main_frame, text="Imamat date and time")
imamat_date_and_time_label.configure(font=("Helvetica", 10))
imamat_date_and_time_label.pack(pady=10)

# Add the Tooltip Appearance label
tooltip_appearance_label = CTk.CTkLabel(main_frame, text="Tooltip Appearance")
tooltip_appearance_label.configure(font=("Helvetica", 10))
tooltip_appearance_label.pack(pady=10)

# Add the Fles and other experimental label
fles_and_other_experimental_label = CTk.CTkLabel(main_frame, text="Fles and other experimental (Use ONLY if something is not working)")
fles_and_other_experimental_label.configure(font=("Helvetica", 10))
fles_and_other_experimental_label.pack(pady=10)

root.mainloop()
