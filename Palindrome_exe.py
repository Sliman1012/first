import string

def clean_text(text):
    """Remove spaces, punctuation and convert to lowercase."""
    try:
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        # Remove punctuation and spaces, then convert to lowercase
        cleaned = ''.join(char.lower() for char in text 
                         if char not in string.punctuation and char != ' ')
        return cleaned
    except TypeError as e:
        print(f"Error: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error in clean_text: {e}")
        return ""

def is_palindrome(text):
    """Check if the cleaned text is a palindrome."""
    try:
        if not text:
            raise ValueError("Cannot check empty text")
        
        # Check if input contains only digits
        if text.strip().isdigit():
            raise ValueError("Numbers are not allowed. Please enter text with letters.")
        
        cleaned = clean_text(text)
        
        if not cleaned:
            raise ValueError("No valid characters to check after cleaning")
        
        # Check if cleaned text has at least one letter
        if not any(c.isalpha() for c in cleaned):
            raise ValueError("Input must contain at least one letter")
        
        return cleaned == cleaned[::-1]
    except ValueError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error in is_palindrome: {e}")
        return False

def check_and_display(text, palindrome_count, encouragement_messages):
    """Check palindrome and display original, cleaned text, and result."""
    try:
        if not text:
            raise ValueError("Cannot check empty text")
        
        # Check if input contains only digits
        if text.strip().isdigit():
            print("Error: Numbers are not allowed. Please enter text with letters.\n")
            return None
        
        cleaned = clean_text(text)
        
        if not cleaned:
            print("Error: No valid characters to check after cleaning\n")
            return None
        
        # Check if cleaned text has at least one letter
        if not any(c.isalpha() for c in cleaned):
            print("Error: Input must contain at least one letter\n")
            return None
        
        # Check palindrome
        is_palin = cleaned == cleaned[::-1]
        
        # Display results
        print(f"Original input: '{text}'")
        print(f"Cleaned text: '{cleaned}'")
        
        if is_palin:
            print(f"Result: '{text}' is a Palindrome ✓")
            
            # Show different encouragement based on count (max 5)
            if palindrome_count < len(encouragement_messages):
                print(encouragement_messages[palindrome_count])
            else:
                # After 5, show a repeating message
                print("🌟 Another palindrome! You're absolutely incredible! 🎉\n")
            
            return {'input': text, 'cleaned': cleaned, 'result': 'Palindrome'}
        else:
            print(f"Result: '{text}' is Not a palindrome ✗\n")
            return {'input': text, 'cleaned': cleaned, 'result': 'Not palindrome'}
            
    except Exception as e:
        print(f"Error: {e}\n")
        return None

def main():
    """Main loop to check palindromes until user exits."""
    print("=" * 50)
    print("Palindrome Checker")
    print("=" * 50)
    print("Type 'exit' or 'quit' to stop")
    print("Type 'history' to see all checks\n")
    
    # List to store history of checks
    history = []
    
    # Counter for correct palindromes found
    palindrome_count = 0
    
    # Different encouragement messages
    encouragement_messages = [
        "🎉 Awesome! You found a palindrome! 🌟\n💪 Keep it up, you're doing great! 🚀\n",
        "🔥 Amazing! Another palindrome! 🎊\n⭐ You're on fire! Keep going! 💫\n",
        "🏆 Incredible! Three palindromes! 🎯\n🌈 You're a palindrome master! 🚀\n",
        "💎 Outstanding! Four palindromes! 👑\n🎪 You're unstoppable! Keep crushing it! 🎸\n",
        "🎖️ LEGENDARY! Five palindromes! 🏅\n🦸 You're officially a Palindrome Champion! 👏🎉\n"
    ]
    
    try:
        while True:
            try:
                user_input = input("Enter text to check: ")
                
                # Check for exit condition
                if user_input.lower() in ['exit', 'quit']:
                    print("\nGoodbye!")
                    break
                
                # Check for history command
                if user_input.lower() == 'history':
                    if not history:
                        print("No checks yet.\n")
                    else:
                        print("\n" + "=" * 50)
                        print("HISTORY OF CHECKS")
                        print("=" * 50)
                        for i, record in enumerate(history, 1):
                            print(f"{i}. Original: '{record['input']}'")
                            print(f"   Cleaned: '{record['cleaned']}'")
                            print(f"   Result: {record['result']}\n")
                        print("=" * 50 + "\n")
                    continue
                
                # Check for empty input
                if not user_input.strip():
                    print("Warning: Empty input. Please enter some text.\n")
                    continue
                
                # Check if palindrome
                result_obj = check_and_display(user_input, palindrome_count, encouragement_messages)
                
                # Add to history only if check was successful
                if result_obj:
                    history.append(result_obj)
                    # Increment counter if it was a palindrome
                    if result_obj['result'] == 'Palindrome':
                        palindrome_count += 1
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user. Exiting...")
                break
            except EOFError:
                print("\n\nEnd of input detected. Exiting...")
                break
            except Exception as e:
                print(f"Unexpected error in main loop: {e}")
                print("Continuing...\n")
    
    finally:
        # Show final summary
        print("\n" + "=" * 50)
        print(f"Total checks performed: {len(history)}")
        print(f"Palindromes found: {palindrome_count} 🎯")
        if history:
            print("\nYour checks:")
            for i, record in enumerate(history, 1):
                print(f"{i}. '{record['input']}' → cleaned: '{record['cleaned']}' → {record['result']}")
        print("=" * 50)
        print("Thank you for using Palindrome Checker!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        print("Program terminated.")