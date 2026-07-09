import random

# ==========================================
# 1. CLASSES & CONSTANTS
# ==========================================

# Mapping card faces to numeric values to prevent the 'Ace' crash
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
    '7': 7, '8': 8, '9': 9, '10': 10, 'Ace': 1
}

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.numeric_value = CARD_VALUES[value] # Pre-calculate to avoid int() crashes

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Player:
    def __init__(self, name, is_computer=False):
        self.name = name
        self.hand = []
        self.side_deck = []
        self.is_computer = is_computer

    def get_points(self):
        return sum(card.numeric_value for card in self.side_deck)

# ==========================================
# 2. HELPER & DISPLAY FUNCTIONS
# ==========================================

def initialize_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = list(CARD_VALUES.keys())
    deck = [Card(suit, value) for suit in suits for value in values]
    random.shuffle(deck)
    return deck

def get_valid_int(prompt, min_val, max_val):
    """Helper to cleanly handle user input without repeating try/except blocks."""
    while True:
        try:
            choice = int(input(prompt))
            if min_val <= choice <= max_val:
                return choice
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def display_hand(player):
    print(f"\n--- {player.name}'s Hand ---")
    for i, card in enumerate(player.hand, start=1):
        print(f"{i}: {card}")
    print("-" * 25)

def display_table(table):
    print("\n[ TABLE ]")
    if not table:
        print("The table is empty.")
    else:
        for i, card in enumerate(table, start=1):
            print(f"{i}: {card}")
    print("-" * 25)

def display_side_deck(player):
    points = player.get_points()
    print(f"{player.name}'s Side Deck: {len(player.side_deck)} cards ({points} points)")

# ==========================================
# 3. GAME MECHANICS
# ==========================================

def human_turn(player, table, last_capture_player):
    display_hand(player)
    display_table(table)
    
    # Determine available actions
    can_capture_match = False
    can_capture_sum = False
    
    # Check if we can capture a single matching card
    for h_card in player.hand:
        for t_card in table:
            if h_card.numeric_value == t_card.numeric_value:
                can_capture_match = True
                break
                
    # Check if we can capture a sum of exactly 2 cards
    for h_card in player.hand:
        for i in range(len(table)):
            for j in range(i + 1, len(table)):
                if table[i].numeric_value + table[j].numeric_value == h_card.numeric_value:
                    can_capture_sum = True
                    break

    print("\nActions:")
    print("1: Play a card to the table")
    if can_capture_match:
        print("2: Capture a single matching card")
    if can_capture_sum:
        print("3: Capture a sum of two cards")
        
    max_action = 1
    if can_capture_sum: max_action = 3
    elif can_capture_match: max_action = 2

    action = get_valid_int("Choose an action: ", 1, max_action)

    if action == 1:
        # PLAY A CARD
        card_idx = get_valid_int("Choose a card from your hand to play: ", 1, len(player.hand))
        played_card = player.hand.pop(card_idx - 1)
        table.append(played_card)
        print(f"{player.name} played {played_card} to the table.")

    elif action == 2:
        # CAPTURE SINGLE MATCH
        print("Choose the card from your hand to capture with:")
        hand_idx = get_valid_int("Hand card: ", 1, len(player.hand))
        hand_card = player.hand[hand_idx - 1]
        
        # Find valid table cards
        valid_table_cards = [i+1 for i, t in enumerate(table) if t.numeric_value == hand_card.numeric_value]
        print(f"Choose the matching card on the table ({valid_table_cards}):")
        table_idx = get_valid_int("Table card: ", min(valid_table_cards), max(valid_table_cards))
        
        table_card = table.pop(table_idx - 1)
        player.hand.remove(hand_card)
        player.side_deck.extend([hand_card, table_card])
        print(f"{player.name} captured {table_card} with {hand_card}!")
        last_capture_player = player

    elif action == 3:
        # CAPTURE SUM
        print("Choose the card from your hand to capture with:")
        hand_idx = get_valid_int("Hand card: ", 1, len(player.hand))
        hand_card = player.hand[hand_idx - 1]
        
        print("Choose the FIRST card on the table to sum:")
        t1_idx = get_valid_int("Table card 1: ", 1, len(table))
        
        print("Choose the SECOND card on the table to sum:")
        t2_idx = get_valid_int("Table card 2: ", 1, len(table))
        while t2_idx == t1_idx:
            print("You must choose a different card for the second choice.")
            t2_idx = get_valid_int("Table card 2: ", 1, len(table))

        # Validate the sum
        card1 = table[t1_idx - 1]
        card2 = table[t2_idx - 1]
        if card1.numeric_value + card2.numeric_value == hand_card.numeric_value:
            # Remove cards (remove higher index first to avoid shifting issues)
            for idx in sorted([t1_idx - 1, t2_idx - 1], reverse=True):
                table.pop(idx)
            player.hand.remove(hand_card)
            player.side_deck.extend([hand_card, card1, card2])
            print(f"{player.name} captured {card1} and {card2} (sum {card1.numeric_value + card2.numeric_value}) with {hand_card}!")
            last_capture_player = player
        else:
            print("Invalid sum! Those cards don't match your hand card. Turn wasted, playing card instead.")
            table.append(player.hand.pop(hand_idx - 1))

    return last_capture_player

def computer_turn(player, table, last_capture_player):
    print(f"\n--- {player.name}'s Turn ---")
    
    # 1. Try to capture a single match
    for h_card in player.hand:
        for t_card in table:
            if h_card.numeric_value == t_card.numeric_value:
                table.remove(t_card)
                player.hand.remove(h_card)
                player.side_deck.extend([h_card, t_card])
                print(f"Computer captured {t_card} with {h_card}.")
                return player # Return self as last capture player

    # 2. Try to capture a sum of 2 cards
    for h_card in player.hand:
        for i in range(len(table)):
            for j in range(i + 1, len(table)):
                if table[i].numeric_value + table[j].numeric_value == h_card.numeric_value:
                    card1, card2 = table[i], table[j]
                    table.remove(card1)
                    table.remove(card2)
                    player.hand.remove(h_card)
                    player.side_deck.extend([h_card, card1, card2])
                    print(f"Computer captured {card1} and {card2} (sum {card1.numeric_value + card2.numeric_value}) with {h_card}.")
                    return player

    # 3. If no captures possible, play the lowest value card
    player.hand.sort(key=lambda c: c.numeric_value)
    played_card = player.hand.pop(0)
    table.append(played_card)
    print(f"Computer played {played_card} to the table.")
    
    return last_capture_player

# ==========================================
# 4. MAIN GAME LOOP
# ==========================================

def main():
    print("=" * 30)
    print("Welcome to Alliance Casino!")
    print("=" * 30)
    
    player_name = input("Player, please enter your name: ")
    
    # Setup Players and Deck
    deck = initialize_deck()
    human = Player(player_name)
    computer = Player("Computer", is_computer=True)
    players = [human, computer]
    
    # Deal 20 cards to each player (40 card deck total)
    for _ in range(20):
        for p in players:
            p.hand.append(deck.pop())
            
    table = []
    current_player_idx = 0
    last_capture_player = None # Tracks who gets the leftover cards at the end

    # Game Loop
    while any(len(p.hand) > 0 for p in players):
        current_player = players[current_player_idx]
        
        print(f"\n{'='*15} {current_player.name}'s Turn {'='*15}")
        
        if not current_player.is_computer:
            last_capture_player = human_turn(current_player, table, last_capture_player)
        else:
            last_capture_player = computer_turn(current_player, table, last_capture_player)
            
        # Switch turns
        current_player_idx = 1 - current_player_idx

    # End Game: Sweep leftover table cards
    if table:
        print("\n--- End of Round Sweep ---")
        if last_capture_player:
            print(f"{last_capture_player.name} made the last capture and sweeps the remaining {len(table)} cards from the table!")
            last_capture_player.side_deck.extend(table)
        else:
            print("No captures were made. Cards remain on the table.")
        table = []

    # Calculate and Display Results
    print("\n" + "=" * 30)
    print("GAME OVER - FINAL RESULTS")
    print("=" * 30)
    
    for p in players:
        points = p.get_points()
        display_side_deck(p)
        
    human_points = human.get_points()
    comp_points = computer.get_points()
    
    if human_points > comp_points:
        print(f"\n {human.name} WINS! 🎉")
    elif comp_points > human_points:
        print(f"\n🤖 {computer.name} WINS! 🤖")
    else:
        print("\n🤝 It's a TIE! 🤝")

if __name__ == "__main__":
    main()