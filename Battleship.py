import random
import time
import os

# מחלקת עיצוב מתקדמת
class Style:
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    CLEAR = '\033[H\033[J'

class ProfessionalBattleship:
    def __init__(self):
        self.size = 15
        self.ship_size = 3
        self.max_missiles = 8
        self.radar_uses = 2
        self.board = ["_"] * self.size
        # מיקום ספינה רב-תאית (רצף של תאים)
        start_pos = random.randint(0, self.size - self.ship_size)
        self.ship_coords = set(range(start_pos, start_pos + self.ship_size))
        self.hits = set()
        self.misses = set()
        self.score = 0

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_header(self):
        print(f"{Style.MAGENTA}{'='*45}")
        print(f"{Style.BOLD}   B A T T L E S H I P :  D E E P  S E A   ")
        print(f"{Style.MAGENTA}{'='*45}{Style.RESET}")
        
        # תצוגת סטטוס
        status = f"Missiles: {Style.RED}{'🚀' * (self.max_missiles - len(self.misses))}{Style.RESET}"
        radars = f"Radars: {Style.CYAN}{'📡' * self.radar_uses}{Style.RESET}"
        print(f"{status}  |  {radars}  |  Hits: {len(self.hits)}/{self.ship_size}")
        print("-" * 45)

    def draw_board(self, reveal=False):
        display = []
        for i in range(self.size):
            if i in self.hits:
                display.append(f"{Style.RED}X{Style.RESET}")
            elif i in self.misses:
                display.append(f"{Style.YELLOW}O{Style.RESET}")
            elif reveal and i in self.ship_coords:
                display.append(f"{Style.GREEN}S{Style.RESET}")
            else:
                display.append(f"{Style.CYAN}_{Style.RESET}")
        
        print("\nIndex: " + " ".join(f"{i:2}" for i in range(self.size)))
        print("Board: " + "  ".join(display) + "\n")

    def use_radar(self, center):
        """סורק רדיוס של תא אחד מסביב לניחוש"""
        self.radar_uses -= 1
        found = False
        scan_range = range(max(0, center-1), min(self.size, center+2))
        for i in scan_range:
            if i in self.ship_coords:
                found = True
        return found

    def fire_missile(self, target):
        print(f"\n{Style.BOLD}Launching Missile...{Style.RESET}", end="", flush=True)
        for _ in range(3):
            time.sleep(0.3)
            print(".", end="", flush=True)
        
        if target in self.ship_coords:
            self.hits.add(target)
            return f"\n{Style.GREEN}{Style.BOLD}DIRECT HIT!{Style.RESET}"
        else:
            self.misses.add(target)
            return f"\n{Style.RED}Splash... Miss.{Style.RESET}"

    def run(self):
        while len(self.misses) < self.max_missiles and len(self.hits) < self.ship_size:
            self.clear_screen()
            self.draw_header()
            self.draw_board()

            choice = input(f"Choose action: ({Style.BOLD}F{Style.RESET}ire / {Style.BOLD}R{Style.RESET}adar): ").lower()

            if choice == 'r' and self.radar_uses > 0:
                try:
                    target = int(input("Where to scan? "))
                    if self.use_radar(target):
                        print(f"{Style.GREEN}Radar detected metal in the area!{Style.RESET}")
                    else:
                        print(f"{Style.BLUE}Area is clear. Nothing found.{Style.RESET}")
                    time.sleep(2)
                except ValueError: pass
                continue

            try:
                target = int(input("Enter target coordinate: "))
                if not (0 <= target < self.size) or target in self.hits or target in self.misses:
                    print("Invalid target or already hit.")
                    time.sleep(1)
                    continue

                result = self.fire_missile(target)
                print(result)
                time.sleep(1.5)

            except ValueError:
                continue

        self.end_game()

    def end_game(self):
        self.clear_screen()
        self.draw_header()
        self.draw_board(reveal=True)
        if len(self.hits) == self.ship_size:
            print(f"{Style.GREEN}{Style.BOLD}MISSION ACCOMPLISHED! Enemy fleet destroyed.{Style.RESET}")
        else:
            print(f"{Style.RED}{Style.BOLD}MISSION FAILED. You ran out of ammo.{Style.RESET}")

if __name__ == "__main__":
    game = ProfessionalBattleship()
    game.run()