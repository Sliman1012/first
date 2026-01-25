import string
import time
import json
from datetime import datetime

# ANSI color codes for terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_logo():
    """Print ASCII art logo."""
    logo = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════╗
    ║                                                   ║
    ║     ██████   █████  ██      ██ ███    ██ ██████  ║
    ║     ██   ██ ██   ██ ██      ██ ████   ██ ██   ██ ║
    ║     ██████  ███████ ██      ██ ██ ██  ██ ██   ██ ║
    ║     ██      ██   ██ ██      ██ ██  ██ ██ ██   ██ ║
    ║     ██      ██   ██ ███████ ██ ██   ████ ██████  ║
    ║                                                   ║
    ║            🎯 PALINDROME CHECKER 🎯              ║
    ║                                                   ║
    ╚═══════════════════════════════════════════════════╝
{Colors.END}
    """
    print(logo)

def loading_animation(text="Checking"):
    """Show a loading animation."""
    for i in range(3):
        print(f"\r{Colors.YELLOW}{text}{'.' * (i + 1)}   {Colors.END}", end='', flush=True)
        time.sleep(0.3)
    print("\r" + " " * 50 + "\r", end='')  # Clear the line

def clean_text(text):
    """Remove spaces, punctuation and convert to lowercase."""
    try:
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        cleaned = ''.join(char.lower() for char in text 
                         if char not in string.punctuation and char != ' ')
        return cleaned
    except TypeError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return ""
    except Exception as e:
        print(f"{Colors.RED}Unexpected error in clean_text: {e}{Colors.END}")
        return ""

def is_palindrome(text):
    """Check if the cleaned text is a palindrome."""
    try:
        if not text:
            raise ValueError("Cannot check empty text")
        
        if text.strip().isdigit():
            raise ValueError("Numbers are not allowed. Please enter text with letters.")
        
        cleaned = clean_text(text)
        
        if not cleaned:
            raise ValueError("No valid characters to check after cleaning")
        
        if not any(c.isalpha() for c in cleaned):
            raise ValueError("Input must contain at least one letter")
        
        return cleaned == cleaned[::-1]
    except ValueError as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}")
        return False
    except Exception as e:
        print(f"{Colors.RED}Unexpected error in is_palindrome: {e}{Colors.END}")
        return False

def get_palindrome_hint(text, cleaned):
    """Suggest how to make it a palindrome."""
    if len(cleaned) <= 2:
        return f"{Colors.YELLOW}💡 Hint: Try adding '{cleaned[::-1]}' at the end!{Colors.END}"
    return f"{Colors.YELLOW}💡 Hint: To make it palindrome, you could try: '{cleaned + cleaned[::-1]}'{Colors.END}"

def check_and_display(text, palindrome_count, encouragement_messages, stats):
    """Check palindrome and display original, cleaned text, and result."""
    try:
        if not text:
            raise ValueError("Cannot check empty text")
        
        if text.strip().isdigit():
            print(f"{Colors.RED}Error: Numbers are not allowed. Please enter text with letters.{Colors.END}\n")
            return None
        
        cleaned = clean_text(text)
        
        if not cleaned:
            print(f"{Colors.RED}Error: No valid characters to check after cleaning{Colors.END}\n")
            return None
        
        if not any(c.isalpha() for c in cleaned):
            print(f"{Colors.RED}Error: Input must contain at least one letter{Colors.END}\n")
            return None
        
        # Show loading animation
        loading_animation("Checking")
        
        # Check palindrome
        is_palin = cleaned == cleaned[::-1]
        
        # Display results with colors
        print(f"{Colors.CYAN}Original input: {Colors.BOLD}'{text}'{Colors.END}")
        print(f"{Colors.CYAN}Cleaned text: {Colors.BOLD}'{cleaned}'{Colors.END}")
        
        if is_palin:
            print(f"{Colors.GREEN}{Colors.BOLD}Result: '{text}' is a Palindrome ✓{Colors.END}")
            
            # Update stats
            stats['longest'] = max(stats.get('longest', ''), cleaned, key=len)
            stats['shortest'] = min(stats.get('shortest', cleaned), cleaned, key=len) if stats.get('shortest') else cleaned
            
            # Show different encouragement based on count
            if palindrome_count < len(encouragement_messages):
                print(f"{Colors.GREEN}{encouragement_messages[palindrome_count]}{Colors.END}")
            else:
                print(f"{Colors.GREEN}🌟 Another palindrome! You're absolutely incredible! 🎉{Colors.END}\n")
            
            return {'input': text, 'cleaned': cleaned, 'result': 'Palindrome', 'timestamp': datetime.now().strftime("%H:%M:%S")}
        else:
            print(f"{Colors.RED}{Colors.BOLD}Result: '{text}' is Not a palindrome ✗{Colors.END}")
            print(get_palindrome_hint(text, cleaned))
            print()
            return {'input': text, 'cleaned': cleaned, 'result': 'Not palindrome', 'timestamp': datetime.now().strftime("%H:%M:%S")}
            
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.END}\n")
        return None

def print_table_history(history):
    """Print history in a nice table format."""
    if not history:
        print(f"{Colors.YELLOW}No checks yet.{Colors.END}\n")
        return
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*90}")
    print(f"{'#':<4} {'Time':<10} {'Original':<25} {'Cleaned':<25} {'Result':<15}")
    print(f"{'='*90}{Colors.END}")
    
    for i, record in enumerate(history, 1):
        result_color = Colors.GREEN if record['result'] == 'Palindrome' else Colors.RED
        print(f"{Colors.BOLD}{i:<4}{Colors.END} {record['timestamp']:<10} {record['input']:<25} {record['cleaned']:<25} {result_color}{record['result']:<15}{Colors.END}")
    
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*90}{Colors.END}\n")

def save_history_to_file(history):
    """Save history to a JSON file."""
    try:
        filename = f"palindrome_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        print(f"{Colors.GREEN}✅ History saved to {filename}{Colors.END}\n")
    except Exception as e:
        print(f"{Colors.RED}Error saving file: {e}{Colors.END}\n")

def print_statistics(history, palindrome_count, stats):
    """Print detailed statistics."""
    if not history:
        return
    
    total = len(history)
    success_rate = (palindrome_count / total * 100) if total > 0 else 0
    
    print(f"\n{Colors.CYAN}{Colors.BOLD}📊 STATISTICS 📊{Colors.END}")
    print(f"{Colors.CYAN}{'='*50}{Colors.END}")
    print(f"{Colors.BOLD}Total checks:{Colors.END} {total}")
    print(f"{Colors.GREEN}{Colors.BOLD}Palindromes found:{Colors.END} {palindrome_count} 🎯")
    print(f"{Colors.RED}{Colors.BOLD}Not palindromes:{Colors.END} {total - palindrome_count}")
    print(f"{Colors.YELLOW}{Colors.BOLD}Success rate:{Colors.END} {success_rate:.1f}%")
    
    if stats.get('longest'):
        print(f"{Colors.BLUE}{Colors.BOLD}Longest palindrome:{Colors.END} '{stats['longest']}' ({len(stats['longest'])} chars)")
    if stats.get('shortest'):
        print(f"{Colors.BLUE}{Colors.BOLD}Shortest palindrome:{Colors.END} '{stats['shortest']}' ({len(stats['shortest'])} chars)")
    
    print(f"{Colors.CYAN}{'='*50}{Colors.END}\n")

def main():
    """Main loop to check palindromes until user exits."""
    print_logo()
    
    print(f"{Colors.YELLOW}{Colors.BOLD}Commands:{Colors.END}")
    print(f"  • Type {Colors.GREEN}'exit'{Colors.END} or {Colors.GREEN}'quit'{Colors.END} to stop")
    print(f"  • Type {Colors.BLUE}'history'{Colors.END} to see all checks")
    print(f"  • Type {Colors.BLUE}'stats'{Colors.END} to see statistics")
    print(f"  • Type {Colors.BLUE}'save'{Colors.END} to save history to file")
    print(f"  • Type {Colors.BLUE}'clear'{Colors.END} to clear history\n")
    
    history = []
    palindrome_count = 0
    stats = {}
    
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
                user_input = input(f"{Colors.BOLD}Enter text to check: {Colors.END}")
                
                if user_input.lower() in ['exit', 'quit']:
                    print(f"\n{Colors.CYAN}Goodbye! 👋{Colors.END}")
                    break
                
                if user_input.lower() == 'history':
                    print_table_history(history)
                    continue
                
                if user_input.lower() == 'stats':
                    print_statistics(history, palindrome_count, stats)
                    continue
                
                if user_input.lower() == 'save':
                    save_history_to_file(history)
                    continue
                
                if user_input.lower() == 'clear':
                    history.clear()
                    palindrome_count = 0
                    stats.clear()
                    print(f"{Colors.GREEN}✅ History cleared!{Colors.END}\n")
                    continue
                
                if not user_input.strip():
                    print(f"{Colors.YELLOW}Warning: Empty input. Please enter some text.{Colors.END}\n")
                    continue
                
                result_obj = check_and_display(user_input, palindrome_count, encouragement_messages, stats)
                
                if result_obj:
                    history.append(result_obj)
                    if result_obj['result'] == 'Palindrome':
                        palindrome_count += 1
                        
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Program interrupted by user. Exiting...{Colors.END}")
                break
            except EOFError:
                print(f"\n\n{Colors.YELLOW}End of input detected. Exiting...{Colors.END}")
                break
            except Exception as e:
                print(f"{Colors.RED}Unexpected error in main loop: {e}{Colors.END}")
                print(f"{Colors.YELLOW}Continuing...{Colors.END}\n")
    
    finally:
        print_statistics(history, palindrome_count, stats)
        
        if history:
            print(f"{Colors.CYAN}{Colors.BOLD}Your checks:{Colors.END}")
            for i, record in enumerate(history, 1):
                result_color = Colors.GREEN if record['result'] == 'Palindrome' else Colors.RED
                print(f"{i}. '{record['input']}' → cleaned: '{record['cleaned']}' → {result_color}{record['result']}{Colors.END}")
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*50}")
        print(f"Thank you for using Palindrome Checker! 🎉")
        print(f"{'='*50}{Colors.END}\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Colors.RED}Fatal error: {e}{Colors.END}")
        print("Program terminated.")