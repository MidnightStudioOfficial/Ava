import re

def extract_search_request(text):
    # Define the regular expression pattern
    pattern = r'(?:google\s+search|search\s+google)\s+for\s+(.+)'

    # Use re.search() to find the pattern in the text
    match = re.search(pattern, text, re.IGNORECASE)

    # If a match is found, return the search request, otherwise return None
    return match.group(1) if match else "none"

# Example usage:
while True:
    text = input("you:")
    result = extract_search_request(text)
    if result != "none":
        print(result)  # Output: "cats"
