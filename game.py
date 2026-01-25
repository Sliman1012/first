import random

def print_board(board):
    print(f"\n {board[0]} | {board[1]} | {board[2]} ")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]} \n")

def check_winner(board):
    win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] != " ":
            return board[a]
    if " " not in board:
        return "Tie"
    return None

def main():
    board = [" "] * 9
    
    print("--- Welcome to Tic-Tac-Toe! ---")
    
    # User chooses their side
    user_choice = ""
    while user_choice not in ["X", "O"]:
        user_choice = input("Do you want to be X or O? ").upper()
    
    computer_choice = "O" if user_choice == "X" else "X"
    current_turn = "X"  # X always starts
    
    print(f"You are {user_choice}. Computer is {computer_choice}.")
    print("Positions are 0-8.")

    while True:
        print_board(board)
        result = check_winner(board)
        
        if result:
            if result == "Tie":
                print("It's a draw!")
            else:
                print(f"Winner is: {result}!")
            break

        if current_turn == user_choice:
            # User Move
            try:
                move = int(input(f"Your turn ({user_choice}). Choose (0-8): "))
                if board[move] != " ":
                    print("Taken! Try again.")
                    continue
                board[move] = user_choice
                current_turn = computer_choice
            except (ValueError, IndexError):
                print("Invalid input. Enter 0-8.")
        else:
            # Computer Move (Random)
            print(f"Computer ({computer_choice}) is thinking...")
            available_moves = [i for i, val in enumerate(board) if val == " "]
            move = random.choice(available_moves)
            board[move] = computer_choice
            current_turn = user_choice

if __name__ == "__main__":
    main()