import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x780")
app.title("CustomTkinter simple_example.py")

def slider_callback(value):
    progressbar_1.set(value)
    label.configure(text=str(value))

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(frame_1, text="CTkLabel", fg_color="transparent")
label.pack()

progressbar_1 = customtkinter.CTkProgressBar(master=frame_1)
progressbar_1.pack(pady=10, padx=10)

slider_1 = customtkinter.CTkSlider(master=frame_1, command=slider_callback, from_=0, to=100)
slider_1.pack(pady=10, padx=10)
slider_1.set(0.5)

app.mainloop()
