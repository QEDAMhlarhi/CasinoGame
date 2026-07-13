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
        box-shadow: 
            inset 0 0 50px rgba(0,0,0,0.5),
            0 10px 30px rgba(0,0,0,0.8),
            0 0 0 4px #654321;
        min-height: 250px; 
        display: flex; 
        flex-wrap: wrap; 
        justify-content: center; 
        gap: 20px;
        position: relative;
    }
    
    .table-area::before {
        content: '';
        position: absolute;
        top: 10px;
        left: 10px;
        right: 10px;
        bottom: 10px;
        border: 2px solid rgba(255,215,0,0.3);
        border-radius: 15px;
        pointer-events: none;
    }
    
    .playing-card {
        background: white;
        border-radius: 12px;
        width: 100px;
        height: 140px;
        position: relative;
        box-shadow: 
            0 4px 8px rgba(0,0,0,0.3),
            0 8px 16px rgba(0,0,0,0.2),
            inset 0 1px 0 rgba(255,255,255,0.8);
        border: 1px solid #ddd;
        transition: all 0.3s ease;
        cursor: pointer;
        overflow: hidden;
    }
    
    .playing-card:hover {
        transform: translateY(-10px) rotate(2deg);
        box-shadow: 
            0 8px 16px rgba(0,0,0,0.4),
            0 12px 24px rgba(0,0,0,0.3);
    }
    
    .playing-card.selected {
        border: 3px solid #FFD700;
        box-shadow: 
            0 0 20px #FFD700,
            0 8px 16px rgba(0,0,0,0.4);
        transform: translateY(-15px);
    }
    
    .card-corner {
        position: absolute;
        display: flex;
        flex-direction: column;
        align-items: center;
        line-height: 1;
    }
    
    .card-corner-top {
        top: 8px;
        left: 8px;
    }
    
    .card-corner-bottom {
        bottom: 8px;
        right: 8px;
        transform: rotate(180deg);
    }
    
    .card-value {
        font-size: 1.4rem;
        font-weight: bold;
        font-family: 'Playfair Display', serif;
    }
    
    .card-suit-small {
        font-size: 1.2rem;
        margin-top: 2px;
    }
    
    .card-center {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3.5rem;
    }
    
    .red-card {
        color: #dc143c;
    }
    
    .black-card {
        color: #1a1a1a;
    }
    
    .build-pile {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        border-radius: 12px;
        padding: 15px;
        min-width: 120px;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        border: 3px solid #8B4513;
        box-shadow: 
            0 6px 12px rgba(0,0,0,0.4),
            inset 0 2px 4px rgba(255,255,255,0.3);
        position: relative;
    }
    
    .build-label {
        font-size: 1.1rem;
        font-weight: bold;
        color: #000;
        margin-bottom: 10px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }
    
    .build-cards-stack {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 10px 0;
    }
    
    .build-card-mini {
        background: white;
        border-radius: 6px;
        padding: 4px;
        width: 50px;
        height: 70px;
        margin: -15px 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        border: 1px solid #999;
        font-size: 0.9rem;
        position: relative;
    }
    
    .build-card-mini.top-card {
        margin-bottom: 0;
        border: 2px solid #FFD700;
        z-index: 10;
        background: #fffacd;
        box-shadow: 0 0 10px rgba(255,215,0,0.8);
    }
    
    .score-box {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 15px;
        border: 3px solid #FFD700;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .score-box h3 {
        margin: 0 0 10px 0;
        font-size: 1.3rem;
        color: #FFD700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    .score-box p {
        margin: 5px 0;
        font-size: 1.1rem;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        font-size: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #FFA500 0%, #FFD700 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.4);
    }
    
    .stButton>button:disabled {
        background: #555;
        color: #888;
        cursor: not-allowed;
        transform: none;
    }
    
    .action-panel {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        padding: 25px;
        border-radius: 15px;
        border: 3px solid #00ff88;
        margin-top: 25px;
        box-shadow: 0 0 20px rgba(0,255,136,0.3);
    }
    
    .warning-box {
        background: linear-gradient(135deg, #8B0000 0%, #5c1a1a 100%);
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #ff4444;
        color: #ffcccc;
        margin-bottom: 20px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
    }
    
    .sweep-info {
        background: linear-gradient(135deg, #00ff88 0%, #00cc66 100%);
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #00ff88;
        color: #000;
        margin-bottom: 20px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
        box-shadow: 0 0 15px rgba(0,255,136,0.5);
    }
    
    .end-sweep-box {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-weight: bold;
        font-size: 1.3rem;
        margin: 25px 0;
        box-shadow: 0 0 30px rgba(255,215,0,0.6);
        border: 3px solid #FFD700;
    }
    
    .pack-display {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%);
        padding: 15px;
        border-radius: 12px;
        border: 2px solid #666;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .pack-label {
        font-size: 0.9rem;
        color: #aaa;
        margin-top: 10px;
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
    st.session_state.message = "🎮 Round 1 started! Watch the opponent's top card!"
    st.session_state.game_over = False
    st.session_state.last_capturer = None
    st.session_state.selected_hand_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_table_cards = []

def deal_round_2():
    human = st.session_state.human
    computer = st.session_state.computer
    deck = st.session_state.deck
    
    for _ in range(10):
        if deck: human.hand.append(deck.pop())
        if deck: computer.hand.append(deck.pop())
        
    st.session_state.round_num = 2
    st.session_state.message = " Round 2 (Final Round)! Last capture gets the leftover table cards!"
    st.session_state.selected_hand_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_table_cards = []

def check_auto_capture(build_value, builder):
    """
    Auto-capture rule: If you build a number and opponent's top card matches,
    automatically add it to your build!
    """
    opponent = st.session_state.computer if builder == st.session_state.human else st.session_state.human
    
    if opponent.side_deck:
        top_card = opponent.side_deck[-1]
        if top_card.numeric_value == build_value:
            # Auto-capture!
            opponent.side_deck.pop()  # Remove from opponent's deck
            return top_card
    return None

def render_playing_card(card, is_selected=False):
    color_class = "red-card" if card.is_red else "black-card"
    selected_class = "selected" if is_selected else ""
    
    html = f'''<div class="playing-card {color_class} {selected_class}">
        <div class="card-corner card-corner-top {color_class}">
            <div class="card-value">{card.value}</div>
            <div class="card-suit-small">{card.symbol}</div>
        </div>
        <div class="card-center {color_class}">
            {card.symbol}
        </div>
        <div class="card-corner card-corner-bottom {color_class}">
            <div class="card-value">{card.value}</div>
            <div class="card-suit-small">{card.symbol}</div>
        </div>
    </div>'''
    return html

def render_build(build):
    cards_html = '<div class="build-cards-stack">'
    for i, c in enumerate(build['cards']):
        is_top = (i == len(build['cards']) - 1)
        color_class = "red-card" if c.is_red else "black-card"
        top_class = "top-card" if is_top else ""
        cards_html += f'<div class="build-card-mini {top_class} {color_class}">'
        cards_html += f'<div style="font-weight:bold; font-size:1.1rem;">{c.value}</div>'
        cards_html += f'<div style="font-size:1.3rem;">{c.symbol}</div>'
        cards_html += '</div>'
    cards_html += '</div>'
    
    html = f'''<div class="build-pile">
        <div class="build-label">BUILD {build["value"]}</div>
        {cards_html}
        <div style="font-size:0.7rem; margin-top:10px; color:#000;">By {build["owner"]}</div>
    </div>'''
    return html

def check_round_end():
    human = st.session_state.human
    computer = st.session_state.computer
    
    if not human.hand and not computer.hand:
        if st.session_state.round_num == 1 and st.session_state.deck:
            st.session_state.message = "🔄 Hands empty! Dealing Round 2..."
            deal_round_2()
            return True
        else:
            st.session_state.game_over = True
            remaining_cards_count = len(st.session_state.table_cards) + sum(len(b['cards']) for b in st.session_state.table_builds)
            if remaining_cards_count > 0:
                if st.session_state.last_capturer:
                    for c in st.session_state.table_cards:
                        st.session_state.last_capturer.side_deck.append(c)
                    for b in st.session_state.table_builds:
                        st.session_state.last_capturer.side_deck.extend(b['cards'])
                    st.session_state.end_sweep_message = f"🧹 END GAME SWEEP: {st.session_state.last_capturer.name} made the last capture and takes the remaining {remaining_cards_count} cards!"
                else:
                    st.session_state.end_sweep_message = "No captures were made. Table cards are discarded."
            else:
                st.session_state.end_sweep_message = "✨ Table was completely cleared!"
                
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
                table_cards.pop(t_idx)
                comp.hand.pop(h_idx)
                comp.side_deck.extend([h_card, t_card])
                st.session_state.last_capturer = comp
                st.session_state.message = f"🤖 Computer Hit {t_card} with {h_card}!"
                return

    for h_idx, h_card in enumerate(comp.hand):
        for i in range(len(table_cards)):
            for j in range(i + 1, len(table_cards)):
                if table_cards[i].numeric_value + table_cards[j].numeric_value == h_card.numeric_value:
                    c1, c2 = table_cards[i], table_cards[j]
                    for idx in sorted([i, j], reverse=True):
                        table_cards.pop(idx)
                    comp.hand.pop(h_idx)
                    comp.side_deck.extend([h_card, c1, c2])
                    st.session_state.last_capturer = comp
                    st.session_state.message = f"🤖 Computer Swept {c1} + {c2} with {h_card}!"
                    return

    for h_idx, h_card in enumerate(comp.hand):
        for b_idx, build in enumerate(table_builds):
            if h_card.numeric_value == build['value']:
                comp.hand.pop(h_idx)
                comp.side_deck.append(h_card)
                comp.side_deck.extend(build['cards'])
                table_builds.pop(b_idx)
                st.session_state.last_capturer = comp
                st.session_state.message = f"🤖 Computer Stole Build {build['value']}!"
                return

    for h_idx, h_card in enumerate(comp.hand):
        for t_idx, t_card in enumerate(table_cards):
            build_value = h_card.numeric_value + t_card.numeric_value
            if build_value <= 10:
                has_build_card = any(c.numeric_value == build_value for i, c in enumerate(comp.hand) if i != h_idx)
                if has_build_card:
                    existing_build = next((b for b in table_builds if b['value'] == build_value and b['owner'] == comp.name), None)
                    if not existing_build:
                        existing_build = next((b for b in table_builds if b['value'] == build_value), None)

                    if existing_build:
                        base = sorted(existing_build['cards'] + [t_card], key=lambda c: c.numeric_value)
                        existing_build['cards'] = base + [h_card]
                        existing_build['owner'] = comp.name
                        table_cards.pop(t_idx)
                        comp.hand.pop(h_idx)
                        
                        # Check auto-capture
                        auto_card = check_auto_capture(build_value, comp)
                        if auto_card:
                            existing_build['cards'].append(auto_card)
                            st.session_state.message = f"🤖 Computer Built {build_value} + AUTO-CAPTURED your {auto_card}!"
                        else:
                            st.session_state.message = f"🤖 Computer added to existing Build {build_value}!"
                        return
                    else:
                        build_cards = [t_card, h_card]
                        table_builds.append({'cards': build_cards, 'value': build_value, 'owner': comp.name})
                        table_cards.pop(t_idx)
                        comp.hand.pop(h_idx)
                        
                        # Check auto-capture
                        auto_card = check_auto_capture(build_value, comp)
                        if auto_card:
                            table_builds[-1]['cards'].append(auto_card)
                            st.session_state.message = f"🤖 Computer Built {build_value} + AUTO-CAPTURED your {auto_card}!"
                        else:
                            st.session_state.message = f"🤖 Computer Built {build_value}!"
                        return
            
            if human.side_deck:
                opp_top = human.side_deck[-1]
                build_value_opp = h_card.numeric_value + t_card.numeric_value + opp_top.numeric_value
                if build_value_opp <= 10:
                    has_build_card_opp = any(c.numeric_value == build_value_opp for i, c in enumerate(comp.hand) if i != h_idx)
                    if has_build_card_opp:
                        base_cards = sorted([t_card, opp_top], key=lambda c: c.numeric_value)
                        build_cards = base_cards + [h_card]
                        
                        existing_build = next((b for b in table_builds if b['value'] == build_value_opp), None)
                        if existing_build:
                            merged_base = sorted(existing_build['cards'] + [t_card, opp_top], key=lambda c: c.numeric_value)
                            existing_build['cards'] = merged_base + [h_card]
                            existing_build['owner'] = comp.name
                            human.side_deck.pop()
                            table_cards.pop(t_idx)
                            comp.hand.pop(h_idx)
                            st.session_state.message = f"🤖 Computer built on Build {build_value_opp} using your {opp_top}!"
                            return
                        else:
                            table_builds.append({'cards': build_cards, 'value': build_value_opp, 'owner': comp.name})
                            human.side_deck.pop()
                            table_cards.pop(t_idx)
                            comp.hand.pop(h_idx)
                            st.session_state.message = f"🤖 Computer Built {build_value_opp} using your {opp_top}!"
                            return

        for b_idx, build in enumerate(table_builds):
            new_build_value = h_card.numeric_value + build['value']
            if new_build_value <= 10:
                has_build_card = any(c.numeric_value == new_build_value for i, c in enumerate(comp.hand) if i != h_idx)
                if has_build_card:
                    target_build = next((b for b in table_builds if b['value'] == new_build_value and b is not build), None)
                    
                    if target_build:
                        base_cards = sorted(target_build['cards'] + build['cards'], key=lambda c: c.numeric_value)
                        target_build['cards'] = base_cards + [h_card]
                        target_build['owner'] = comp.name
                        table_builds.remove(build)
                        comp.hand.pop(h_idx)
                        st.session_state.message = f"🤖 Computer built on Build to make {new_build_value} (Merged)!"
                        return
                    else:
                        build['cards'] = build['cards'] + [h_card]
                        build['value'] = new_build_value
                        build['owner'] = comp.name
                        comp.hand.pop(h_idx)
                        st.session_state.message = f" Computer built on Build to make {new_build_value}!"
                        return

    comp.hand.sort(key=lambda c: c.numeric_value)
    played = comp.hand.pop(0)
    table_cards.append(played)
    st.session_state.message = f" Computer Threw {played}."

# ==========================================
# 4. MAIN APP UI
# ==========================================
def main():
    st.markdown('<h1 class="main-title">🎰 SA Street Casino 🇦</h1>', unsafe_allow_html=True)
    
    if 'human' not in st.session_state:
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h2 style="color: #FFD700; font-size: 2.5rem;">Welcome to South African Street Casino!</h2>
            <p style="font-size: 1.3rem; margin: 30px 0;">
                🃏 Deck: Ace to 10 only. Two rounds of 10 cards.<br>
                👁️ Pack Visibility: See opponent's top card!<br>
                🏗️ Build with Pack: Use opponent's top card to build!<br>
                 Packing Order: Small-to-big, building card on top.<br>
                🔄 No Duplicate Builds: Same numbers merge!<br>
                 Sweep: Capture multiple cards if sum matches!<br>
                🏆 End Game Sweep: Last capture gets all remaining cards!<br>
                 <b>NEW: Auto-Capture!</b> Build a number that matches opponent's top card = automatic capture!
            </p>
        </div>
        """, unsafe_allow_html=True)
        name = st.text_input("Enter Your Name", "Player", label_visibility="collapsed")
        if st.button("🎲 Start Game", type="primary"):
            init_game(name)
            st.rerun()
        return

    with st.sidebar:
        st.header("📊 Scoreboard")
        st.markdown(f"**Round:** {st.session_state.round_num} / 2")
        
        st.markdown("### 👁️ Opponent's Pack (Top Card)")
        if st.session_state.computer.side_deck:
            top_card = st.session_state.computer.side_deck[-1]
            st.markdown(f'<div class="pack-display">{render_playing_card(top_card)}<div class="pack-label">Computer\'s Top Card</div></div>', unsafe_allow_html=True)
        else:
            st.write("Computer's pack is empty.")
            
        st.markdown("---")
        st.markdown("### 👁️ Your Pack (Top Card)")
        if st.session_state.human.side_deck:
            top_card = st.session_state.human.side_deck[-1]
            st.markdown(f'<div class="pack-display">{render_playing_card(top_card)}<div class="pack-label">Your Top Card</div></div>', unsafe_allow_html=True)
        else:
            st.write("Your pack is empty.")

        st.markdown("---")
        st.markdown(f"""
        <div class="score-box">
            <h3>👤 {st.session_state.human.name}</h3>
            <p style="font-size: 2rem; color: #FFD700; font-weight: bold;">{st.session_state.human.get_points()} pts</p>
            <p>Cards: {len(st.session_state.human.side_deck)}</p>
        </div>
        <div class="score-box">
            <h3>🤖 Computer</h3>
            <p style="font-size: 2rem; color: #FFD700; font-weight: bold;">{st.session_state.computer.get_points()} pts</p>
            <p>Cards: {len(st.session_state.computer.side_deck)}</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔄 New Game"):
            st.session_state.clear()
            st.rerun()

    st.info(f"🎯 {st.session_state.message}")

    if st.session_state.game_over:
        st.success(" GAME OVER! 🏁")
        if 'end_sweep_message' in st.session_state:
            st.markdown(f'<div class="end-sweep-box">{st.session_state.end_sweep_message}</div>', unsafe_allow_html=True)
        
        h_pts = st.session_state.human.get_points()
        c_pts = st.session_state.computer.get_points()
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if h_pts > c_pts:
                st.balloons()
                st.success(f" {st.session_state.human.name} WINS! 🎉")
            elif c_pts > h_pts:
                st.error(f"🤖 Computer WINS!")
            else:
                st.warning("🤝 It's a TIE!")
            st.markdown(f"### Final Score: {h_pts} - {c_pts}")
        return

    st.markdown("### 🃏 The Table")
    st.markdown('<div class="table-area">', unsafe_allow_html=True)
    table_empty = True
    
    if st.session_state.table_builds:
        table_empty = False
        for i, build in enumerate(st.session_state.table_builds):
            is_selected = (st.session_state.selected_build_idx == i)
            border = "border: 3px solid #00ff88; box-shadow: 0 0 20px #00ff88;" if is_selected else ""
            build_html = render_build(build)
            st.markdown(f'<div style="{border} display: inline-block;">{build_html}</div>', unsafe_allow_html=True)
            if st.button(f"Select Build {build['value']}", key=f"sel_build_{i}"):
                st.session_state.selected_build_idx = i
                st.session_state.selected_table_cards = []
                st.rerun()

    if st.session_state.table_cards:
        table_empty = False
        for i, card in enumerate(st.session_state.table_cards):
            is_selected = (i in st.session_state.selected_table_cards)
            card_html = render_playing_card(card, is_selected)
            st.markdown(f'<div style="display: inline-block;">{card_html}</div>', unsafe_allow_html=True)
            btn_text = "✓ Selected" if is_selected else f"Select {card}"
            if st.button(btn_text, key=f"sel_table_{i}", type="primary" if is_selected else "secondary"):
                if i in st.session_state.selected_table_cards:
                    st.session_state.selected_table_cards.remove(i)
                else:
                    st.session_state.selected_table_cards.append(i)
                st.session_state.selected_build_idx = None
                st.rerun()

    if table_empty:
        st.markdown("<p style='text-align: center; color: white; font-style: italic; width: 100%; font-size: 1.2rem;'>Table is empty</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    human = st.session_state.human
    computer = st.session_state.computer
    
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
            border = "border: 3px solid #FFD700; box-shadow: 0 0 20px #FFD700;" if is_selected else ""
            card_html = render_playing_card(card)
            st.markdown(f'<div style="{border} display: inline-block;">{card_html}</div>', unsafe_allow_html=True)
            if st.button(f"Select", key=f"sel_hand_{idx}", type="primary" if is_selected else "secondary"):
                st.session_state.selected_hand_idx = idx
                st.session_state.selected_build_idx = None
                st.session_state.selected_table_cards = []
                st.rerun()

    if st.session_state.selected_hand_idx is not None:
        selected_card = human.hand[st.session_state.selected_hand_idx]
        
        throw_disabled = False
        warning_message = ""
        
        if st.session_state.round_num == 1:
            human_builds = [b for b in st.session_state.table_builds if b['owner'] == human.name]
            if human_builds:
                can_capture_own_build = any(selected_card.numeric_value == build['value'] for build in human_builds)
                can_build_on_own = False
                for build in human_builds:
                    for t_card in st.session_state.table_cards:
                        if selected_card.numeric_value + t_card.numeric_value == build['value']:
                            can_build_on_own = True
                            break
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
            st.markdown("**2. Hit / Sweep (Capture)**")
            st.caption("Select card(s)/build on table first!")
            
            if len(st.session_state.selected_table_cards) == 1:
                t_idx = st.session_state.selected_table_cards[0]
                t_card = st.session_state.table_cards[t_idx]
                if t_card.numeric_value == selected_card.numeric_value:
                    if st.button(f"Hit {t_card}", key="act_hit_single", use_container_width=True):
                        st.session_state.table_cards.pop(t_idx)
                        human.hand.pop(st.session_state.selected_hand_idx)
                        human.side_deck.extend([selected_card, t_card])
                        st.session_state.last_capturer = human
                        st.session_state.message = f" You Hit {t_card} with {selected_card}!"
                        st.session_state.selected_hand_idx = None
                        st.session_state.selected_table_cards = []
                        computer_turn()
                        check_round_end()
                        st.rerun()

            if len(st.session_state.selected_table_cards) >= 2:
                selected_cards_sum = sum(st.session_state.table_cards[i].numeric_value for i in st.session_state.selected_table_cards)
                if selected_cards_sum == selected_card.numeric_value:
                    st.markdown(f'<div class="sweep-info">🧹 SWEEP: {selected_cards_sum} = {selected_card.numeric_value}!</div>', unsafe_allow_html=True)
                    if st.button("🧹 SWEEP TABLE!", key="act_sweep", use_container_width=True):
                        cards_to_capture = [st.session_state.table_cards[i] for i in sorted(st.session_state.selected_table_cards, reverse=True)]
                        for idx in sorted(st.session_state.selected_table_cards, reverse=True):
                            st.session_state.table_cards.pop(idx)
                        human.hand.pop(st.session_state.selected_hand_idx)
                        human.side_deck.append(selected_card)
                        human.side_deck.extend(cards_to_capture)
                        st.session_state.last_capturer = human
                        st.session_state.message = f"👤 You Swept {len(cards_to_capture)} cards with {selected_card}!"
                        st.session_state.selected_hand_idx = None
                        st.session_state.selected_table_cards = []
                        computer_turn()
                        check_round_end()
                        st.rerun()
                else:
                    st.warning(f"Selected cards sum to {selected_cards_sum}, not {selected_card.numeric_value}")

            if st.session_state.selected_build_idx is not None:
                build = st.session_state.table_builds[st.session_state.selected_build_idx]
                if build['value'] == selected_card.numeric_value:
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

        with col3:
            st.markdown("**3. Build**")
            can_build = False
            
            if len(st.session_state.selected_table_cards) == 1:
                t_idx = st.session_state.selected_table_cards[0]
                t_card = st.session_state.table_cards[t_idx]
                
                build_value = selected_card.numeric_value + t_card.numeric_value
                if build_value <= 10:
                    has_build_card = any(c.numeric_value == build_value for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                    if has_build_card:
                        can_build = True
                        existing_build = next((b for b in st.session_state.table_builds if b['value'] == build_value and b['owner'] == human.name), None)
                        if not existing_build:
                            existing_build = next((b for b in st.session_state.table_builds if b['value'] == build_value), None)

                        btn_text = f"Add to Build {build_value}" if existing_build else f"Build {build_value}"
                        if st.button(btn_text, key="act_build_card", use_container_width=True):
                            if existing_build:
                                base = sorted(existing_build['cards'] + [t_card], key=lambda c: c.numeric_value)
                                existing_build['cards'] = base + [selected_card]
                                existing_build['owner'] = human.name
                                st.session_state.table_cards.pop(t_idx)
                                human.hand.pop(st.session_state.selected_hand_idx)
                                
                                # Check auto-capture
                                auto_card = check_auto_capture(build_value, human)
                                if auto_card:
                                    existing_build['cards'].append(auto_card)
                                    st.session_state.message = f"👤 Added to Build {build_value} + AUTO-CAPTURED Computer's {auto_card}!"
                                else:
                                    st.session_state.message = f"👤 Added to existing Build {build_value}!"
                            else:
                                build_cards = [t_card, selected_card]
                                st.session_state.table_builds.append({'cards': build_cards, 'value': build_value, 'owner': human.name})
                                st.session_state.table_cards.pop(t_idx)
                                human.hand.pop(st.session_state.selected_hand_idx)
                                
                                # Check auto-capture
                                auto_card = check_auto_capture(build_value, human)
                                if auto_card:
                                    st.session_state.table_builds[-1]['cards'].append(auto_card)
                                    st.session_state.message = f"👤 Built {build_value} + AUTO-CAPTURED Computer's {auto_card}!"
                                else:
                                    st.session_state.message = f"👤 Built {build_value}!"
                            st.session_state.selected_hand_idx = None
                            st.session_state.selected_table_cards = []
                            computer_turn()
                            check_round_end()
                            st.rerun()

                if computer.side_deck:
                    opp_top = computer.side_deck[-1]
                    build_value_opp = selected_card.numeric_value + t_card.numeric_value + opp_top.numeric_value
                    
                    if build_value_opp <= 10:
                        has_build_card_opp = any(c.numeric_value == build_value_opp for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                        if has_build_card_opp:
                            can_build = True
                            st.caption(f"Opponent's Top: {opp_top}")
                            existing_build = next((b for b in st.session_state.table_builds if b['value'] == build_value_opp), None)
                            btn_text = f"Build {build_value_opp} (uses {opp_top})"
                            if existing_build:
                                btn_text = f"Add to Build {build_value_opp} (uses {opp_top})"
                                
                            if st.button(btn_text, key="act_build_opp", use_container_width=True):
                                if existing_build:
                                    merged_base = sorted(existing_build['cards'] + [t_card, opp_top], key=lambda c: c.numeric_value)
                                    existing_build['cards'] = merged_base + [selected_card]
                                    existing_build['owner'] = human.name
                                    st.session_state.table_cards.pop(t_idx)
                                    computer.side_deck.pop()
                                    human.hand.pop(st.session_state.selected_hand_idx)
                                    st.session_state.message = f"👤 Added to Build {build_value_opp} using Computer's {opp_top}!"
                                else:
                                    base_cards = sorted([t_card, opp_top], key=lambda c: c.numeric_value)
                                    build_cards = base_cards + [selected_card]
                                    st.session_state.table_builds.append({'cards': build_cards, 'value': build_value_opp, 'owner': human.name})
                                    st.session_state.table_cards.pop(t_idx)
                                    computer.side_deck.pop()
                                    human.hand.pop(st.session_state.selected_hand_idx)
                                    st.session_state.message = f"👤 Built {build_value_opp} using Computer's {opp_top}!"
                                st.session_state.selected_hand_idx = None
                                st.session_state.selected_table_cards = []
                                computer_turn()
                                check_round_end()
                                st.rerun()

            elif st.session_state.selected_build_idx is not None:
                build = st.session_state.table_builds[st.session_state.selected_build_idx]
                new_build_value = selected_card.numeric_value + build['value']
                if new_build_value <= 10:
                    has_build_card = any(c.numeric_value == new_build_value for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                    if has_build_card:
                        can_build = True
                        st.caption(f"Add {selected_card} to Build {build['value']} to make Build {new_build_value}")
                        
                        target_build = next((b for b in st.session_state.table_builds if b['value'] == new_build_value and b is not build), None)

                        if st.button(f"Build on {build['value']} → {new_build_value}", key="act_build_on_build", use_container_width=True):
                            if target_build:
                                base_cards = sorted(target_build['cards'] + build['cards'], key=lambda c: c.numeric_value)
                                target_build['cards'] = base_cards + [selected_card]
                                target_build['owner'] = human.name
                                st.session_state.table_builds.remove(build)
                                human.hand.pop(st.session_state.selected_hand_idx)
                                st.session_state.message = f"👤 Built on Build to make {new_build_value} (Merged into existing Build)!"
                            else:
                                build['cards'] = build['cards'] + [selected_card]
                                build['value'] = new_build_value
                                build['owner'] = human.name
                                human.hand.pop(st.session_state.selected_hand_idx)
                                st.session_state.message = f"👤 Built on Build to make Build {new_build_value}!"
                            
                            st.session_state.selected_hand_idx = None
                            computer_turn()
                            check_round_end()
                            st.rerun()
                    else:
                        st.error(f"You need a {new_build_value} in hand to build this!")
                else:
                    st.error(f"New build value {new_build_value} exceeds 10!")
            else:
                st.caption("Select a table card or build first to build.")

        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()