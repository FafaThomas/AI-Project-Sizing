import re

def simple_tokenizer(text):
    """
    A simple tokenizer that counts tokens in a given string.
    
    This function considers words, numbers, and punctuation marks as individual tokens.
    It splits the text based on spaces and then further separates any attached punctuation.

    Args:
        text (str): The input string to tokenize.

    Returns:
        tuple: A tuple containing a list of the tokens and the total token count.
    """
    if not isinstance(text, str):
        return [], 0

    # Use a regular expression to find all words, numbers, and punctuation.
    # This pattern matches any sequence of letters, numbers, or a single non-whitespace character.
    tokens = re.findall(r'\b\w+\b|\S', text.strip())
    
    return tokens, len(tokens)

if __name__ == "__main__":
    print("Welcome to the simple tokenizer!")
    print("This program will count the number of tokens in your input.")
    print("To exit, type 'quit' or 'exit'.\n")

    while True:
        user_input = input("Enter text to tokenize: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("Exiting the program. Goodbye!")
            break
        
        tokens, token_count = simple_tokenizer(user_input)
        
        print("\n--- Tokenization Results ---")
        print(f"Original Text: '{user_input}'")
        print(f"Tokens found: {tokens}")
        print(f"Total token count: {token_count}")
        print("----------------------------\n")
