import subprocess

def enable_dark_mode():
    try:
        subprocess.run(['reg', 'add', 'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', '/v', 'AppsUseLightTheme', '/t', 'REG_DWORD', '/d', '0', '/f'])
        print("Dark mode enabled.")
    except subprocess.CalledProcessError:
        print("Error enabling dark mode.")

def disable_dark_mode():
    try:
        subprocess.run(['reg', 'add', 'HKCU\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize', '/v', 'AppsUseLightTheme', '/t', 'REG_DWORD', '/d', '1', '/f'])
        print("Dark mode disabled.")
    except subprocess.CalledProcessError:
        print("Error disabling dark mode.")

choice = input("Enter 'enable' to enable dark mode or 'disable' to disable dark mode: ")

if choice == 'enable':
    enable_dark_mode()
elif choice == 'disable':
    disable_dark_mode()
else:
    print("Invalid choice.")
