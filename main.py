import threading
import random
import time
import logging

# Constants
GRID_SIZE = 10
NUM_PLAYERS = 10

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("game_log.txt"),
                        logging.StreamHandler()
                    ])

# Helper function to generate all positions
def generate_positions(size):
    return [(x, y) for x in range(size) for y in range(size)]


class Player(threading.Thread):
    def __init__(self, name, hit_event, next_player_lock, next_player=None):
        super().__init__(daemon=True)
        self.name = name
        self.grid = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ship_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
        self.grid[self.ship_position[0]][self.ship_position[1]] = True
        self.hit_event = hit_event
        self.next_player = next_player
        self.alive = True
        self.possible_positions = generate_positions(GRID_SIZE)
        self.next_player_lock = next_player_lock

    def run(self):
        while self.alive:
            # Wait for the signal to take the turn to bomb
            self.hit_event.wait()
            if not self.alive:  # If the player has been hit, exit the loop
                return

            # Select a random position to bomb from possible positions
            bomb_position = random.choice(self.possible_positions)
            print(f"{self.name} bombing {self.next_player.name} at {bomb_position}")
            logging.info(f"{self.name} bombing {self.next_player.name} at {bomb_position}")

            # Bomb the next player and update the list of possible positions
            with self.next_player_lock:
                hit_success = self.next_player.bomb(bomb_position)
                if hit_success:
                    # If next player has been hit, reset possible positions
                    self.possible_positions = generate_positions(GRID_SIZE)
                    self.next_player = self.next_player.next_player
                else:
                    # Remove the missed position from the list of possible positions
                    self.possible_positions.remove(bomb_position)

                # Signal next player to take their turn
                self.next_player.hit_event.set()
                # Reset own event
                self.hit_event.clear()

    def bomb(self, position):
        # Simulate receiving a bomb at the given position
        if position == self.ship_position:
            self.alive = False
            print(f"{self.name} has been hit and is out!")
            logging.info(f"{self.name} has been hit and is out!")
            # Notify the next player to take the turn
            if self.next_player:
                self.next_player.hit_event.set()
            return True
        return False


# Helper function to link the players in a ring
def setup_ring(players):
    for i, player in enumerate(players):
        players[i].next_player = players[(i + 1) % len(players)]


# Helper function to start the game
def start_game(players):
    # Start all player threads
    for player in players:
        player.start()

    # Begin the game by bombing the first player
    players[0].hit_event.set()


player_names = [chr(65+i) for i in range(NUM_PLAYERS)]

hit_events = [threading.Event() for _ in player_names]
next_player_lock = threading.Lock()  # Create a lock for updating next player
players = [Player(name, hit_event, next_player_lock) for name, hit_event in zip(player_names, hit_events)]

setup_ring(players)
start_game(players)

# Wait for the game to end
alive_players = [player for player in players if player.alive]
while len(alive_players) > 1:
    time.sleep(1)
    alive_players = [player for player in players if player.alive]

# At this point, only one player is left alive
winner = alive_players[0]
print(f"Game over. {winner.name} is the winner!")
logging.info(f"Game over. {winner.name} is the winner!")
