import streamlit as st
import random
from copy import deepcopy

# ==========================================
# 1. SETUP & CONSTANTS
# ==========================================
st.set_page_config(page_title="Casino - 40 Card", layout="wide", page_icon="🎰")

CARD_VALUES = {
    'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, 
    '6': 6, '7': 7, '8': 8, '9': 9, '10': 10
}
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
SUITS_SYMBOLS = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Roboto:wght@400;500;700&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: white; 
        font-family: 'Roboto', sans-serif;
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.5);
        margin-bottom: 2rem;
    }
    
    .table-area { 
        background: radial-gradient(ellipse at center, #2d5016 0%, #1a3a0a 100%); 
        border-radius: 20px; 
        padding: 30px; 
        border: 8px solid #8B4513;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.5), 0 10px 30px rgba(0,0,0,0.8), 0 0 0 4px #654321;
        min-height: 250px; 
        display: flex; 
        flex-wrap: wrap; 
        justify-content: center; 
        gap: 20px;
        position: relative;
    }
    
    .playing-card {
        background: white; border-radius: 12px; width: 100px; height: 140px;
        position: relative; box-shadow: 0 4px 8px rgba(0,0,0,0.3), 0 8px 16px rgba(0,0,0,0.2);
        border: 1px solid #ddd; transition: all 0.3s ease; cursor: pointer; overflow: hidden;
    }
    .playing-card:hover { transform: translateY(-10px) rotate(2deg); }
    .playing-card.selected { border: 3px solid #FFD700; box-shadow: 0 0 20px #FFD700; transform: translateY(-15px); }
    
    .card-corner { position: absolute; display: flex; flex-direction: column; align-items: center; line-height: 1; }
    .card-corner-top { top: 8px; left: 8px; }
    .card-corner-bottom { bottom: 8px; right: 8px; transform: rotate(180deg); }
    .card-value { font-size: 1.4rem; font-weight: bold; font-family: 'Playfair Display', serif; }
    .card-suit-small { font-size: 1.2rem; margin-top: 2px; }
    .card-center { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 3.5rem; }
    
    .red-card { color: #dc143c; }
    .black-card { color: #1a1a1a; }
    
    .build-pile {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); border-radius: 12px; padding: 12px;
        min-width: 110px; min-height: 150px; display: flex; flex-direction: column; align-items: center;
        border: 3px solid #8B4513; box-shadow: 0 6px 12px rgba(0,0,0,0.4); position: relative;
    }
    .build-pile.owner-human { border-color: #00ff88; }
    .build-pile.owner-computer { border-color: #ff4444; }
    .build-label { font-size: 1rem; font-weight: bold; color: #000; margin-bottom: 8px; }
    .build-owner { font-size: 0.7rem; color: #333; margin-bottom: 5px; }
    .build-cards-stack { display: flex; flex-direction: column; align-items: center; margin: 5px 0; }
    .build-card-mini {
        background: white; border-radius: 5px; padding: 3px; width: 45px; height: 60px; margin: -12px 0;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.3); border: 1px solid #999; font-size: 0.8rem;
    }
    .build-card-mini.top-card { margin-bottom: 0; border: 2px solid #FFD700; z-index: 10; background: #fffacd; }
    
    .score-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 15px; border-radius: 12px;
        border: 2px solid #FFD700; text-align: center; margin-bottom: 10px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: bold;
        border: none; border-radius: 8px; padding: 10px 18px; width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
        transform: translateY(-2px);
    }
    .action-panel {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); padding: 20px; border-radius: 15px;
        border: 3px solid #00ff88; margin-top: 20px;
    }
    .action-section {
        background: #1e3c72; padding: 15px; border-radius: 10px; margin: 10px 0;
        border: 2px solid #FFD700;
    }
    .pack-display {
        background: #2a2a2a; padding: 12px; border-radius: 10px; border: 2px solid #666;
        text-align: center; margin-bottom: 15px;
    }
    .scoring-breakdown {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        padding: 15px; border-radius: 12px; margin: 10px 0;
        border: 2px solid #FFD700;
    }
    .scoring-item {
        display: flex; justify-content: space-between; align-items: center;
        padding: 8px; margin: 4px 0; background: rgba(255,255,255,0.1);
        border-radius: 6px;
    }
    .scoring-points { font-weight: bold; color: #FFD700; font-size: 1.1rem; }
    .rules-info {
        background: rgba(255,215,0,0.1); padding: 15px; border-radius: 10px;
        border: 1px solid #FFD700; margin: 10px 0; font-size: 0.9rem;
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
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        return {'suit': self.suit, 'value': self.value}
    
    @staticmethod
    def from_dict(d):
        return Card(d['suit'], d['value'])

class Player:
    def __init__(self, name, is_computer=False):
        self.name = name
        self.hand = []
        self.capture_pile = []  # All captured cards
        self.is_computer = is_computer

    def get_card_points(self):
        """Sum of numeric values of captured cards"""
        return sum(card.numeric_value for card in self.capture_pile)
    
    def count_cards(self):
        return len(self.capture_pile)
    
    def count_spades(self):
        return sum(1 for c in self.capture_pile if c.suit == 'Spades')
    
    def has_ten_diamonds(self):
        return sum(1 for c in self.capture_pile if c.value == '10' and c.suit == 'Diamonds')
    
    def has_two_spades(self):
        return sum(1 for c in self.capture_pile if c.value == '2' and c.suit == 'Spades')
    
    def count_aces(self):
        return sum(1 for c in self.capture_pile if c.value == 'Ace')
    
    def to_dict(self):
        return {
            'name': self.name,
            'hand': [c.to_dict() for c in self.hand],
            'capture_pile': [c.to_dict() for c in self.capture_pile],
            'is_computer': self.is_computer
        }
    
    @staticmethod
    def from_dict(d):
        player = Player(d['name'], d['is_computer'])
        player.hand = [Card.from_dict(c) for c in d['hand']]
        player.capture_pile = [Card.from_dict(c) for c in d['capture_pile']]
        return player

# ==========================================
# 3. BUILD MANAGEMENT
# ==========================================
def create_build(cards, owner_name, build_type='single'):
    """Create a new build"""
    value = sum(c.numeric_value for c in cards)
    return {
        'type': build_type,
        'value': value,
        'owner': owner_name,
        'cards': list(cards),
        'groups': [list(cards)] if build_type == 'augmented' else None
    }

def get_build_value(build):
    return build['value']

def can_capture_build(build, card):
    """Check if a card can capture a build"""
    return card.numeric_value == build['value']

def calculate_scoring(human, computer):
    """Calculate the 11-point Casino scoring system"""
    h_cards = human.count_cards()
    c_cards = computer.count_cards()
    h_spades = human.count_spades()
    c_spades = computer.count_spades()
    h_td = human.has_ten_diamonds()
    c_td = computer.has_ten_diamonds()
    h_ts = human.has_two_spades()
    c_ts = computer.has_two_spades()
    h_aces = human.count_aces()
    c_aces = computer.count_aces()
    
    scoring = {
        'human': {
            'most_cards': 2 if h_cards > c_cards else (1 if h_cards == c_cards else 0),
            'most_spades': 2 if h_spades > c_spades else (1 if h_spades == c_spades else 0),
            'ten_diamonds': h_td * 2,
            'two_spades': h_ts * 1,
            'aces': h_aces * 1,
            'card_points': human.get_card_points(),
            'total': 0
        },
        'computer': {
            'most_cards': 2 if c_cards > h_cards else (1 if c_cards == h_cards else 0),
            'most_spades': 2 if c_spades > h_spades else (1 if c_spades == h_spades else 0),
            'ten_diamonds': c_td * 2,
            'two_spades': c_ts * 1,
            'aces': c_aces * 1,
            'card_points': computer.get_card_points(),
            'total': 0
        },
        'details': {
            'human_cards': h_cards, 'computer_cards': c_cards,
            'human_spades': h_spades, 'computer_spades': c_spades,
            'human_td': h_td, 'computer_td': c_td,
            'human_ts': h_ts, 'computer_ts': c_ts,
            'human_aces': h_aces, 'computer_aces': c_aces
        }
    }
    
    for key in ['human', 'computer']:
        s = scoring[key]
        s['total'] = s['most_cards'] + s['most_spades'] + s['ten_diamonds'] + s['two_spades'] + s['aces']
    
    return scoring

# ==========================================
# 4. GAME STATE MANAGEMENT
# ==========================================
def init_game(player_name):
    deck = [Card(suit, value) for suit in SUITS for value in CARD_VALUES.keys()]
    random.shuffle(deck)
    human = Player(player_name)
    computer = Player("Computer", is_computer=True)
    
    # Deal 10 cards each (Round 1)
    for _ in range(10):
        human.hand.append(deck.pop())
        computer.hand.append(deck.pop())
    
    st.session_state.round_num = 1
    st.session_state.deck = deck
    st.session_state.human = human
    st.session_state.computer = computer
    st.session_state.layout = []  # Single cards on table
    st.session_state.builds = []  # Builds on table
    st.session_state.message = "🎮 Round 1 started! Select a card from your hand."
    st.session_state.game_over = False
    st.session_state.last_capturer = None
    st.session_state.selected_hand_idx = None
    st.session_state.selected_layout_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_layout_multi = []
    st.session_state.game_history = []

def save_game_state():
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if len(st.session_state.game_history) >= 5:
        st.session_state.game_history.pop(0)
    
    state = {
        'round_num': st.session_state.round_num,
        'human': st.session_state.human.to_dict(),
        'computer': st.session_state.computer.to_dict(),
        'layout': [c.to_dict() for c in st.session_state.layout],
        'builds': deepcopy(st.session_state.builds),
        'message': st.session_state.message,
        'last_capturer': st.session_state.last_capturer,
        'game_over': st.session_state.game_over,
        'deck': [c.to_dict() for c in st.session_state.deck]
    }
    st.session_state.game_history.append(state)

def undo_last_move():
    if 'game_history' not in st.session_state or not st.session_state.game_history:
        return False
    state = st.session_state.game_history.pop()
    st.session_state.round_num = state['round_num']
    st.session_state.human = Player.from_dict(state['human'])
    st.session_state.computer = Player.from_dict(state['computer'])
    st.session_state.layout = [Card.from_dict(c) for c in state['layout']]
    st.session_state.builds = state['builds']
    st.session_state.message = state['message']
    st.session_state.last_capturer = state['last_capturer']
    st.session_state.game_over = state['game_over']
    st.session_state.deck = [Card.from_dict(c) for c in state['deck']]
    st.session_state.selected_hand_idx = None
    st.session_state.selected_layout_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_layout_multi = []
    return True

def deal_round_2():
    human = st.session_state.human
    computer = st.session_state.computer
    deck = st.session_state.deck
    for _ in range(10):
        if deck: human.hand.append(deck.pop())
        if deck: computer.hand.append(deck.pop())
    st.session_state.round_num = 2
    st.session_state.message = " Round 2 (Final Round)!"
    st.session_state.selected_hand_idx = None
    st.session_state.selected_layout_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_layout_multi = []

def check_round_end():
    human = st.session_state.human
    computer = st.session_state.computer
    if not human.hand and not computer.hand:
        if st.session_state.round_num == 1 and st.session_state.deck:
            st.session_state.message = "🔄 Dealing Round 2..."
            deal_round_2()
            return True
        else:
            st.session_state.game_over = True
            # Last capturer takes remaining layout and builds
            remaining = list(st.session_state.layout)
            for b in st.session_state.builds:
                remaining.extend(b['cards'])
            if remaining and st.session_state.last_capturer:
                capturer = st.session_state.human if st.session_state.last_capturer == 'human' else st.session_state.computer
                capturer.capture_pile.extend(remaining)
                st.session_state.end_sweep_message = f"🧹 {capturer.name} takes {len(remaining)} remaining cards!"
            st.session_state.layout = []
            st.session_state.builds = []
            return True
    return False

# ==========================================
# 5. RENDERING
# ==========================================
def render_card(card, is_selected=False):
    color_class = "red-card" if card.is_red else "black-card"
    selected_class = "selected" if is_selected else ""
    return f'''<div class="playing-card {color_class} {selected_class}">
        <div class="card-corner card-corner-top {color_class}"><div class="card-value">{card.value}</div><div class="card-suit-small">{card.symbol}</div></div>
        <div class="card-center {color_class}">{card.symbol}</div>
        <div class="card-corner card-corner-bottom {color_class}"><div class="card-value">{card.value}</div><div class="card-suit-small">{card.symbol}</div></div>
    </div>'''

def render_build(build):
    owner_class = f"owner-{build['owner']}"
    cards_html = '<div class="build-cards-stack">'
    for i, c in enumerate(build['cards']):
        is_top = (i == len(build['cards']) - 1)
        color_class = "red-card" if c.is_red else "black-card"
        top_class = "top-card" if is_top else ""
        cards_html += f'<div class="build-card-mini {top_class} {color_class}"><div style="font-weight:bold;">{c.value}</div><div>{c.symbol}</div></div>'
    cards_html += '</div>'
    type_label = "AUG" if build['type'] == 'augmented' else "BUILD"
    return f'''<div class="build-pile {owner_class}">
        <div class="build-label">{type_label} {build["value"]}</div>
        <div class="build-owner">By {build["owner"]}</div>
        {cards_html}
    </div>'''

# ==========================================
# 6. COMPUTER AI
# ==========================================
def computer_turn():
    comp = st.session_state.computer
    human = st.session_state.human
    layout = st.session_state.layout
    builds = st.session_state.builds
    
    if not comp.hand:
        return
    
    # Strategy 1: Capture a build (highest value first)
    for h_idx, h_card in enumerate(sorted(comp.hand, key=lambda c: -c.numeric_value)):
        for b_idx, build in enumerate(builds):
            if can_capture_build(build, h_card):
                # Capture the build
                comp.capture_pile.extend(build['cards'])
                comp.capture_pile.append(h_card)
                comp.hand.remove(h_card)
                builds.pop(b_idx)
                st.session_state.last_capturer = 'computer'
                st.session_state.message = f"🤖 Computer captured Build {build['value']} with {h_card}!"
                return
    
    # Strategy 2: Capture single cards or sets
    for h_idx, h_card in enumerate(comp.hand):
        # Single card match
        for t_idx, t_card in enumerate(layout):
            if h_card.numeric_value == t_card.numeric_value:
                comp.capture_pile.append(t_card)
                comp.capture_pile.append(h_card)
                layout.pop(t_idx)
                comp.hand.remove(h_card)
                st.session_state.last_capturer = 'computer'
                st.session_state.message = f"🤖 Computer captured {t_card} with {h_card}!"
                return
        
        # Sum of two cards
        for i in range(len(layout)):
            for j in range(i+1, len(layout)):
                if layout[i].numeric_value + layout[j].numeric_value == h_card.numeric_value:
                    c1, c2 = layout[i], layout[j]
                    for idx in sorted([i, j], reverse=True):
                        layout.pop(idx)
                    comp.capture_pile.extend([c1, c2, h_card])
                    comp.hand.remove(h_card)
                    st.session_state.last_capturer = 'computer'
                    st.session_state.message = f"🤖 Computer swept {c1}+{c2} with {h_card}!"
                    return
    
    # Strategy 3: Create a build (if possible)
    for h_idx, h_card in enumerate(comp.hand):
        # Try to build with layout cards
        for t_idx, t_card in enumerate(layout):
            build_value = h_card.numeric_value + t_card.numeric_value
            if build_value <= 10:
                # Check if computer has the build_value card
                has_capture = any(c.numeric_value == build_value for c in comp.hand if c != h_card)
                if has_capture:
                    # Check no existing build of same value
                    existing = next((b for b in builds if b['value'] == build_value), None)
                    if not existing:
                        new_build = create_build([t_card, h_card], 'computer')
                        builds.append(new_build)
                        layout.pop(t_idx)
                        comp.hand.remove(h_card)
                        st.session_state.message = f" Computer built {build_value} ({t_card}+{h_card})!"
                        return
    
    # Strategy 4: Change opponent's build value
    for h_idx, h_card in enumerate(comp.hand):
        for b_idx, build in enumerate(builds):
            if build['owner'] == 'human':
                new_value = build['value'] + h_card.numeric_value
                if new_value <= 10:
                    has_capture = any(c.numeric_value == new_value for c in comp.hand if c != h_card)
                    if has_capture:
                        build['value'] = new_value
                        build['cards'].append(h_card)
                        build['owner'] = 'computer'
                        comp.hand.remove(h_card)
                        st.session_state.message = f"🤖 Computer changed Build to {new_value}!"
                        return
    
    # Strategy 5: Augment own build with opponent's top card
    if human.capture_pile:
        opp_top = human.capture_pile[-1]
        for h_idx, h_card in enumerate(comp.hand):
            for b_idx, build in enumerate(builds):
                if build['owner'] == 'computer':
                    if build['type'] == 'single':
                        # Try to make augmented build
                        new_value = build['value']
                        if opp_top.numeric_value == new_value:
                            # Can augment with opponent's top
                            build['type'] = 'augmented'
                            build['cards'].append(opp_top)
                            if build['groups'] is None:
                                build['groups'] = [list(build['cards'][:-1])]
                            build['groups'].append([opp_top])
                            human.capture_pile.pop()
                            st.session_state.message = f" Computer augmented Build {new_value} with your {opp_top}!"
                            return
    
    # Strategy 6: Discard lowest card
    comp.hand.sort(key=lambda c: c.numeric_value)
    played = comp.hand.pop(0)
    layout.append(played)
    st.session_state.message = f"🤖 Computer discarded {played}."

# ==========================================
# 7. MAIN APP UI
# ==========================================
def main():
    st.markdown('<h1 class="main-title">🎰 Casino - 40 Card 🇿🇦</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("📊 Scoreboard")
        
        if 'human' in st.session_state and st.session_state.game_history:
            if st.button("↩️ Undo Last Move", key="undo_btn", use_container_width=True):
                if undo_last_move():
                    st.success("Move undone!")
                    st.rerun()
        
        if 'round_num' in st.session_state:
            st.markdown(f"**Round:** {st.session_state.round_num}/2")
        
        st.markdown("### 👁️ Opponent's Top Card")
        if 'computer' in st.session_state and st.session_state.computer.capture_pile:
            top = st.session_state.computer.capture_pile[-1]
            st.markdown(f'<div class="pack-display">{render_card(top)}<div style="color:#aaa; font-size:0.8rem;">Computer\'s Top</div></div>', unsafe_allow_html=True)
        else:
            st.write("Empty")
            
        st.markdown("### 👁️ Your Top Card")
        if 'human' in st.session_state and st.session_state.human.capture_pile:
            top = st.session_state.human.capture_pile[-1]
            st.markdown(f'<div class="pack-display">{render_card(top)}<div style="color:#aaa; font-size:0.8rem;">Your Top</div></div>', unsafe_allow_html=True)
        else:
            st.write("Empty")
        
        if 'human' in st.session_state:
            h = st.session_state.human
            c = st.session_state.computer
            st.markdown(f"""<div class="score-box"><h3>👤 {h.name}</h3><p style="font-size:1.5rem; color:#FFD700;">{h.count_cards()} cards</p></div>
            <div class="score-box"><h3>🤖 Computer</h3><p style="font-size:1.5rem; color:#FFD700;">{c.count_cards()} cards</p></div>""", unsafe_allow_html=True)
        
        if st.button("🔄 New Game"): 
            st.session_state.clear()
            st.rerun()

    if 'human' not in st.session_state:
        st.markdown("""<div style="text-align:center; padding:40px;">
            <h2 style="color:#FFD700;">Welcome to Casino!</h2>
            <div class="rules-info">
            <p><b> 40-Card Deck (Ace-10)</b></p>
            <p><b>🏗️ Builds:</b> Single (sum=value) or Augmented (multiple groups)</p>
            <p><b>👑 Ownership:</b> Builds have owners who must capture them</p>
            <p><b>🔄 Change Value:</b> Add card to opponent's build to steal it</p>
            <p><b>➕ Augment:</b> Add cards to your builds (can use opponent's top card!)</p>
            <p><b>📊 11-Point Scoring:</b> Most Cards(2), Most Spades(2), Ten♦(2), Two(1), Aces(4)</p>
            <p><b>↩️ Undo:</b> Reverse your last move anytime!</p>
            </div>
        </div>""", unsafe_allow_html=True)
        name = st.text_input("Your Name", "Player", label_visibility="collapsed")
        if st.button("🎲 Start Game", type="primary"): 
            init_game(name)
            st.rerun()
        return

    st.info(f"🎯 {st.session_state.message}")

    if st.session_state.game_over:
        st.success("🏁 GAME OVER!")
        if 'end_sweep_message' in st.session_state:
            st.markdown(f'<div style="background:#00ff88; color:#000; padding:15px; border-radius:10px; text-align:center; font-weight:bold;">{st.session_state.end_sweep_message}</div>', unsafe_allow_html=True)
        
        scoring = calculate_scoring(st.session_state.human, st.session_state.computer)
        
        st.markdown("### 📊 11-Point Scoring Breakdown")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**👤 {st.session_state.human.name}**")
            s = scoring['human']
            d = scoring['details']
            st.markdown(f"""<div class="scoring-breakdown">
            <div class="scoring-item"><span>🃏 Most Cards ({d['human_cards']})</span><span class="scoring-points">+{s['most_cards']}</span></div>
            <div class="scoring-item"><span>️ Most Spades ({d['human_spades']})</span><span class="scoring-points">+{s['most_spades']}</span></div>
            <div class="scoring-item"><span>♦️ Ten of Diamonds ({d['human_td']})</span><span class="scoring-points">+{s['ten_diamonds']}</span></div>
            <div class="scoring-item"><span>️ Two of Spades ({d['human_ts']})</span><span class="scoring-points">+{s['two_spades']}</span></div>
            <div class="scoring-item"><span>🅰️ Aces ({d['human_aces']})</span><span class="scoring-points">+{s['aces']}</span></div>
            <hr style="border-color:#FFD700;">
            <div class="scoring-item"><span><b>Bonus Total</b></span><span class="scoring-points" style="font-size:1.5rem;"><b>{s['total']}</b></span></div>
            <div class="scoring-item"><span>Card Points (sum)</span><span class="scoring-points">{s['card_points']}</span></div>
            </div>""", unsafe_allow_html=True)
        
        with col2:
            st.markdown("**🤖 Computer**")
            s = scoring['computer']
            d = scoring['details']
            st.markdown(f"""<div class="scoring-breakdown">
            <div class="scoring-item"><span> Most Cards ({d['computer_cards']})</span><span class="scoring-points">+{s['most_cards']}</span></div>
            <div class="scoring-item"><span>♠️ Most Spades ({d['computer_spades']})</span><span class="scoring-points">+{s['most_spades']}</span></div>
            <div class="scoring-item"><span>♦️ Ten of Diamonds ({d['computer_td']})</span><span class="scoring-points">+{s['ten_diamonds']}</span></div>
            <div class="scoring-item"><span>♠️ Two of Spades ({d['computer_ts']})</span><span class="scoring-points">+{s['two_spades']}</span></div>
            <div class="scoring-item"><span>🅰️ Aces ({d['computer_aces']})</span><span class="scoring-points">+{s['aces']}</span></div>
            <hr style="border-color:#FFD700;">
            <div class="scoring-item"><span><b>Bonus Total</b></span><span class="scoring-points" style="font-size:1.5rem;"><b>{s['total']}</b></span></div>
            <div class="scoring-item"><span>Card Points (sum)</span><span class="scoring-points">{s['card_points']}</span></div>
            </div>""", unsafe_allow_html=True)
        
        h_final = scoring['human']['total']
        c_final = scoring['computer']['total']
        
        st.markdown("###  Final Results")
        if h_final > c_final:
            st.balloons()
            st.success(f"🎉 {st.session_state.human.name} WINS! ({h_final} vs {c_final})")
        elif c_final > h_final:
            st.error(f" Computer WINS! ({c_final} vs {h_final})")
        else:
            st.warning(f"🤝 It's a TIE! ({h_final} each)")
        return

    # === THE TABLE (Layout + Builds) ===
    st.markdown("### 🃏 The Table")
    st.markdown('<div class="table-area">', unsafe_allow_html=True)
    
    # Show builds first
    if st.session_state.builds:
        for i, build in enumerate(st.session_state.builds):
            is_sel = (st.session_state.selected_build_idx == i)
            border = "border:3px solid #00ff88; box-shadow:0 0 15px #00ff88;" if is_sel else ""
            st.markdown(f'<div style="{border} display:inline-block; margin:5px;">{render_build(build)}</div>', unsafe_allow_html=True)
            if st.button(f"Select Build {build['value']}", key=f"sel_b_{i}"):
                st.session_state.selected_build_idx = i
                st.session_state.selected_layout_idx = None
                st.session_state.selected_layout_multi = []
                st.rerun()
    
    # Show single cards in layout
    if st.session_state.layout:
        for i, card in enumerate(st.session_state.layout):
            is_sel = (i in st.session_state.selected_layout_multi)
            st.markdown(f'<div style="display:inline-block; margin:5px;">{render_card(card, is_sel)}</div>', unsafe_allow_html=True)
            btn_text = "✓" if is_sel else f"Select {card}"
            if st.button(btn_text, key=f"sel_l_{i}"):
                if is_sel:
                    st.session_state.selected_layout_multi.remove(i)
                else:
                    st.session_state.selected_layout_multi.append(i)
                st.session_state.selected_build_idx = None
                st.rerun()
    
    if not st.session_state.layout and not st.session_state.builds:
        st.markdown("<p style='text-align:center; color:white; font-style:italic;'>Table is empty</p>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    # === PLAYER HAND ===
    human = st.session_state.human
    if not human.hand:
        st.warning("Waiting for computer...")
        computer_turn()
        check_round_end()
        st.rerun()

    st.markdown("### 🖐️ Your Hand")
    cols = st.columns(min(len(human.hand), 10))
    for idx, card in enumerate(human.hand):
        with cols[idx % len(cols)]:
            is_sel = (st.session_state.selected_hand_idx == idx)
            border = "border:3px solid #FFD700; box-shadow:0 0 15px #FFD700;" if is_sel else ""
            st.markdown(f'<div style="{border} display:inline-block;">{render_card(card)}</div>', unsafe_allow_html=True)
            if st.button("Select", key=f"sel_h_{idx}"):
                st.session_state.selected_hand_idx = idx
                st.session_state.selected_build_idx = None
                st.session_state.selected_layout_idx = None
                st.session_state.selected_layout_multi = []
                st.rerun()

    # === ACTION PANEL ===
    if st.session_state.selected_hand_idx is not None:
        sel_card = human.hand[st.session_state.selected_hand_idx]
        layout = st.session_state.layout
        builds = st.session_state.builds
        
        st.markdown('<div class="action-panel">', unsafe_allow_html=True)
        st.markdown(f"#### 🎯 Action for {sel_card} (Value: {sel_card.numeric_value})")
        
        st.markdown('<div class="action-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Available Actions")
        
        # === CAPTURE ACTIONS ===
        st.markdown("**🎯 1. Capture**")
        
        # Capture single card
        for i, t_card in enumerate(layout):
            if t_card.numeric_value == sel_card.numeric_value:
                if st.button(f"🎯 Capture {t_card}", key=f"cap_single_{i}", use_container_width=True):
                    save_game_state()
                    human.capture_pile.append(t_card)
                    human.capture_pile.append(sel_card)
                    layout.pop(i)
                    human.hand.remove(sel_card)
                    st.session_state.last_capturer = 'human'
                    st.session_state.message = f"👤 You captured {t_card} with {sel_card}!"
                    st.session_state.selected_hand_idx = None
                    computer_turn()
                    check_round_end()
                    st.rerun()
        
        # Capture sum of selected cards
        if len(st.session_state.selected_layout_multi) >= 2:
            selected_sum = sum(layout[i].numeric_value for i in st.session_state.selected_layout_multi)
            if selected_sum == sel_card.numeric_value:
                cards_str = " + ".join([str(layout[i]) for i in st.session_state.selected_layout_multi])
                if st.button(f"🎯 Capture ({cards_str} = {sel_card.numeric_value})", key="cap_sum", use_container_width=True):
                    save_game_state()
                    captured = [layout[i] for i in sorted(st.session_state.selected_layout_multi, reverse=True)]
                    for idx in sorted(st.session_state.selected_layout_multi, reverse=True):
                        layout.pop(idx)
                    human.capture_pile.extend(captured)
                    human.capture_pile.append(sel_card)
                    human.hand.remove(sel_card)
                    st.session_state.last_capturer = 'human'
                    st.session_state.message = f"👤 You swept {cards_str} with {sel_card}!"
                    st.session_state.selected_hand_idx = None
                    st.session_state.selected_layout_multi = []
                    computer_turn()
                    check_round_end()
                    st.rerun()
        
        # Capture build
        for i, build in enumerate(builds):
            if can_capture_build(build, sel_card):
                if st.button(f"🎯 Capture Build {build['value']} (By {build['owner']})", key=f"cap_build_{i}", use_container_width=True):
                    save_game_state()
                    human.capture_pile.extend(build['cards'])
                    human.capture_pile.append(sel_card)
                    builds.pop(i)
                    human.hand.remove(sel_card)
                    st.session_state.last_capturer = 'human'
                    st.session_state.message = f"👤 You captured Build {build['value']} with {sel_card}!"
                    st.session_state.selected_hand_idx = None
                    computer_turn()
                    check_round_end()
                    st.rerun()
        
        # === BUILD ACTIONS ===
        st.markdown("**🏗️ 2. Create/Change Build**")
        
        # Create single build from selected layout cards
        if len(st.session_state.selected_layout_multi) >= 1:
            selected_sum = sum(layout[i].numeric_value for i in st.session_state.selected_layout_multi)
            build_value = selected_sum + sel_card.numeric_value
            
            if build_value <= 10:
                # Check if we have the capture card
                has_capture = any(c.numeric_value == build_value for c in human.hand if c != sel_card)
                # Check no existing build of same value
                existing = next((b for b in builds if b['value'] == build_value), None)
                
                if has_capture and not existing:
                    cards_str = " + ".join([str(layout[i]) for i in st.session_state.selected_layout_multi])
                    if st.button(f"🏗️ Build {build_value} ({cards_str} + {sel_card})", key="create_build", use_container_width=True):
                        save_game_state()
                        selected_cards = [layout[i] for i in sorted(st.session_state.selected_layout_multi, reverse=True)]
                        for idx in sorted(st.session_state.selected_layout_multi, reverse=True):
                            layout.pop(idx)
                        new_build = create_build(selected_cards + [sel_card], 'human')
                        builds.append(new_build)
                        human.hand.remove(sel_card)
                        st.session_state.message = f"👤 You created Build {build_value}!"
                        st.session_state.selected_hand_idx = None
                        st.session_state.selected_layout_multi = []
                        computer_turn()
                        check_round_end()
                        st.rerun()
        
        # Change opponent's build value
        for i, build in enumerate(builds):
            if build['owner'] == 'computer':
                new_value = build['value'] + sel_card.numeric_value
                if new_value <= 10:
                    has_capture = any(c.numeric_value == new_value for c in human.hand if c != sel_card)
                    if has_capture:
                        if st.button(f"🔄 Change Build {build['value']} → {new_value} (Steal!)", key=f"change_build_{i}", use_container_width=True):
                            save_game_state()
                            build['value'] = new_value
                            build['cards'].append(sel_card)
                            build['owner'] = 'human'
                            human.hand.remove(sel_card)
                            st.session_state.message = f" You changed Build to {new_value} and took ownership!"
                            st.session_state.selected_hand_idx = None
                            computer_turn()
                            check_round_end()
                            st.rerun()
        
        # === AUGMENT ACTIONS ===
        st.markdown("**➕ 3. Augment Build**")
        
        # Augment own build with layout cards
        for i, build in enumerate(builds):
            if build['owner'] == 'human':
                # Try augmenting with selected layout cards
                if len(st.session_state.selected_layout_multi) >= 1:
                    selected_sum = sum(layout[j].numeric_value for j in st.session_state.selected_layout_multi)
                    if selected_sum == build['value']:
                        cards_str = " + ".join([str(layout[j]) for j in st.session_state.selected_layout_multi])
                        if st.button(f"➕ Add {cards_str} to your Build {build['value']}", key=f"augment_layout_{i}", use_container_width=True):
                            save_game_state()
                            selected_cards = [layout[j] for j in sorted(st.session_state.selected_layout_multi, reverse=True)]
                            for idx in sorted(st.session_state.selected_layout_multi, reverse=True):
                                layout.pop(idx)
                            if build['type'] == 'single':
                                build['type'] = 'augmented'
                                build['groups'] = [list(build['cards']), selected_cards]
                            else:
                                build['groups'].append(selected_cards)
                            build['cards'].extend(selected_cards)
                            st.session_state.message = f"👤 You augmented Build {build['value']}!"
                            st.session_state.selected_hand_idx = None
                            st.session_state.selected_layout_multi = []
                            computer_turn()
                            check_round_end()
                            st.rerun()
                
                # Try augmenting with opponent's top card
                comp = st.session_state.computer
                if comp.capture_pile:
                    opp_top = comp.capture_pile[-1]
                    if opp_top.numeric_value == build['value']:
                        if st.button(f"➕ Add Computer's {opp_top} to your Build {build['value']}", key=f"augment_opp_{i}", use_container_width=True):
                            save_game_state()
                            comp.capture_pile.pop()
                            if build['type'] == 'single':
                                build['type'] = 'augmented'
                                build['groups'] = [list(build['cards']), [opp_top]]
                            else:
                                build['groups'].append([opp_top])
                            build['cards'].append(opp_top)
                            st.session_state.message = f"👤 You augmented Build {build['value']} with Computer's {opp_top}!"
                            st.session_state.selected_hand_idx = None
                            computer_turn()
                            check_round_end()
                            st.rerun()
        
        # === DISCARD (DRIFT) ===
        st.markdown("**🗑️ 4. Discard (Drift)**")
        if st.button(f"🗑️ Discard {sel_card} to Table", key="discard", use_container_width=True):
            save_game_state()
            layout.append(sel_card)
            human.hand.remove(sel_card)
            st.session_state.message = f"👤 You discarded {sel_card}."
            st.session_state.selected_hand_idx = None
            computer_turn()
            check_round_end()
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    