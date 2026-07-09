import streamlit as st
import random

# ==========================================
# 1. SETUP & CONSTANTS
# ==========================================
st.set_page_config(page_title="SA Street Casino", layout="wide", page_icon="🎰")

CARD_VALUES = {
    'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, 
    '6': 6, '7': 7, '8': 8, '9': 9, '10': 10
}
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
SUITS_SYMBOLS = {'Hearts': '♥️', 'Diamonds': '♦️', 'Clubs': '♣️', 'Spades': '♠️'}

st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    .table-area { 
        background: linear-gradient(135deg, #0f5132 0%, #198754 100%); 
        border-radius: 15px; padding: 20px; border: 4px solid #FFD700;
        min-height: 200px; display: flex; flex-wrap: wrap; justify-content: center; gap: 15px;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
    }
    .card {
        background: white; color: black; border-radius: 10px; padding: 10px;
        text-align: center; font-weight: bold; box-shadow: 3px 3px 8px rgba(0,0,0,0.6);
        width: 70px; height: 100px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; border: 2px solid #ddd;
    }
    .build-pile {
        background: #FFD700; color: black; border-radius: 10px; padding: 10px;
        text-align: center; font-weight: bold; box-shadow: 3px 3px 8px rgba(0,0,0,0.6);
        width: 90px; height: 100px; display: flex; flex-direction: column; 
        justify-content: center; align-items: center; border: 2px solid #000;
    }
    .red-card { color: #d90429; }
    .black-card { color: #2b2d42; }
    .score-box {
        background: #1e1e1e; padding: 15px; border-radius: 10px; 
        border: 2px solid #FFD700; text-align: center; margin-bottom: 10px;
    }
    .stButton>button {
        background: #FFD700; color: black; font-weight: bold; border: none;
        border-radius: 5px; padding: 8px 15px; width: 100%;
    }
    .stButton>button:hover { background: #FFA500; }
    .stButton>button:disabled { background: #555; color: #888; cursor: not-allowed; }
    .action-panel {
        background: #2a2a2a; padding: 20px; border-radius: 10px;
        border: 2px solid #00ff88; margin-top: 20px;
    }
    .warning-box {
        background: #5c1a1a; padding: 10px; border-radius: 5px; 
        border: 1px solid #ff4444; color: #ffcccc; margin-bottom: 15px;
        text-align: center; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. GAME CLASSES
# ==========================================
class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.numeric_value = CARD_VALUES[value]
        self.symbol = SUITS_SYMBOLS[suit]
        self.is_red = suit in ['Hearts', 'Diamonds']

    def __str__(self):
        return f"{self.value}{self.symbol}"

class Player:
    def __init__(self, name, is_computer=False):
        self.name = name
        self.hand = []
        self.side_deck = []
        self.is_computer = is_computer

    def get_points(self):
        return sum(card.numeric_value for card in self.side_deck)

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def init_game(player_name):
    deck = [Card(suit, value) for suit in SUITS for value in CARD_VALUES.keys()]
    random.shuffle(deck)
    
    human = Player(player_name)
    computer = Player("Computer", is_computer=True)
    
    for _ in range(10):
        human.hand.append(deck.pop())
        computer.hand.append(deck.pop())
        
    st.session_state.round_num = 1
    st.session_state.deck = deck
    st.session_state.human = human
    st.session_state.computer = computer
    st.session_state.table_cards = []
    st.session_state.table_builds = [] 
    st.session_state.message = "Round 1 started! If you build, you must capture it if you can."
    st.session_state.game_over = False
    st.session_state.last_capturer = None
    st.session_state.selected_hand_idx = None
    st.session_state.selected_table_card_idx = None
    st.session_state.selected_build_idx = None

def deal_round_2():
    human = st.session_state.human
    computer = st.session_state.computer
    deck = st.session_state.deck
    
    for _ in range(10):
        if deck: human.hand.append(deck.pop())
        if deck: computer.hand.append(deck.pop())
        
    st.session_state.round_num = 2
    st.session_state.message = "Round 2 (Final Round) started!"
    st.session_state.selected_hand_idx = None
    st.session_state.selected_table_card_idx = None
    st.session_state.selected_build_idx = None

def render_card(card):
    color_class = "red-card" if card.is_red else "black-card"
    return f"""
    <div class="card {color_class}">
        <div style="font-size: 1.5rem; font-weight: bold;">{card.value}</div>
        <div style="font-size: 2rem;">{card.symbol}</div>
    </div>
    """

def render_build(build):
    return f"""
    <div class="build-pile">
        <div style="font-size: 1.2rem; font-weight: bold;">BUILD {build['value']}</div>
        <div style="font-size: 0.8rem;">({len(build['cards'])} cards)</div>
        <div style="font-size: 0.7rem;">By {build['owner']}</div>
    </div>
    """

def check_round_end():
    human = st.session_state.human
    computer = st.session_state.computer
    
    if not human.hand and not computer.hand:
        if st.session_state.round_num == 1 and st.session_state.deck:
            st.session_state.message = "Hands empty! Dealing Round 2..."
            deal_round_2()
            return True
        else:
            st.session_state.game_over = True
            if st.session_state.table_cards or st.session_state.table_builds:
                if st.session_state.last_capturer:
                    for c in st.session_state.table_cards:
                        st.session_state.last_capturer.side_deck.append(c)
                    for b in st.session_state.table_builds:
                        st.session_state.last_capturer.side_deck.extend(b['cards'])
                    st.session_state.message = f" {st.session_state.last_capturer.name} sweeps the table!"
                st.session_state.table_cards = []
                st.session_state.table_builds = []
            return True
    return False

def computer_turn():
    comp = st.session_state.computer
    table_cards = st.session_state.table_cards
    table_builds = st.session_state.table_builds
    
    if not comp.hand: return

    # 1. Try to Capture (Hit) a single card or Build
    for h_idx, h_card in enumerate(comp.hand):
        for t_idx, t_card in enumerate(table_cards):
            if h_card.numeric_value == t_card.numeric_value:
                table_cards.pop(t_idx)
                comp.hand.pop(h_idx)
                comp.side_deck.extend([h_card, t_card])
                st.session_state.last_capturer = comp
                st.session_state.message = f"🤖 Computer Hit {t_card} with {h_card}!"
                return
        for b_idx, build in enumerate(table_builds):
            if h_card.numeric_value == build['value']:
                comp.hand.pop(h_idx)
                comp.side_deck.append(h_card)
                comp.side_deck.extend(build['cards'])
                table_builds.pop(b_idx)
                st.session_state.last_capturer = comp
                st.session_state.message = f"🤖 Computer Stole Build {build['value']}!"
                return

    # 2. Try to Build (Allowed in both rounds)
    for h_idx, h_card in enumerate(comp.hand):
        for t_idx, t_card in enumerate(table_cards):
            build_value = h_card.numeric_value + t_card.numeric_value
            has_build_card = any(c.numeric_value == build_value for c in comp.hand)
            if has_build_card:
                existing_build = next((b for b in table_builds if b['value'] == build_value), None)
                if existing_build:
                    existing_build['cards'].extend([table_cards.pop(t_idx), comp.hand.pop(h_idx)])
                    st.session_state.message = f"🤖 Computer added to existing Build {build_value}!"
                else:
                    build_cards = [table_cards.pop(t_idx), comp.hand.pop(h_idx)]
                    table_builds.append({'cards': build_cards, 'value': build_value, 'owner': comp.name})
                    st.session_state.message = f" Computer Built {build_value}!"
                return

    # 3. Throw lowest card
    comp.hand.sort(key=lambda c: c.numeric_value)
    played = comp.hand.pop(0)
    table_cards.append(played)
    st.session_state.message = f"🤖 Computer Threw {played}."

# ==========================================
# 4. MAIN APP UI
# ==========================================
def main():
    st.title("🎰 SA Street Casino 🇿")
    
    if 'human' not in st.session_state:
        st.markdown("""
        ### 🇿🇦 Welcome to South African Street Casino!
        **Street Rules:**
        -  Deck: Ace to 10 only. Two rounds of 10 cards.
        - 🏗️ **Building:** Allowed in Round 1 and Round 2.
        - 🚫 **Round 1 Restriction:** If YOU build a number, you MUST capture it if you can. If you can't capture or build on it, you can throw.
        - ✅ If opponent builds, you can still throw.
        - 🔄 **Merging:** You cannot have two "Build 10s". New builds merge into existing ones!
        -  **Steal:** Capture an opponent's Build if you have the matching number.
        """)
        name = st.text_input("Enter Your Name", "Player")
        if st.button("🎲 Start Game", type="primary"):
            init_game(name)
            st.rerun()
        return

    with st.sidebar:
        st.header("📊 Scoreboard")
        st.markdown(f"**Round:** {st.session_state.round_num} / 2")
        st.markdown(f"**Cards in Deck:** {len(st.session_state.deck)}")
        st.markdown(f"""
        <div class="score-box">
            <h3>👤 {st.session_state.human.name}</h3>
            <p style="font-size: 1.5rem; color: #FFD700;">{st.session_state.human.get_points()} pts</p>
            <p>Cards: {len(st.session_state.human.side_deck)}</p>
        </div>
        <div class="score-box">
            <h3> Computer</h3>
            <p style="font-size: 1.5rem; color: #FFD700;">{st.session_state.computer.get_points()} pts</p>
            <p>Cards: {len(st.session_state.computer.side_deck)}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button(" New Game"):
            st.session_state.clear()
            st.rerun()

    st.info(f"🎯 {st.session_state.message}")

    if st.session_state.game_over:
        st.success("🏁 GAME OVER! 🏁")
        h_pts = st.session_state.human.get_points()
        c_pts = st.session_state.computer.get_points()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if h_pts > c_pts:
                st.balloons()
                st.success(f"🎉 {st.session_state.human.name} WINS! 🎉")
            elif c_pts > h_pts:
                st.error(f" Computer WINS!")
            else:
                st.warning("🤝 It's a TIE!")
            st.markdown(f"### Final Score: {h_pts} - {c_pts}")
        return

    # --- THE TABLE ---
    st.markdown("### 🃏 The Table")
    st.markdown('<div class="table-area">', unsafe_allow_html=True)
    table_empty = True
    
    if st.session_state.table_builds:
        table_empty = False
        for i, build in enumerate(st.session_state.table_builds):
            is_selected = (st.session_state.selected_build_idx == i)
            border = "border: 3px solid #00ff88;" if is_selected else ""
            st.markdown(f'<div style="{border} display: inline-block;">{render_build(build)}</div>', unsafe_allow_html=True)
            if st.button(f"Select Build {build['value']}", key=f"sel_build_{i}"):
                st.session_state.selected_build_idx = i
                st.session_state.selected_table_card_idx = None
                st.rerun()

    if st.session_state.table_cards:
        table_empty = False
        for i, card in enumerate(st.session_state.table_cards):
            is_selected = (st.session_state.selected_table_card_idx == i)
            border = "border: 3px solid #00ff88;" if is_selected else ""
            st.markdown(f'<div style="{border} display: inline-block;">{render_card(card)}</div>', unsafe_allow_html=True)
            if st.button(f"Select {card}", key=f"sel_table_{i}"):
                st.session_state.selected_table_card_idx = i
                st.session_state.selected_build_idx = None
                st.rerun()

    if table_empty:
        st.markdown("<p style='text-align: center; color: white; font-style: italic; width: 100%;'>Table is empty</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PLAYER HAND ---
    human = st.session_state.human
    if not human.hand:
        st.warning("Your hand is empty! Waiting for computer...")
        computer_turn()
        check_round_end()
        st.rerun()

    st.markdown("### 🖐️ Your Hand (Select a card to play)")
    hand_cols = st.columns(min(len(human.hand), 10))
    for idx, card in enumerate(human.hand):
        with hand_cols[idx % len(hand_cols)]:
            is_selected = (st.session_state.selected_hand_idx == idx)
            border = "border: 3px solid #FFD700; transform: translateY(-10px);" if is_selected else ""
            st.markdown(f'<div style="{border} display: inline-block;">{render_card(card)}</div>', unsafe_allow_html=True)
            if st.button(f"Select", key=f"sel_hand_{idx}", type="primary" if is_selected else "secondary"):
                st.session_state.selected_hand_idx = idx
                st.session_state.selected_table_card_idx = None
                st.session_state.selected_build_idx = None
                st.rerun()

    # --- ACTION PANEL ---
    if st.session_state.selected_hand_idx is not None:
        selected_card = human.hand[st.session_state.selected_hand_idx]
        
        # RULE CHECK: Can we throw?
        throw_disabled = False
        warning_message = ""
        
        if st.session_state.round_num == 1:
            # Check if human owns any build on the table
            human_builds = [b for b in st.session_state.table_builds if b['owner'] == human.name]
            
            if human_builds:
                # Check if player can capture any of their own builds
                can_capture_own_build = any(
                    selected_card.numeric_value == build['value'] 
                    for build in human_builds
                )
                
                # Check if player can build on top of their own build
                # (by adding a table card to reach the build value)
                can_build_on_own = False
                for build in human_builds:
                    for t_card in st.session_state.table_cards:
                        if selected_card.numeric_value + t_card.numeric_value == build['value']:
                            can_build_on_own = True
                            break
                
                # If player can capture OR build on their own build, they MUST do so
                if can_capture_own_build or can_build_on_own:
                    throw_disabled = True
                    warning_message = "⚠️ ROUND 1 RULE: You have a build on the table and can capture/build on it! You must Hit or Build on your own build."

        st.markdown('<div class="action-panel">', unsafe_allow_html=True)
        st.markdown(f"#### 🎯 Action for {selected_card} (Value: {selected_card.numeric_value})")
        
        if throw_disabled:
            st.markdown(f'<div class="warning-box">{warning_message}</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**1. Throw (Play to Table)**")
            if throw_disabled:
                st.button("Throw Card", key="act_throw", disabled=True, use_container_width=True)
            else:
                if st.button("Throw Card", key="act_throw", use_container_width=True):
                    st.session_state.table_cards.append(human.hand.pop(st.session_state.selected_hand_idx))
                    st.session_state.message = f"👤 You Threw {selected_card}."
                    st.session_state.selected_hand_idx = None
                    computer_turn()
                    check_round_end()
                    st.rerun()

        with col2:
            st.markdown("**2. Hit (Capture)**")
            st.caption("Select a card/build on table first!")
            can_hit = False
            
            if st.session_state.selected_table_card_idx is not None:
                t_card = st.session_state.table_cards[st.session_state.selected_table_card_idx]
                if t_card.numeric_value == selected_card.numeric_value:
                    can_hit = True
                    if st.button(f"Hit {t_card}", key="act_hit_single", use_container_width=True):
                        st.session_state.table_cards.pop(st.session_state.selected_table_card_idx)
                        human.hand.pop(st.session_state.selected_hand_idx)
                        human.side_deck.extend([selected_card, t_card])
                        st.session_state.last_capturer = human
                        st.session_state.message = f"👤 You Hit {t_card} with {selected_card}!"
                        st.session_state.selected_hand_idx = None
                        computer_turn()
                        check_round_end()
                        st.rerun()

            if st.session_state.selected_build_idx is not None:
                build = st.session_state.table_builds[st.session_state.selected_build_idx]
                if build['value'] == selected_card.numeric_value:
                    can_hit = True
                    if st.button(f"Steal Build {build['value']}", key="act_hit_build", use_container_width=True):
                        human.hand.pop(st.session_state.selected_hand_idx)
                        human.side_deck.append(selected_card)
                        human.side_deck.extend(build['cards'])
                        st.session_state.table_builds.pop(st.session_state.selected_build_idx)
                        st.session_state.last_capturer = human
                        st.session_state.message = f"👤 You Stole Build {build['value']}!"
                        st.session_state.selected_hand_idx = None
                        computer_turn()
                        check_round_end()
                        st.rerun()

            if not can_hit and (st.session_state.selected_table_card_idx is not None or st.session_state.selected_build_idx is not None):
                st.error("Cannot capture this with your selected card!")

        with col3:
            st.markdown("**3. Build**")
            st.caption("Select a table card to build with!")
            can_build = False
            
            if st.session_state.selected_table_card_idx is not None:
                t_card = st.session_state.table_cards[st.session_state.selected_table_card_idx]
                build_value = selected_card.numeric_value + t_card.numeric_value
                has_build_card = any(c.numeric_value == build_value for c in human.hand)
                
                if has_build_card:
                    can_build = True
                    existing_build = next((b for b in st.session_state.table_builds if b['value'] == build_value), None)
                    btn_text = f"Add to Build {build_value}" if existing_build else f"Build {build_value}"
                    
                    if st.button(btn_text, key="act_build", use_container_width=True):
                        if existing_build:
                            existing_build['cards'].append(t_card)
                            existing_build['cards'].append(selected_card)
                            st.session_state.table_cards.pop(st.session_state.selected_table_card_idx)
                            human.hand.pop(st.session_state.selected_hand_idx)
                            st.session_state.message = f"👤 Added to existing Build {build_value}!"
                        else:
                            build_cards = [st.session_state.table_cards.pop(st.session_state.selected_table_card_idx), 
                                           human.hand.pop(st.session_state.selected_hand_idx)]
                            st.session_state.table_builds.append({
                                'cards': build_cards, 'value': build_value, 'owner': human.name
                            })
                            st.session_state.message = f"👤 Built {build_value}!"
                        
                        st.session_state.selected_hand_idx = None
                        computer_turn()
                        check_round_end()
                        st.rerun()
                else:
                    st.error(f"You need a {build_value} in hand to build!")
            else:
                st.caption("Select a table card first to build.")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()