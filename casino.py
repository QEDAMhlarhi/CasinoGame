import random
import time

#display a player's hand
def display_hand(player):
    print(f"{player['name']}'s hand:")
    for i, card in enumerate(player['hand'], start=1):
        print(f"{i}: {card['value']} of {card['suit']}")
    print()

#display a player's side deck (show only the top card)
def display_side_deck(player):
    print(f"{player['name']}'s side deck:")
    if player['side_deck']:
        print(f"{player['side_deck'][-1]['value']} of {player['side_deck'][-1]['suit']} (Top Card)")
    else:
        print("Side deck is empty.")
    print()

#display the cards on the table
def display_table(table):
    print("\nCards on the table:")
    for card in table:
        print(f"{card['value']} of {card['suit']}")

#check if a player has a card in hand
def has_card_in_hand(player, value):
    return any(card['value'] == value for card in player['hand'])

#calculate the total points in a player's side deck
def calculate_side_deck_points(player):
    return sum(int(card['value']) for card in player['side_deck'])

#allow a player to play a card, build, hit, or top
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

#allow a player to play a card
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

#allow a player to build with a card on the table
def build_card(player, table):
    display_table(table)
    build_value = input(f"{player['name']}, enter the total value you want to build (e.g., 10): ")
    
    try:
        build_value = int(build_value)
        
        if not has_card_in_hand(player, str(build_value)):
            print(f"You don't have a {build_value} in your hand. You can't build this.")
            return

        possible_builds = []

        # 
        for i in range(len(table)):
            for j in range(i + 1, len(table)):
                if table[i]['value'] != table[j]['value']:
                    total_value = int(table[i]['value']) + int(table[j]['value'])
                    total_value_ = table[j]['value']
                    print(total_value_,total_value)
                    if total_value == build_value:
                        possible_builds.append((i, j))

        if not possible_builds:
            print("No valid builds found.")
            return

        print("Possible builds on the table:")
        for idx, (card1_idx, card2_idx) in enumerate(possible_builds, start=1):
            print(f"{idx}: Build {table[card1_idx]['value']} and {table[card2_idx]['value']}")

        build_choice = input("Choose a build from the options above (enter the corresponding number, e.g., 1): ")
        build_choice = int(build_choice) - 1

        if 0 <= build_choice < len(possible_builds):
            card1_idx, card2_idx = possible_builds[build_choice]
            build_cards = [table.pop(card1_idx), table.pop(card2_idx - 1)]
            player['hand'].extend(build_cards)
            print(f"{player['name']} built {build_value} with {build_cards[0]['value']} and {build_cards[1]['value']}.\n")
        else:
            print("Invalid choice. Please choose a valid build.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")

#allow a player to hit and take a card from the table
def hit_card(player, table, deck):
    if table:
        card_to_hit = random.choice(table)
        table.remove(card_to_hit)
        player['side_deck'].append(card_to_hit)  # Add to the side deck, not hand
        print(f"{player['name']} hit and took {card_to_hit['value']} of {card_to_hit['suit']} from the table to their side deck.\n")
    else:
        print("The table is empty. You cannot hit.")

#allow a player to top with a matching card
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

#computer player to play a card (randomly)
def computer_play(player, table):
    if player['hand']:
        card_to_play = random.choice(player['hand'])
        player['hand'].remove(card_to_play)
        table.append(card_to_play)
        print(f"{player['name']} played {card_to_play['value']} of {card_to_play['suit']} (Computer)\n")

# Set Up the Deck
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Ace']

deck = [{'suit': suit, 'value': value} for suit in suits for value in values]
random.shuffle(deck)

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

# Show Final Result
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
