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
    st.session_state.message = " Round 1 started!"
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
    st.session_state.message = "🎯 Round 2 (Final Round)!"
    st.session_state.selected_hand_idx = None
    st.session_state.selected_build_idx = None
    st.session_state.selected_table_cards = []

def check_auto_capture(build_value, builder):
    """
    Checks for auto-capture rules after a build is made.
    1. Exact match: Opponent top card == build value.
    2. Sum match: Opponent top card + Table card == build value.
    Returns a list of captured cards.
    """
    opponent = st.session_state.computer if builder == st.session_state.human else st.session_state.human
    captured = []
    
    if not opponent.side_deck:
        return captured
        
    top_card = opponent.side_deck[-1]
    
    # Rule 1: Exact match
    if top_card.numeric_value == build_value:
        captured.append(opponent.side_deck.pop())
        return captured
        
    # Rule 2: Sum match (Top card + Table card)
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

    # 1. Hit single
    for h_idx, h_card in enumerate(comp.hand):
        for t_idx, t_card in enumerate(table_cards):
            if h_card.numeric_value == t_card.numeric_value:
                table_cards.pop(t_idx); comp.hand.pop(h_idx)
                comp.side_deck.extend([h_card, t_card])
                st.session_state.last_capturer = comp
                st.session_state.message = f" Hit {t_card} with {h_card}!"
                return

    # 2. Sweep sum
    for h_idx, h_card in enumerate(comp.hand):
        for i in range(len(table_cards)):
            for j in range(i + 1, len(table_cards)):
                if table_cards[i].numeric_value + table_cards[j].numeric_value == h_card.numeric_value:
                    c1, c2 = table_cards[i], table_cards[j]
                    for idx in sorted([i, j], reverse=True): table_cards.pop(idx)
                    comp.hand.pop(h_idx); comp.side_deck.extend([h_card, c1, c2])
                    st.session_state.last_capturer = comp
                    st.session_state.message = f"🤖 Swept {c1}+{c2} with {h_card}!"
                    return

    # 3. Steal build
    for h_idx, h_card in enumerate(comp.hand):
        for b_idx, build in enumerate(table_builds):
            if h_card.numeric_value == build['value']:
                comp.hand.pop(h_idx); comp.side_deck.append(h_card); comp.side_deck.extend(build['cards'])
                table_builds.pop(b_idx); st.session_state.last_capturer = comp
                st.session_state.message = f"🤖 Stole Build {build['value']}!"
                return

    # 4. Build
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
                        st.session_state.message = f"🤖 Built {build_value}!" + (f" ⚡ Auto-captured {auto}!" if auto else "")
                        return

    # 5. Throw
    comp.hand.sort(key=lambda c: c.numeric_value)
    played = comp.hand.pop(0); table_cards.append(played)
    st.session_state.message = f"🤖 Threw {played}."

# ==========================================
# 4. MAIN APP UI
# ==========================================
def main():
    st.markdown('<h1 class="main-title"> SA Street Casino 🇿🇦</h1>', unsafe_allow_html=True)
    
    if 'human' not in st.session_state:
        st.markdown("""<div style="text-align:center; padding:50px;">
            <h2 style="color:#FFD700;">Welcome to SA Street Casino!</h2>
            <p>🃏 Ace-10 only. Two rounds.<br>🏗️ Build with opponent's top card.<br>
            🔄 Builds of same number merge.<br>
            ⚡ <b>Auto-Capture:</b> If you build a number, and opponent's top card + table card = that number, they get swept into your build!</p>
        </div>""", unsafe_allow_html=True)
        name = st.text_input("Name", "Player", label_visibility="collapsed")
        if st.button(" Start Game", type="primary"): init_game(name); st.rerun()
        return

    with st.sidebar:
        st.header("📊 Scoreboard")
        st.markdown(f"**Round:** {st.session_state.round_num}/2")
        st.markdown("### 👁️ Opponent's Top Card")
        if st.session_state.computer.side_deck:
            st.markdown(f'<div class="pack-display">{render_playing_card(st.session_state.computer.side_deck[-1])}<div style="color:#aaa; font-size:0.8rem;">Computer\'s Top</div></div>', unsafe_allow_html=True)
        st.markdown("### 👁️ Your Top Card")
        if st.session_state.human.side_deck:
            st.markdown(f'<div class="pack-display">{render_playing_card(st.session_state.human.side_deck[-1])}<div style="color:#aaa; font-size:0.8rem;">Your Top</div></div>', unsafe_allow_html=True)
        
        st.markdown(f"""<div class="score-box"><h3> {st.session_state.human.name}</h3><p style="font-size:2rem; color:#FFD700;">{st.session_state.human.get_points()} pts</p></div>
        <div class="score-box"><h3>🤖 Computer</h3><p style="font-size:2rem; color:#FFD700;">{st.session_state.computer.get_points()} pts</p></div>""", unsafe_allow_html=True)
        if st.button("🔄 New Game"): st.session_state.clear(); st.rerun()

    st.info(f" {st.session_state.message}")

    if st.session_state.game_over:
        st.success(" GAME OVER!")
        if 'end_sweep_message' in st.session_state: st.markdown(f'<div class="sweep-info">{st.session_state.end_sweep_message}</div>', unsafe_allow_html=True)
        h_pts, c_pts = st.session_state.human.get_points(), st.session_state.computer.get_points()
        if h_pts > c_pts: st.balloons(); st.success(f"🎉 {st.session_state.human.name} WINS!")
        elif c_pts > h_pts: st.error("🤖 Computer WINS!")
        else: st.warning("🤝 Tie!")
        return

    st.markdown("### 🃏 The Table")
    st.markdown('<div class="table-area">', unsafe_allow_html=True)
    if st.session_state.table_builds:
        for i, build in enumerate(st.session_state.table_builds):
            is_sel = (st.session_state.selected_build_idx == i)
            border = "border:3px solid #00ff88;" if is_sel else ""
            st.markdown(f'<div style="{border} display:inline-block;">{render_build(build)}</div>', unsafe_allow_html=True)
            if st.button(f"Select Build {build['value']}", key=f"sel_b_{i}"): st.session_state.selected_build_idx = i; st.session_state.selected_table_cards = []; st.rerun()
    if st.session_state.table_cards:
        for i, card in enumerate(st.session_state.table_cards):
            is_sel = (i in st.session_state.selected_table_cards)
            st.markdown(f'<div style="display:inline-block;">{render_playing_card(card, is_sel)}</div>', unsafe_allow_html=True)
            if st.button("✓" if is_sel else f"Select {card}", key=f"sel_t_{i}"):
                if is_sel: st.session_state.selected_table_cards.remove(i)
                else: st.session_state.selected_table_cards.append(i)
                st.session_state.selected_build_idx = None; st.rerun()
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
                st.session_state.selected_hand_idx = idx; st.session_state.selected_build_idx = None; st.session_state.selected_table_cards = []; st.rerun()

    if st.session_state.selected_hand_idx is not None:
        sel_card = human.hand[st.session_state.selected_hand_idx]
        st.markdown('<div class="action-panel">', unsafe_allow_html=True)
        st.markdown(f"#### 🎯 Action for {sel_card} ({sel_card.numeric_value})")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**1. Throw**")
            if st.button("Throw Card", use_container_width=True):
                st.session_state.table_cards.append(human.hand.pop(st.session_state.selected_hand_idx))
                st.session_state.message = f"👤 Threw {sel_card}."; st.session_state.selected_hand_idx = None; computer_turn(); check_round_end(); st.rerun()

        with c2:
            st.markdown("**2. Hit / Sweep**")
            if len(st.session_state.selected_table_cards) == 1:
                t_idx = st.session_state.selected_table_cards[0]
                t_card = st.session_state.table_cards[t_idx]
                if t_card.numeric_value == sel_card.numeric_value:
                    if st.button(f"Hit {t_card}", use_container_width=True):
                        st.session_state.table_cards.pop(t_idx); human.hand.pop(st.session_state.selected_hand_idx)
                        human.side_deck.extend([sel_card, t_card]); st.session_state.last_capturer = human
                        st.session_state.message = f"👤 Hit {t_card}!"; st.session_state.selected_hand_idx = None; computer_turn(); check_round_end(); st.rerun()
            if len(st.session_state.selected_table_cards) >= 2:
                s_sum = sum(st.session_state.table_cards[i].numeric_value for i in st.session_state.selected_table_cards)
                if s_sum == sel_card.numeric_value:
                    st.markdown(f'<div class="sweep-info"> SWEEP: {s_sum} = {sel_card.numeric_value}!</div>', unsafe_allow_html=True)
                    if st.button("🧹 SWEEP!", use_container_width=True):
                        caps = [st.session_state.table_cards[i] for i in sorted(st.session_state.selected_table_cards, reverse=True)]
                        for idx in sorted(st.session_state.selected_table_cards, reverse=True): st.session_state.table_cards.pop(idx)
                        human.hand.pop(st.session_state.selected_hand_idx); human.side_deck.append(sel_card); human.side_deck.extend(caps)
                        st.session_state.last_capturer = human; st.session_state.message = f"👤 Swept {len(caps)} cards!"; st.session_state.selected_hand_idx = None; computer_turn(); check_round_end(); st.rerun()
            if st.session_state.selected_build_idx is not None:
                build = st.session_state.table_builds[st.session_state.selected_build_idx]
                if build['value'] == sel_card.numeric_value:
                    if st.button(f"Steal Build {build['value']}", use_container_width=True):
                        human.hand.pop(st.session_state.selected_hand_idx); human.side_deck.append(sel_card); human.side_deck.extend(build['cards'])
                        st.session_state.table_builds.pop(st.session_state.selected_build_idx); st.session_state.last_capturer = human
                        st.session_state.message = f"👤 Stole Build!"; st.session_state.selected_hand_idx = None; computer_turn(); check_round_end(); st.rerun()

        with c3:
            st.markdown("**3. Build**")
            if len(st.session_state.selected_table_cards) == 1:
                t_idx = st.session_state.selected_table_cards[0]
                t_card = st.session_state.table_cards[t_idx]
                b_val = sel_card.numeric_value + t_card.numeric_value
                if b_val <= 10:
                    has_card = any(c.numeric_value == b_val for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                    if has_card:
                        existing = next((b for b in st.session_state.table_builds if b['value'] == b_val), None)
                        btn = f"Add to Build {b_val}" if existing else f"Build {b_val}"
                        if st.button(btn, use_container_width=True):
                            if existing:
                                base = sorted(existing['cards'] + [t_card], key=lambda c: c.numeric_value)
                                existing['cards'] = base + [sel_card]; existing['owner'] = human.name
                                st.session_state.table_cards.pop(t_idx); human.hand.pop(st.session_state.selected_hand_idx)
                                auto = check_auto_capture(b_val, human)
                                if auto: existing['cards'].extend(auto)
                                st.session_state.message = f"👤 Added to Build {b_val}!" + (f" ⚡ Auto-captured {auto}!" if auto else "")
                            else:
                                st.session_state.table_builds.append({'cards': [t_card, sel_card], 'value': b_val, 'owner': human.name})
                                st.session_state.table_cards.pop(t_idx); human.hand.pop(st.session_state.selected_hand_idx)
                                auto = check_auto_capture(b_val, human)
                                if auto: st.session_state.table_builds[-1]['cards'].extend(auto)
                                st.session_state.message = f" Built {b_val}!" + (f" ⚡ Auto-captured {auto}!" if auto else "")
                            st.session_state.selected_hand_idx = None; computer_turn(); check_round_end(); st.rerun()

                # Build using opponent's top card
                if st.session_state.computer.side_deck:
                    opp_top = st.session_state.computer.side_deck[-1]
                    b_val_opp = sel_card.numeric_value + t_card.numeric_value + opp_top.numeric_value
                    if b_val_opp <= 10:
                        has_card_opp = any(c.numeric_value == b_val_opp for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                        if has_card_opp:
                            existing = next((b for b in st.session_state.table_builds if b['value'] == b_val_opp), None)
                            btn = f"Build {b_val_opp} (uses {opp_top})"
                            if st.button(btn, use_container_width=True):
                                if existing:
                                    merged = sorted(existing['cards'] + [t_card, opp_top], key=lambda c: c.numeric_value)
                                    existing['cards'] = merged + [sel_card]; existing['owner'] = human.name
                                    st.session_state.table_cards.pop(t_idx); st.session_state.computer.side_deck.pop(); human.hand.pop(st.session_state.selected_hand_idx)
                                    st.session_state.message = f"👤 Added to Build {b_val_opp} using {opp_top}!"
                                else:
                                    base = sorted([t_card, opp_top], key=lambda c: c.numeric_value)
                                    st.session_state.table_builds.append({'cards': base + [sel_card], 'value': b_val_opp, 'owner': human.name})
                                    st.session_state.table_cards.pop(t_idx); st.session_state.computer.side_deck.pop(); human.hand.pop(st.session_state.selected_hand_idx)
                                    st.session_state.message = f" Built {b_val_opp} using {opp_top}!"
                                st.session_state.selected_hand_idx = None; computer_turn(); check_round_end(); st.rerun()

            elif st.session_state.selected_build_idx is not None:
                build = st.session_state.table_builds[st.session_state.selected_build_idx]
                new_val = sel_card.numeric_value + build['value']
                if new_val <= 10:
                    has_card = any(c.numeric_value == new_val for i, c in enumerate(human.hand) if i != st.session_state.selected_hand_idx)
                    if has_card:
                        target = next((b for b in st.session_state.table_builds if b['value'] == new_val and b is not build), None)
                        if st.button(f"Build on {build['value']} → {new_val}", use_container_width=True):
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

if __name__ == "__main__":
    main()