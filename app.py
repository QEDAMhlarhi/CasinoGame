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
    
    .table-area::before {
        content: ''; position: absolute; top: 10px; left: 10px; right: 10px; bottom: 10px;
        border: 2px solid rgba(255,215,0,0.3); border-radius: 15px; pointer-events: none;
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
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); border-radius: 12px; padding: 15px;
        min-width: 120px; min-height: 160px; display: flex; flex-direction: column; align-items: center;
        border: 3px solid #8B4513; box-shadow: 0 6px 12px rgba(0,0,0,0.4); position: relative;
    }
    .build-label { font-size: 1.1rem; font-weight: bold; color: #000; margin-bottom: 10px; }
    .build-cards-stack { display: flex; flex-direction: column; align-items: center; margin: 10px 0; }
    .build-card-mini {
        background: white; border-radius: 6px; padding: 4px; width: 50px; height: 70px; margin: -15px 0;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.3); border: 1px solid #999; font-size: 0.9rem;
    }
    .build-card-mini.top-card { margin-bottom: 0; border: 2px solid #FFD700; z-index: 10; background: #fffacd; }
    
    .score-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 15px;
        border: 3px solid #FFD700; text-align: center; margin-bottom: 15px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: bold;
        border: none; border-radius: 8px; padding: 12px 20px; width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    .stButton>button:disabled {
        background: #555; color: #888; cursor: not-allowed; transform: none;
    }
    .action-panel {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%); padding: 25px; border-radius: 15px;
        border: 3px solid #00ff88; margin-top: 25px;
    }
    .warning-box {
        background: #8B0000; padding: 15px; border-radius: 10px; border: 2px solid #ff4444;
        color: #ffcccc; margin-bottom: 20px; text-align: center; font-weight: bold;
    }
    .sweep-info {
        background: #00ff88; padding: 15px; border-radius: 10px; color: #000;
        margin-bottom: 20px; text-align: center; font-weight: bold; font-size: 1.2rem;
    }
    .pack-display {
        background: #2a2a2a; padding: 15px; border-radius: 12px; border: 2px solid #666;
        text-align: center; margin-bottom: 20px;
    }
    .build-option {
        background: #1a3a0a; padding: 10px; border-radius: 8px; margin: 10px 0;
        border: 2px solid #00ff88;
    }
    .action-section {
        background: #1e3c72; padding: 15px; border-radius: 10px; margin: 15px 0;
        border: 2px solid #FFD700;
    }
    .top-option {
        background: #4a1a6b; padding: 10px; border-radius: 8px; margin: 10px 0;
        border: 2px solid #9b59b6;
    }
    .opp-sweep-option {
        background: #6b1a4a; padding: 10px; border-radius: 8px; margin: 10px 0;
        border: 2px solid #b6599b;
    }
    .scoring-breakdown {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        padding: 20px; border-radius: 15px; margin: 15px 0;
        border: 2px solid #FFD700;
    }
    .scoring-item {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px; margin: 5px 0; background: rgba(255,255,255,0.1);
        border-radius: 8px;
    }
    .scoring-points {
        font-weight: bold; color: #FFD700; font-size: 1.2rem;
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
    
    def to_dict(self):
        return {'suit': self.suit, 'value': self.value, 'numeric_value': self.numeric_value, 
                'symbol': self.symbol, 'is_red': self.is_red}
    
    @staticmethod
    def from_dict(d):
        card = Card(d['suit'], d['value'])
        card.numeric_value = d['numeric_value']
        card.symbol = d['symbol']
        card.is_red = d['is_red']
        return card

class Player:
    def __init__(self, name, is_computer=False):
        self.name = name
        self.hand = []
        self.side_deck = []
        self.is_computer = is_computer

    def get_points(self):
        return sum(card.numeric_value for card in self.side_deck)
    
    def to_dict(self):
        return {
            'name': self.name,
            'hand': [c.to_dict() for c in self.hand],
            'side_deck': [c.to_dict() for c in self.side_deck],
            'is_computer': self.is_computer
        }
    
    @staticmethod
    def from_dict(d):
        player = Player(d['name'], d['is_computer'])
        player.hand = [Card.from_dict(c) for c in d['hand']]
        player.side_deck = [Card.from_dict(c) for c in d['side_deck']]
        return player

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def calculate_casino_scoring(human, computer):
    """Calculate the 40-Card Casino scoring system"""
    scoring = {
        'human': {'cards': 0, 'spades': 0, 'ten_diamonds': 0, 'two_spades': 0, 'aces': 0, 'total': 0},
        'computer': {'cards': 0, 'spades': 0, 'ten_diamonds': 0, 'two_spades': 0, 'aces': 0, 'total': 0}
    }
    
    # Count cards for each player
    for player, key in [(human, 'human'), (computer, 'computer')]:
        all_cards = player.side_deck
        
        # Most Cards (total count)
        scoring[key]['cards'] = len(all_cards)
        
        # Most Spades
        scoring[key]['spades'] = sum(1 for c in all_cards if c.suit == 'Spades')
        
        # Ten of Diamonds (Mummy)
        scoring[key]['ten_diamonds'] = sum(1 for c in all_cards if c.value == '10' and c.suit == 'Diamonds')
        
        # Two of Spades (Spy Two)
        scoring[key]['two_spades'] = sum(1 for c in all_cards if c.value == '2' and c.suit == 'Spades')
        
        # Aces
        scoring[key]['aces'] = sum(1 for c in all_cards if c.value == 'Ace')
    
    # Calculate points
    # Most Cards: 2 points to whoever has more
    if scoring['human']['cards'] > scoring['computer']['cards']:
        scoring['human']['total'] += 2
    elif scoring['computer']['cards'] > scoring['human']['cards']:
        scoring['computer']['total'] += 2
    
    # Most Spades: 2 points to whoever has more
    if scoring['human']['spades'] > scoring['computer']['spades']:
        scoring['human']['total'] += 2
    elif scoring['computer']['spades'] > scoring['human']['spades']:
        scoring['computer']['total'] += 2
    
    # Ten of Diamonds: 2 points each
    scoring['human']['total'] += scoring['human']['ten_diamonds'] * 2
    scoring['computer']['total'] += scoring['computer']['ten_diamonds'] * 2
    
    # Two of Spades: 1 point each
    scoring['human']['total'] += scoring['human']['two_spades'] * 1
    scoring['computer']['total'] += scoring['computer']['two_spades'] * 1
    
    # Aces: 1 point each
    scoring['human']['total'] += scoring['human']['aces'] * 1
    scoring['computer']['total'] += scoring['computer']['aces'] * 1
    
    return scoring

def save_game_state():
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []
    if len(st.session_state.game_history) >= 10:
        st.session_state.game_history.pop(0)
    state = {
        'round_num': st.session_state.round_num,
        'human': st.session_state.human.to_dict(),
        'computer': st.session_state.computer.to_dict(),
        'table_cards': [c.to_dict() for c in st.session_state.table_cards],
        'table_builds': st.session_state.table_builds,
        'message': st.session_state.message,
        'last_capturer': st.session_state.last_capturer.name if st.session_state.last_capturer else None,
        'game_over': st.session_state.game_over
    }
    st.session_state.game_history.append(state)

def undo_last_move():
    if 'game_history' not in st.session_state or len(st.session_state.game_history) == 0:
        return False
    state = st.session_state.game_history.pop()
    st.session_state.round_num = state['round_num']
    st.session_state.human = Player.from_dict(state['human'])
    st.session_state.computer = Player.from_dict(state['computer'])
    st.session_state.table_cards = [Card.from_dict(c) for c in state['table_cards']]
    st.session_state.table_builds = state['table_builds']
    st.session_state.message = state['message']
    st.session_state.last_capturer = st.session_state.human if state['last_capturer'] == st.session_state.human.name else st.session_state.computer if state['last_capturer'] else None
    st.session_state.game_over = state['game_over']
    st.session_state.selected_hand_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_table_cards = []
    return True

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
    st.session_state.message = "🎮 Round 1 started!"
    st.session_state.game_over = False
    st.session_state.last_capturer = None
    st.session_state.selected_hand_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_table_cards = []
    st.session_state.game_history = []

def deal_round_2():
    human = st.session_state.human
    computer = st.session_state.computer
    deck = st.session_state.deck
    for _ in range(10):
        if deck: human.hand.append(deck.pop())
        if deck: computer.hand.append(deck.pop())
    st.session_state.round_num = 2
    st.session_state.message = "🎯 Round 2 (Final Round)!"
    st.session_state.selected_hand_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_table_cards = []

def check_auto_capture(build_value, builder):
    opponent = st.session_state.computer if builder == st.session_state.human else st.session_state.human
    captured = []
    if not opponent.side_deck:
        return captured
    top_card = opponent.side_deck[-1]
    if top_card.numeric_value == build_value:
        captured.append(opponent.side_deck.pop())
        return captured
    for i, t_card in enumerate(st.session_state.table_cards):
        if top_card.numeric_value + t_card.numeric_value == build_value:
            captured.append(opponent.side_deck.pop())
            captured.append(st.session_state.table_cards.pop(i))
            return captured
    return captured

def render_playing_card(card, is_selected=False):
    color_class = "red-card" if card.is_red else "black-card"
    selected_class = "selected" if is_selected else ""
    return f'''<div class="playing-card {color_class} {selected_class}">
        <div class="card-corner card-corner-top {color_class}"><div class="card-value">{card.value}</div><div class="card-suit-small">{card.symbol}</div></div>
        <div class="card-center {color_class}">{card.symbol}</div>
        <div class="card-corner card-corner-bottom {color_class}"><div class="card-value">{card.value}</div><div class="card-suit-small">{card.symbol}</div></div>
    </div>'''

def render_build(build):
    cards_html = '<div class="build-cards-stack">'
    for i, c in enumerate(build['cards']):
        is_top = (i == len(build['cards']) - 1)
        color_class = "red-card" if c.is_red else "black-card"
        top_class = "top-card" if is_top else ""
        cards_html += f'<div class="build-card-mini {top_class} {color_class}"><div style="font-weight:bold;">{c.value}</div><div>{c.symbol}</div></div>'
    cards_html += '</div>'
    return f'''<div class="build-pile"><div class="build-label">BUILD {build["value"]}</div>{cards_html}<div style="font-size:0.7rem; margin-top:10px;">By {build["owner"]}</div></div>'''

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
            remaining = len(st.session_state.table_cards) + sum(len(b['cards']) for b in st.session_state.table_builds)
            if remaining > 0 and st.session_state.last_capturer:
                for c in st.session_state.table_cards: st.session_state.last_capturer.side_deck.append(c)
                for b in st.session_state.table_builds: st.session_state.last_capturer.side_deck.extend(b['cards'])
                st.session_state.end_sweep_message = f"🧹 END SWEEP: {st.session_state.last_capturer.name} takes {remaining} cards!"
            st.session_state.table_cards = []
            st.session_state.table_builds = []
            return True
    return False

def computer_turn():
    comp = st.session_state.computer
    human = st.session_state.human
    table_cards = st.session_state.table_cards
    table_builds = st.session_state.table_builds
    if not comp.hand: return

    for h_idx, h_card in enumerate(comp.hand):
        for t_idx, t_card in enumerate(table_cards):
            if h_card.numeric_value == t_card.numeric_value:
                comp.hand.pop(h_idx)
                comp.side_deck.append(t_card)
                table_cards.pop(t_idx)
                
                builds_to_remove = []
                for b_idx, build in enumerate(table_builds):
                    if build['value'] == h_card.numeric_value:
                        comp.side_deck.extend(build['cards'])
                        builds_to_remove.append(b_idx)
                for idx in sorted(builds_to_remove, reverse=True):
                    table_builds.pop(idx)
                
                indices_to_remove = []
                for i, tc in enumerate(table_cards):
                    if tc.numeric_value == h_card.numeric_value:
                        comp.side_deck.append(tc)
                        indices_to_remove.append(i)
                for idx in sorted(indices_to_remove, reverse=True):
                    table_cards.pop(idx)
                
                if human.side_deck and human.side_deck[-1].numeric_value == h_card.numeric_value:
                    comp.side_deck.append(human.side_deck.pop())
                
                comp.side_deck.append(h_card)
                
                st.session_state.last_capturer = comp
                st.session_state.message = f" Hit {t_card} with {h_card}! (Captured all {h_card.value}s!)"
                return

    for h_idx, h_card in enumerate(comp.hand):
        for i in range(len(table_cards)):
            for j in range(i + 1, len(table_cards)):
                if table_cards[i].numeric_value + table_cards[j].numeric_value == h_card.numeric_value:
                    c1, c2 = table_cards[i], table_cards[j]
                    for idx in sorted([i, j], reverse=True): table_cards.pop(idx)
                    comp.hand.pop(h_idx)
                    comp.side_deck.extend([c1, c2]); comp.side_deck.append(h_card)
                    st.session_state.last_capturer = comp
                    st.session_state.message = f" Swept {c1}+{c2} with {h_card}!"
                    return

    for h_idx, h_card in enumerate(comp.hand):
        for b_idx, build in enumerate(table_builds):
            if h_card.numeric_value == build['value']:
                comp.hand.pop(h_idx)
                comp.side_deck.extend(build['cards']); comp.side_deck.append(h_card)
                
                extra_captured = []
                indices_to_remove = []
                for i, t_card in enumerate(table_cards):
                    if t_card.numeric_value == h_card.numeric_value:
                        extra_captured.append(t_card)
                        indices_to_remove.append(i)
                for idx in sorted(indices_to_remove, reverse=True):
                    table_cards.pop(idx)
                
                if human.side_deck and human.side_deck[-1].numeric_value == h_card.numeric_value:
                    extra_captured.append(human.side_deck.pop())
                
                for ec in extra_captured:
                    comp.side_deck.append(ec)
                
                table_builds.pop(b_idx)
                st.session_state.last_capturer = comp
                
                extra_msg = ""
                if extra_captured:
                    extra_names = ", ".join([str(c) for c in extra_captured])
                    extra_msg = f" + captured {extra_names}!"
                
                st.session_state.message = f"🤖 Stole Build {build['value']} with {h_card}!{extra_msg}"
                return

    for h_idx, h_card in enumerate(comp.hand):
        for t_idx, t_card in enumerate(table_cards):
            if h_card.numeric_value == t_card.numeric_value:
                has_extra = any(c.numeric_value == h_card.numeric_value for i, c in enumerate(comp.hand) if i != h_idx)
                if has_extra:
                    existing = next((b for b in table_builds if b['value'] == h_card.numeric_value), None)
                    if existing:
                        existing['cards'].extend([t_card, h_card])
                        existing['owner'] = comp.name
                    else:
                        table_builds.append({'cards': [t_card, h_card], 'value': h_card.numeric_value, 'owner': comp.name})
                    table_cards.pop(t_idx); comp.hand.pop(h_idx)
                    st.session_state.message = f"🤖 Topped {t_card} with {h_card} to Build {h_card.numeric_value}!"
                    return

    for h_idx, h_card in enumerate(comp.hand):
        for t_idx, t_card in enumerate(table_cards):
            build_value = h_card.numeric_value + t_card.numeric_value
            if build_value <= 10:
                has_build_card = any(c.numeric_value == build_value for i, c in enumerate(comp.hand) if i != h_idx)
                if has_build_card:
                    existing = next((b for b in table_builds if b['value'] == build_value), None)
                    if existing:
                        base = sorted(existing['cards'] + [t_card], key=lambda c: c.numeric_value)
                        existing['cards'] = base + [h_card]; existing['owner'] = comp.name
                        table_cards.pop(t_idx); comp.hand.pop(h_idx)
                        auto = check_auto_capture(build_value, comp)
                        if auto: existing['cards'].extend(auto)
                        st.session_state.message = f"🤖 Built {build_value}!" + (f" ⚡ Auto-captured {auto}!" if auto else "")
                        return
                    else:
                        table_builds.append({'cards': [t_card, h_card], 'value': build_value, 'owner': comp.name})
                        table_cards.pop(t_idx); comp.hand.pop(h_idx)
                        auto = check_auto_capture(build_value, comp)
                        if auto: table_builds[-1]['cards'].extend(auto)
                        st.session_state.message = f" Built {build_value}!" + (f" ⚡ Auto-captured {auto}!" if auto else "")
                        return

    comp.hand.sort(key=lambda c: c.numeric_value)
    played = comp.hand.pop(0); table_cards.append(played)
    st.session_state.message = f"🤖 Threw {played}."

# ==========================================
# 4. MAIN APP UI
# ==========================================
def main():
    st.markdown('<h1 class="main-title">🎰 SA Street Casino 🇿🇦</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("📊 Scoreboard")
        
        if 'human' in st.session_state and 'game_history' in st.session_state and len(st.session_state.game_history) > 0:
            if st.button("↩️ Undo Last Move", key="undo_btn", use_container_width=True):
                if undo_last_move():
                    st.success("Move undone!")
                    st.rerun()
                else:
                    st.warning("No moves to undo!")
        
        if 'round_num' in st.session_state:
            st.markdown(f"**Round:** {st.session_state.round_num}/2")
        else:
            st.markdown("**Round:** -")
            
        st.markdown("### 👁️ Opponent's Top Card")
        if 'computer' in st.session_state and st.session_state.computer.side_deck:
            st.markdown(f'<div class="pack-display">{render_playing_card(st.session_state.computer.side_deck[-1])}<div style="color:#aaa; font-size:0.8rem;">Computer\'s Top</div></div>', unsafe_allow_html=True)
        else:
            st.write("Computer's pack is empty.")
            
        st.markdown("### 👁️ Your Top Card")
        if 'human' in st.session_state and st.session_state.human.side_deck:
            st.markdown(f'<div class="pack-display">{render_playing_card(st.session_state.human.side_deck[-1])}<div style="color:#aaa; font-size:0.8rem;">Your Top</div></div>', unsafe_allow_html=True)
        else:
            st.write("Your pack is empty.")
        
        if 'human' in st.session_state and 'computer' in st.session_state:
            st.markdown(f"""<div class="score-box"><h3>👤 {st.session_state.human.name}</h3><p style="font-size:2rem; color:#FFD700;">{st.session_state.human.get_points()} pts</p></div>
            <div class="score-box"><h3>🤖 Computer</h3><p style="font-size:2rem; color:#FFD700;">{st.session_state.computer.get_points()} pts</p></div>""", unsafe_allow_html=True)
        
        if st.button(" New Game"): 
            st.session_state.clear()
            st.rerun()

    if 'human' not in st.session_state:
        st.markdown("""<div style="text-align:center; padding:50px;">
            <h2 style="color:#FFD700;">Welcome to SA Street Casino!</h2>
            <p>🃏 Ace-10 only. Two rounds.<br>️ Build with multiple table cards + hand card.<br>
            👑 <b>TOPPING:</b> Top a table card with same-value hand card (need extra in hand)!<br>
            ️ See opponent's top card.<br>
            ⚡ Auto-Capture: Opponent's top + table card = your build value?<br>
            🎯 <b>Steal All:</b> When hitting/stealing, capture ALL matching cards and builds!<br>
            📊 <b>40-Card Scoring:</b> Bonus points for Most Cards, Most Spades, Ten of Diamonds, Two of Spades, and Aces!<br>
            ↩️ <b>Undo:</b> Click the Undo button to reverse your last move!</p>
        </div>""", unsafe_allow_html=True)
        name = st.text_input("Name", "Player", label_visibility="collapsed")
        if st.button("🎲 Start Game", type="primary"): init_game(name); st.rerun()
        return

    st.info(f"🎯 {st.session_state.message}")

    if st.session_state.game_over:
        st.success("🏁 GAME OVER!")
        if 'end_sweep_message' in st.session_state: st.markdown(f'<div class="sweep-info">{st.session_state.end_sweep_message}</div>', unsafe_allow_html=True)
        
        # Calculate 40-Card Casino Scoring
        scoring = calculate_casino_scoring(st.session_state.human, st.session_state.computer)
        
        st.markdown("### 📊 40-Card Scoring Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**👤 {st.session_state.human.name}**")
            st.markdown('<div class="scoring-breakdown">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="scoring-item"><span> Most Cards ({scoring['human']['cards']} cards)</span><span class="scoring-points">{"+2" if scoring['human']['cards'] > scoring['computer']['cards'] else "0"}</span></div>
            <div class="scoring-item"><span>♠️ Most Spades ({scoring['human']['spades']} spades)</span><span class="scoring-points">{"+2" if scoring['human']['spades'] > scoring['computer']['spades'] else "0"}</span></div>
            <div class="scoring-item"><span>♦️ Ten of Diamonds (Mummy) ({scoring['human']['ten_diamonds']})</span><span class="scoring-points">+{scoring['human']['ten_diamonds'] * 2}</span></div>
            <div class="scoring-item"><span>♠️ Two of Spades (Spy Two) ({scoring['human']['two_spades']})</span><span class="scoring-points">+{scoring['human']['two_spades'] * 1}</span></div>
            <div class="scoring-item"><span>️ Aces ({scoring['human']['aces']})</span><span class="scoring-points">+{scoring['human']['aces'] * 1}</span></div>
            <hr style="border-color: #FFD700;">
            <div class="scoring-item"><span><b>Total Bonus Points</b></span><span class="scoring-points" style="font-size: 1.5rem;"><b>{scoring['human']['total']}</b></span></div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"**🤖 Computer**")
            st.markdown('<div class="scoring-breakdown">', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="scoring-item"><span>🃏 Most Cards ({scoring['computer']['cards']} cards)</span><span class="scoring-points">{"+2" if scoring['computer']['cards'] > scoring['human']['cards'] else "0"}</span></div>
            <div class="scoring-item"><span>♠️ Most Spades ({scoring['computer']['spades']} spades)</span><span class="scoring-points">{"+2" if scoring['computer']['spades'] > scoring['human']['spades'] else "0"}</span></div>
            <div class="scoring-item"><span>♦️ Ten of Diamonds (Mummy) ({scoring['computer']['ten_diamonds']})</span><span class="scoring-points">+{scoring['computer']['ten_diamonds'] * 2}</span></div>
            <div class="scoring-item"><span>♠️ Two of Spades (Spy Two) ({scoring['computer']['two_spades']})</span><span class="scoring-points">+{scoring['computer']['two_spades'] * 1}</span></div>
            <div class="scoring-item"><span>🅰️ Aces ({scoring['computer']['aces']})</span><span class="scoring-points">+{scoring['computer']['aces'] * 1}</span></div>
            <hr style="border-color: #FFD700;">
            <div class="scoring-item"><span><b>Total Bonus Points</b></span><span class="scoring-points" style="font-size: 1.5rem;"><b>{scoring['computer']['total']}</b></span></div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Calculate final scores
        human_final = st.session_state.human.get_points() + scoring['human']['total']
        computer_final = st.session_state.computer.get_points() + scoring['computer']['total']
        
        st.markdown("### 🏆 Final Results")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); border-radius: 15px; border: 3px solid #FFD700;">
                <h3 style="color: #FFD700;">{st.session_state.human.name}</h3>
                <p style="font-size: 1.2rem;">Card Points: {st.session_state.human.get_points()}</p>
                <p style="font-size: 1.2rem;">Bonus Points: {scoring['human']['total']}</p>
                <hr style="border-color: #FFD700;">
                <p style="font-size: 2.5rem; color: #FFD700; font-weight: bold;">{human_final} pts</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); border-radius: 15px; border: 3px solid #FFD700; margin-top: 20px;">
                <h3 style="color: #FFD700;">🤖 Computer</h3>
                <p style="font-size: 1.2rem;">Card Points: {st.session_state.computer.get_points()}</p>
                <p style="font-size: 1.2rem;">Bonus Points: {scoring['computer']['total']}</p>
                <hr style="border-color: #FFD700;">
                <p style="font-size: 2.5rem; color: #FFD700; font-weight: bold;">{computer_final} pts</p>
            </div>
            """, unsafe_allow_html=True)
            
            if human_final > computer_final:
                st.balloons()
                st.success(f"🎉 {st.session_state.human.name} WINS! 🎉")
            elif computer_final > human_final:
                st.error("🤖 Computer WINS!")
            else:
                st.warning("🤝 It's a TIE!")
        return

    st.markdown("### 🃏 The Table")
    st.markdown('<div class="table-area">', unsafe_allow_html=True)
    
    if st.session_state.table_builds:
        for i, build in enumerate(st.session_state.table_builds):
            is_sel = (st.session_state.selected_build_idx == i)
            border = "border:3px solid #00ff88;" if is_sel else ""
            st.markdown(f'<div style="{border} display:inline-block;">{render_build(build)}</div>', unsafe_allow_html=True)
            if st.button(f"Select Build {build['value']}", key=f"sel_b_{i}"): 
                st.session_state.selected_build_idx = i
                st.session_state.selected_table_cards = []
                st.rerun()
    
    if st.session_state.table_cards:
        for i, card in enumerate(st.session_state.table_cards):
            is_sel = (i in st.session_state.selected_table_cards)
            st.markdown(f'<div style="display:inline-block;">{render_playing_card(card, is_sel)}</div>', unsafe_allow_html=True)
            if st.button("✓" if is_sel else f"Select {card}", key=f"sel_t_{i}"):
                if is_sel: 
                    st.session_state.selected_table_cards.remove(i)
                else: 
                    st.session_state.selected_table_cards.append(i)
                st.session_state.selected_build_idx = None
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

    human = st.session_state.human
    if not human.hand:
        st.warning("Waiting for computer..."); computer_turn(); check_round_end(); st.rerun()

    st.markdown("### 🖐️ Your Hand")
    cols = st.columns(min(len(human.hand), 10))
    for idx, card in enumerate(human.hand):
        with cols[idx % len(cols)]:
            is_sel = (st.session_state.selected_hand_idx == idx)
            border = "border:3px solid #FFD700;" if is_sel else ""
            st.markdown(f'<div style="{border} display:inline-block;">{render_playing_card(card)}</div>', unsafe_allow_html=True)
            if st.button("Select", key=f"sel_h_{idx}"):
                st.session_state.selected_hand_idx = idx
                st.session_state.selected_build_idx = None
                st.session_state.selected_table_cards = []
                st.rerun()

    if st.session_state.selected_hand_idx is not None:
        sel_card = human.hand[st.session_state.selected_hand_idx]
        st.markdown('<div class="action-panel">', unsafe_allow_html=True)
        st.markdown(f"#### 🎯 Action for {sel_card} ({sel_card.numeric_value})")

        st.markdown('<div class="action-section">', unsafe_allow_html=True)
        st.markdown("### 🎯 Available Actions")
        
        action_col1, action_col2 = st.columns(2)
        
        with action_col1:
            st.markdown("**🃏 Hit / Capture Builds**")
            for i, build in enumerate(st.session_state.table_builds):
                if build['value'] == sel_card.numeric_value:
                    st.markdown(f"**Build {build['value']}** (By {build['owner']})")
                    if st.button(f"🎯 Hit Build {build['value']}", key=f"auto_hit_{i}", use_container_width=True):
                        save_game_state()
                        human.hand.pop(st.session_state.selected_hand_idx)
                        human.side_deck.extend(build['cards']); human.side_deck.append(sel_card)
                        st.session_state.table_builds.pop(i)
                        st.session_state.last_capturer = human
                        st.session_state.message = f"👤 Hit Build {build['value']} with {sel_card}!"
                        st.session_state.selected_hand_idx = None
                        computer_turn()
                        check_round_end()
                        st.rerun()
            
            for i, t_card in enumerate(st.session_state.table_cards):
                if t_card.numeric_value == sel_card.numeric_value:
                    st.markdown(f"**{t_card}** on table")
                    if st.button(f"🎯 Hit {t_card}", key=f"auto_hit_card_{i}", use_container_width=True):
                        save_game_state()
                        st.session_state.table_cards.pop(i)
                        human.hand.pop(st.session_state.selected_hand_idx)
                        human.side_deck.append(t_card); human.side_deck.append(sel_card)
                        st.session_state.last_capturer = human
                        st.session_state.message = f" Hit {t_card} with {sel_card}!"
                        st.session_state.selected_hand_idx = None
                        computer_turn()
                        check_round_end()
                        st.rerun()
        
        with action_col2:
            st.markdown("**️ Build On Existing Builds**")
            for i, build in enumerate(st.session_state.table_builds):
                new_val = sel_card.numeric_value + build['value']
                if new_val <= 10:
                    has_card = any(c.numeric_value == new_val for j, c in enumerate(human.hand) if j != st.session_state.selected_hand_idx)
                    if has_card:
                        st.markdown(f"**Build {build['value']}** → Build {new_val}")
                        if st.button(f"🏗️ Build on {build['value']} → {new_val}", key=f"auto_build_{i}", use_container_width=True):
                            save_game_state()
                            target = next((b for b in st.session_state.table_builds if b['value'] == new_val and b is not build), None)
                            if target:
                                base = sorted(target['cards'] + build['cards'], key=lambda c: c.numeric_value)
                                target['cards'] = base + [sel_card]; target['owner'] = human.name
                                st.session_state.table_builds.remove(build)
                            else:
                                build['cards'].append(sel_card); build['value'] = new_val; build['owner'] = human.name
                            human.hand.pop(st.session_state.selected_hand_idx)
                            st.session_state.message = f"👤 Built on Build to make {new_val}!"
                            st.session_state.selected_hand_idx = None; computer_turn(); check_round_end(); st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

        # BUILD USING OPPONENT'S TOP CARD
        if st.session_state.computer.side_deck:
            opp_top = st.session_state.computer.side_deck[-1]
            if opp_top.numeric_value == sel_card.numeric_value:
                st.markdown("### 👑 Build with Opponent's Top Card")
                st.markdown(f'<div class="opp-sweep-option">👑 <b>Build {sel_card.numeric_value}</b>: Your {sel_card.value} + Computer\'s top {opp_top.value}<br><small>Both cards join your new build!</small></div>', unsafe_allow_html=True)
                
                existing_build = next((b for b in st.session_state.table_builds if b['value'] == sel_card.numeric_value), None)
                btn_text = f"Add to Build {sel_card.numeric_value}" if existing_build else f"Build {sel_card.numeric_value} with Opponent's Top"
                
                if st.button(btn_text, use_container_width=True, key="act_build_opp_top"):
                    save_game_state()
                    if existing_build:
                        existing_build['cards'].extend([opp_top, sel_card])
                        existing_build['owner'] = human.name
                    else:
                        st.session_state.table_builds.append({'cards': [opp_top, sel_card], 'value': sel_card.numeric_value, 'owner': human.name})
                    
                    st.session_state.computer.side_deck.pop()
                    human.hand.pop(st.session_state.selected_hand_idx)
                    st.session_state.message = f"👤 Built {sel_card.numeric_value} using your {sel_card.value} + Computer's {opp_top.value}!"
                    st.session_state.selected_hand_idx = None
                    st.session_state.selected_table_cards = []
                    computer_turn()
                    check_round_end()
                    st.rerun()

        # SWEEP WITH OPPONENT'S TOP CARD
        if len(st.session_state.selected_table_cards) == 1 and st.session_state.computer.side_deck:
            t_idx = st.session_state.selected_table_cards[0]
            t_card = st.session_state.table_cards[t_idx]
            opp_top = st.session_state.computer.side_deck[-1]
            
            if t_card.numeric_value + opp_top.numeric_value == sel_card.numeric_value:
                st.markdown("### 🎯 Sweep with Opponent's Top Card")
                st.markdown(f'<div class="opp-sweep-option">🎯 <b>Sweep!</b> {t_card.value} (table) + {opp_top.value} (opponent top) = {sel_card.value} (your hand)<br><small>Capture both cards!</small></div>', unsafe_allow_html=True)
                
                if st.button(" SWEEP with Opponent's Top!", use_container_width=True, key="act_opp_sweep"):
                    save_game_state()
                    st.session_state.table_cards.pop(t_idx)
                    st.session_state.computer.side_deck.pop()
                    human.hand.pop(st.session_state.selected_hand_idx)
                    human.side_deck.extend([t_card, opp_top])
                    human.side_deck.append(sel_card)
                    st.session_state.last_capturer = human
                    st.session_state.message = f"👤 Swept {t_card} + {opp_top} with {sel_card}!"
                    st.session_state.selected_hand_idx = None
                    st.session_state.selected_table_cards = []
                    computer_turn()
                    check_round_end()
                    st.rerun()

        # TOPPING OPTION
        if len(st.session_state.selected_table_cards) == 1:
            t_idx = st.session_state.selected_table_cards[0]
            t_card = st.session_state.table_cards[t_idx]
            
            if t_card.numeric_value == sel_card.numeric_value:
                has_extra = any(c.numeric_value == sel_card.numeric_value for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                
                if has_extra:
                    existing_build = next((b for b in st.session_state.table_builds if b['value'] == sel_card.numeric_value), None)
                    
                    if existing_build:
                        st.markdown("### 👑 Top & Add to Build")
                        st.markdown(f'<div class="top-option">👑 <b>Top {t_card.value}</b> with {sel_card.value} and add to your <b>Build {sel_card.numeric_value}</b><br><small>(Both cards will join your existing build)</small></div>', unsafe_allow_html=True)
                        
                        if st.button(f"👑 Top & Add to Build {sel_card.numeric_value}", use_container_width=True, key="act_top_add"):
                            save_game_state()
                            existing_build['cards'].extend([t_card, sel_card])
                            existing_build['owner'] = human.name
                            st.session_state.table_cards.pop(t_idx)
                            human.hand.pop(st.session_state.selected_hand_idx)
                            st.session_state.message = f"👤 Topped {t_card} with {sel_card} and added to Build {sel_card.numeric_value}!"
                            st.session_state.selected_hand_idx = None
                            st.session_state.selected_table_cards = []
                            computer_turn()
                            check_round_end()
                            st.rerun()
                    else:
                        st.markdown("### 👑 Top (Create New Build)")
                        st.markdown(f'<div class="top-option"> <b>Top {t_card.value}</b> with {sel_card.value} to Build {sel_card.numeric_value}<br><small>(You have another {sel_card.value} in hand to capture it later)</small></div>', unsafe_allow_html=True)
                        
                        if st.button(f"👑 Top & Build {sel_card.numeric_value}", use_container_width=True, key="act_top_new"):
                            save_game_state()
                            st.session_state.table_builds.append({'cards': [t_card, sel_card], 'value': sel_card.numeric_value, 'owner': human.name})
                            st.session_state.table_cards.pop(t_idx)
                            human.hand.pop(st.session_state.selected_hand_idx)
                            st.session_state.message = f"👤 Topped {t_card} with {sel_card} to Build {sel_card.numeric_value}!"
                            st.session_state.selected_hand_idx = None
                            st.session_state.selected_table_cards = []
                            computer_turn()
                            check_round_end()
                            st.rerun()
                else:
                    st.warning(f"You need another {sel_card.value} in hand to top {t_card}!")

        # THROW OPTION
        st.markdown("### 1️ Throw Card")
        if st.button("Throw to Table", use_container_width=True, key="throw_btn"):
            save_game_state()
            st.session_state.table_cards.append(human.hand.pop(st.session_state.selected_hand_idx))
            st.session_state.message = f"👤 Threw {sel_card}."
            st.session_state.selected_hand_idx = None
            computer_turn()
            check_round_end()
            st.rerun()

        # SWEEP OPTION
        if len(st.session_state.selected_table_cards) >= 2:
            s_sum = sum(st.session_state.table_cards[i].numeric_value for i in st.session_state.selected_table_cards)
            if s_sum == sel_card.numeric_value:
                st.markdown("### 2️⃣ Sweep Multiple Cards")
                st.markdown(f'<div class="sweep-info">🧹 SWEEP: {s_sum} = {sel_card.numeric_value}!</div>', unsafe_allow_html=True)
                if st.button("🧹 SWEEP!", use_container_width=True, key="sweep_btn"):
                    save_game_state()
                    caps = [st.session_state.table_cards[i] for i in sorted(st.session_state.selected_table_cards, reverse=True)]
                    for idx in sorted(st.session_state.selected_table_cards, reverse=True): st.session_state.table_cards.pop(idx)
                    human.hand.pop(st.session_state.selected_hand_idx)
                    human.side_deck.extend(caps); human.side_deck.append(sel_card)
                    st.session_state.last_capturer = human; st.session_state.message = f"👤 Swept {len(caps)} cards!"; st.session_state.selected_hand_idx = None; computer_turn(); check_round_end(); st.rerun()

        # MULTI-CARD BUILD OPTION
        if len(st.session_state.selected_table_cards) >= 1:
            table_sum = sum(st.session_state.table_cards[i].numeric_value for i in st.session_state.selected_table_cards)
            build_value = table_sum + sel_card.numeric_value
            
            if build_value <= 10 and build_value != sel_card.numeric_value:
                has_build_card = any(c.numeric_value == build_value for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                
                if has_build_card:
                    st.markdown("### 3️⃣ Build with Selected Table Cards")
                    selected_cards_str = " + ".join([f"{st.session_state.table_cards[i].value}" for i in st.session_state.selected_table_cards])
                    st.markdown(f'<div class="build-option">️ <b>Build {build_value}</b>: {selected_cards_str} (table) + {sel_card.value} (hand) = {build_value}</div>', unsafe_allow_html=True)
                    
                    existing = next((b for b in st.session_state.table_builds if b['value'] == build_value), None)
                    btn_text = f"Add to Build {build_value}" if existing else f"Build {build_value}"
                    
                    if st.button(btn_text, use_container_width=True, key="act_build_multi"):
                        save_game_state()
                        table_cards_used = [st.session_state.table_cards[i] for i in sorted(st.session_state.selected_table_cards, reverse=True)]
                        
                        if existing:
                            base = sorted(existing['cards'] + table_cards_used, key=lambda c: c.numeric_value)
                            existing['cards'] = base + [sel_card]
                            existing['owner'] = human.name
                        else:
                            all_cards = sorted(table_cards_used, key=lambda c: c.numeric_value) + [sel_card]
                            st.session_state.table_builds.append({'cards': all_cards, 'value': build_value, 'owner': human.name})
                        
                        for idx in sorted(st.session_state.selected_table_cards, reverse=True):
                            st.session_state.table_cards.pop(idx)
                        
                        human.hand.pop(st.session_state.selected_hand_idx)
                        auto = check_auto_capture(build_value, human)
                        if existing and auto: existing['cards'].extend(auto)
                        elif not existing and auto: st.session_state.table_builds[-1]['cards'].extend(auto)
                        
                        auto_msg = f" ⚡ Auto-captured {auto}!" if auto else ""
                        st.session_state.message = f"👤 Built {build_value} using {selected_cards_str} + {sel_card.value}!{auto_msg}"
                        st.session_state.selected_hand_idx = None
                        st.session_state.selected_table_cards = []
                        computer_turn()
                        check_round_end()
                        st.rerun()

            if st.session_state.computer.side_deck:
                opp_top = st.session_state.computer.side_deck[-1]
                build_value_opp = table_sum + sel_card.numeric_value + opp_top.numeric_value
                
                if build_value_opp <= 10:
                    has_card_opp = any(c.numeric_value == build_value_opp for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                    if has_card_opp:
                        selected_cards_str = " + ".join([f"{st.session_state.table_cards[i].value}" for i in st.session_state.selected_table_cards])
                        st.markdown(f"### 4️ Build with Opponent's Top Card")
                        st.markdown(f'<div class="build-option">️ <b>Build {build_value_opp}</b>: {selected_cards_str} (table) + {opp_top.value} (opponent top) + {sel_card.value} (hand) = {build_value_opp}</div>', unsafe_allow_html=True)
                        
                        existing = next((b for b in st.session_state.table_builds if b['value'] == build_value_opp), None)
                        btn_text = f"Add to Build {build_value_opp}" if existing else f"Build {build_value_opp} (uses {opp_top})"
                        
                        if st.button(btn_text, use_container_width=True, key="act_build_opp_multi"):
                            save_game_state()
                            table_cards_used = [st.session_state.table_cards[i] for i in sorted(st.session_state.selected_table_cards, reverse=True)]
                            
                            if existing:
                                merged = sorted(existing['cards'] + table_cards_used + [opp_top], key=lambda c: c.numeric_value)
                                existing['cards'] = merged + [sel_card]
                                existing['owner'] = human.name
                            else:
                                all_cards = sorted(table_cards_used + [opp_top], key=lambda c: c.numeric_value) + [sel_card]
                                st.session_state.table_builds.append({'cards': all_cards, 'value': build_value_opp, 'owner': human.name})
                            
                            for idx in sorted(st.session_state.selected_table_cards, reverse=True):
                                st.session_state.table_cards.pop(idx)
                            st.session_state.computer.side_deck.pop()
                            human.hand.pop(st.session_state.selected_hand_idx)
                            
                            st.session_state.message = f"👤 Built {build_value_opp} using {selected_cards_str} + {opp_top} + {sel_card.value}!"
                            st.session_state.selected_hand_idx = None
                            st.session_state.selected_table_cards = []
                            computer_turn()
                            check_round_end()
                            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()