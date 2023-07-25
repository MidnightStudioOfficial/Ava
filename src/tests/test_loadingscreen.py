import unittest
from customtkinter import CTkLabel, CTkProgressBar, CTk, CTkButton
from core.ui.loadingscreen import SplashScreen


class TestSplashScreen(unittest.TestCase):
    def setUp(self):
        # Create a dummy root window to act as the parent for SplashScreen
        self.root = CTk()

    def test_splash_screen(self):
        splash_screen = SplashScreen(self.root)
        self.assertIsInstance(splash_screen.text_label, CTkLabel)
        self.assertIsInstance(splash_screen.progressbar, CTkProgressBar)
        self.assertIsInstance(splash_screen.cancel_button, CTkButton)

        # Test set_text() method
        expected_text = "Testing..."
        splash_screen.set_text(expected_text)
        self.assertEqual(splash_screen.text_label.cget("text"), expected_text)

        # Test set_progress() method
        expected_progress = 50
        splash_screen.set_progress(expected_progress)
        actual_progress = round(splash_screen.progressbar.get() * 100)
        self.assertEqual(actual_progress, expected_progress)

    def tearDown(self):
        self.root.destroy()


if __name__ == "__main__":
    unittest.main()
