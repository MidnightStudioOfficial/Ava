from core.ui.signup.sign_up import SignUpApp
import customtkinter

if __name__ == '__main__':
    root = customtkinter.CTk()
    s = SignUpApp(root)
    root.mainloop()