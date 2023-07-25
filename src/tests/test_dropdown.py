import unittest
from customtkinter import CTk
from core.ui.widgets.CTkScrollableDropdown.ctk_scrollable_dropdown import CTkScrollableDropdown

class TestCTkScrollableDropdown(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = CTk()
        cls.root.withdraw()  # Hide the root window as we don't need it for this test

    def test_create_scrollable_dropdown(self):
        # Create a scrollable dropdown and check if it was created successfully
        dropdown = CTkScrollableDropdown(self.root)
        self.assertIsInstance(dropdown, CTkScrollableDropdown)

        # Insert some values into the dropdown
        values = ["Option 1", "Option 2", "Option 3"]
        for value in values:
            dropdown.insert(value)

        # Check if the values were inserted correctly
        self.assertEqual(len(dropdown.values), len(values))
        for value in values:
            self.assertIn(value, dropdown.values)

        # Test the configure method
        new_values = ["New Option 1", "New Option 2"]
        dropdown.configure(values=new_values)
        self.assertEqual(len(dropdown.values), len(new_values))
        for value in new_values:
            self.assertIn(value, dropdown.values)

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

if __name__ == '__main__':
    unittest.main()
