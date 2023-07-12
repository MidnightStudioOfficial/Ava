from core.ui.signup.sign_up import SignUpApp
from core.ui.signup.profile_checker import ProfileChecker
import customtkinter

if __name__ == '__main__':
    root = customtkinter.CTk()
    checker = ProfileChecker()
    if checker.check_if_profile_exists() == False:
        s = SignUpApp(root)
    root.mainloop()