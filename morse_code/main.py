# Morse Code Dictionary
morse_dict = {
    # Letters
    "A": "·–", "B": "–···", "C": "–·–·", "D": "–··", "E": "·",
    "F": "··–·", "G": "––·", "H": "····", "I": "··", "J": "·–––",
    "K": "–·–", "L": "·–··", "M": "––", "N": "–·", "O": "–––",
    "P": "·––·", "Q": "––·–", "R": "·–·", "S": "···", "T": "–",
    "U": "··–", "V": "···–", "W": "·––", "X": "–··–", "Y": "–·––",
    "Z": "––··",

    # Numbers
    "0": "–––––", "1": "·––––", "2": "··–––", "3": "···––",
    "4": "····–", "5": "·····", "6": "–····", "7": "––···",
    "8": "–––··", "9": "––––·",

    # Common punctuation
    ".": "·–·–·–", ",": "––··––", "?": "··––··", "'": "·––––·",
    "!": "–·–·––", "/": "–··–·", "(": "–·––·", ")": "–·––·–",
    "&": "·–···", ":": "–––···", ";": "–·–·–·", "=": "–···–",
    "+": "·–·–·", "-": "–····–", "_": "··––·–", "\"": "·–··–·",
    "$": "···–··–", "@": "·––·–·"
}

# Reverse dictionary for Morse → Text
reverse_morse_dict = {v: k for k, v in morse_dict.items()}

# Convert Text to Morse Code
def text_to_morse(text):
    msg = ""
    for char in text:
        if char == " ":
            msg += "  "  # double space between words
        else:
            msg += morse_dict.get(char.upper(), "") + " "
    return msg.strip()

# Convert Morse Code to Text
def morse_to_text(morse):
    words = morse.split("  ")  # Morse words separated by double space
    decoded = []
    for word in words:
        letters = word.split(" ")
        decoded_word = "".join([reverse_morse_dict.get(letter, "") for letter in letters])
        decoded.append(decoded_word)
    return " ".join(decoded)

# Main Program
if __name__ == "__main__":
    choice = input("Choose conversion:\n1: Text → Morse\n2: Morse → Text\nEnter 1 or 2: ")
    
    if choice == "1":
        text = input("Enter the message to convert to Morse code: ")
        morse = text_to_morse(text)
        print(f"Morse Code: {morse}")
    
    elif choice == "2":
        morse_input = input("Enter the Morse code (use space between letters, double space between words): ")
        text_output = morse_to_text(morse_input)
        print(f"Decoded Text: {text_output}")
    
    else:
        print("Invalid choice! Please enter 1 or 2.")