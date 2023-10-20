import random

# the deck
def initialize_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Ace']
    deck = [{'suit': suit, 'value': value} for suit in suits for value in values]
    random.shuffle(deck)
    return deck

# Display a player's hand
def display_hand(player):
    print(f"{player['name']}'s hand:")
    for i, card in enumerate(player['hand'], start=1):
        print(f"{i}: {card['value']} of {card['suit']}")
    print()

# Display a player's side deck (show only the top card)
def display_side_deck(player):
    print(f"{player['name']}'s side deck:")
    if player['side_deck']:
        print(f"{player['side_deck'][-1]['value']} of {player['side_deck'][-1]['suit']} (Top Card)")
    else:
        print("Side deck is empty.")
    print()

# Display the cards on the table
def display_table(table):
    print("\nCards on the table:")
    for card in table:
        print(f"{card['value']} of {card['suit']}")

# Check if a player has a card in hand
def has_card_in_hand(player, value):
    return any(card['value'] == value for card in player['hand'])

# Calculate the total points in a player's side deck
def calculate_side_deck_points(player):
    return sum(int(card['value']) for card in player['side_deck'])

# Allow players to play a card, build, hit, or top
def player_turn(player, table, deck, opponent):
    display_hand(player)
    display_table(table)
    display_side_deck(player)

    while True:
        choice = input(f"{player['name']}, choose an action:\n1: Play a card\n2: Build with a card on the table\n3: Hit and take a card from the table\n4: Top with a matching card\nEnter your choice: ")
        try:
            choice = int(choice)
            if choice == 1:
                play_card(player, table)
                break
            elif choice == 2:
                build_card(player, table)
                break
            elif choice == 3:
                hit_card(player, table, deck)
                break
            elif choice == 4:
                top_card(player, table, opponent)
                break
            else:
                print("Invalid choice. Please choose a valid action.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Allow players to play a card
def play_card(player, table):
    while True:
        choice = input(f"{player['name']}, choose a card to play (enter the card's position, e.g., 1, 2, 3, 4): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(player['hand']):
                card_to_play = player['hand'].pop(choice - 1)
                table.append(card_to_play)
                print(f"{player['name']} played {card_to_play['value']} of {card_to_play['suit']} on the table.\n")
                break
            else:
                print("Invalid choice. Please choose a valid card.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# Allow players to build with a card on the table
def build_card(player, table):
    display_table(table)

    while True:
        build_choice = input(f"{player['name']}, choose an action:\n1: Build with a card on the table\n2: Cancel build\nEnter your choice: ")

        if build_choice == '1':
            # choose the number they want to build
            while True:
                build_value = input(f"{player['name']}, enter the total value you want to build (e.g., 10): ")

                try:
                    build_value = int(build_value)

                    if not has_card_in_hand(player, str(build_value)):
                        print(f"{player['name']}, you don't have a {build_value} in your hand. You can't build this.")
                        break

                    possible_builds = []

                    # Find possible builds using cards from the table and the player's hand
                    for i in range(len(table)):
                        for j in range(len(player['hand'])):
                            total_value = int(table[i]['value']) + int(player['hand'][j]['value'])
                            if total_value == build_value:
                                possible_builds.append((i, j))

                    if not possible_builds:
                        print("No valid builds found.")
                        break

                    print("Possible builds:")
                    for idx, (table_card_idx, hand_card_idx) in enumerate(possible_builds, start=1):
                        print(f"{idx}: Build {table[table_card_idx]['value']} and {player['hand'][hand_card_idx]['value']}")

                    build_choice = input("Choose a build from the options above (enter the corresponding number, e.g., 1): ")
                    build_choice = int(build_choice) - 1

                    if 0 <= build_choice < len(possible_builds):
                        table_card_idx, hand_card_idx = possible_builds[build_choice]
                        build_cards = [table.pop(table_card_idx), player['hand'].pop(hand_card_idx)]
                        player['hand'].extend(build_cards)
                        print(f"{player['name']} built {build_value} with {build_cards[0]['value']} and {build_cards[1]['value']}.\n")

                        # Check if there is a card of the same value on the table and allow building on top of it
                        for card_idx, card_on_table in enumerate(table):
                            if card_on_table['value'] == str(build_value):
                                build_cards_on_top = player['hand'][:1]  # You can build with the first 2 cards in hand
                                if len(build_cards_on_top) == 2:
                                    table.pop(card_idx)
                                    player['hand'] = player['hand'][2:]
                                    table.extend(build_cards_on_top)
                                    print(f"{player['name']} built on top of {card_on_table['value']}.\n")
                                    break

                        break

                    else:
                        print("Invalid choice. Please choose a valid build.")

                except ValueError:
                    print("Invalid input. Please enter a valid number.")
        elif build_choice == '2':
            print("Build canceled.\n")
            break
        else:
            print("Invalid choice. Please choose a valid action (1 or 2).")


# Allow a player to hit and take a card from the table
def hit_card(player, table, deck):
    if table:
        card_to_hit = random.choice(table)
        table.remove(card_to_hit)
        player['side_deck'].append(card_to_hit)  # Add to the side deck, not hand
        print(f"{player['name']} hit and took {card_to_hit['value']} of {card_to_hit['suit']} from the table to their side deck.\n")
    else:
        print("The table is empty. You cannot hit.")

# Allow a player to top with a matching card
def top_card(player, table, opponent):
    if table:
        matching_card = None
        for card in table:
            if has_card_in_hand(player, card['value']):
                matching_card = card
                break

        if matching_card:
            table.remove(matching_card)
            player['side_deck'].append(matching_card)  # Add to the side deck, not hand
            print(f"{player['name']} topped with a matching {matching_card['value']} from the table to their side deck.\n")
        else:
            print(f"{player['name']} can't top because there is no matching card in their hand.\n")
    else:
        print("The table is empty. You cannot top.")

# Computer player to play a card (randomly)
def computer_play(player, table):
    if player['hand']:
        card_to_play = random.choice(player['hand'])
        player['hand'].remove(card_to_play)
        table.append(card_to_play)
        print(f"{player['name']} played {card_to_play['value']} of {card_to_play['suit']} (Computer)\n")

# Set Up the Deck
deck = initialize_deck()

# Welcome Players and Get Their Names
print("Welcome to Alliance Casino!")
player_name = input("Player, please enter your name: ")
computer_name = "Computer"

# Deal 20 Cards to Each Player
num_cards_to_deal = 20  # Adjust the number of cards to deal

players = [{'name': player_name, 'hand': [], 'side_deck': []}, {'name': computer_name, 'hand': [], 'side_deck': []}]

while len(deck) >= num_cards_to_deal * len(players):
    for _ in range(num_cards_to_deal):
        for player in players:
            card = deck.pop()
            player['hand'].append(card)

# Main Game Loop
table = []
player = players[0]
computer = players[1]

while player['hand']:
    if player == players[0]:
        player_turn(player, table, deck, computer)
        player = players[1]
    else:
        computer_play(player, table)
        player = players[0]

    display_table(table)

# Show Result
display_table(table)

# Determine the Winner based on side deck points
player_points = calculate_side_deck_points(players[0])
computer_points = calculate_side_deck_points(players[1])

if player_points > computer_points:
    print(f"{player_name} wins with {player_points} points in the side deck!")
elif player_points < computer_points:
    print(f"{computer_name} wins with {computer_points} points in the side deck!")
else:
    print("It's a tie!")

# Display remaining cards in each player's hand and side deck
display_hand(players[0])
display_side_deck(players[0])
display_hand(players[1])
display_side_deck(players[1])
