import copy
import random
import streamlit as st

from game import (
    GameBoard, Robot, Tree,
    PLAYER_MARKER, ROBOT_MARKER, EMPTY_CELL, total_step
)
import opening


# ---------- Page config ----------
st.set_page_config(page_title="Twist Tac Four", page_icon="🎲", layout="centered")

# ---------- Key mapping for the 4x4 grid ----------
KEY_MAP = [
    ["1", "2", "3", "4"],
    ["q", "w", "e", "r"],
    ["a", "s", "d", "f"],
    ["z", "x", "c", "v"],
]


# ---------- Session state init ----------
def init_state():
    if "game_board" not in st.session_state:
        st.session_state.game_board = GameBoard()
        st.session_state.robot = Robot()
        st.session_state.finished = False
        st.session_state.message = "Your turn. Pick a cell."
        st.session_state.infinimode = 3
        st.session_state.started = False
        st.session_state.winner = None
        st.session_state.robot_thinking = False
        st.session_state.last_removed = None


init_state()


# ---------- Board rendering as an interactive grid ----------
def render_board(board, disabled=False):
    """Render the 4x4 game board as a grid of buttons."""
    for i in range(4):
        cols = st.columns(4)
        for j in range(4):
            cell = board.gameBoard[i][j]
            label = cell if cell != EMPTY_CELL else KEY_MAP[i][j]
            key = f"cell_{i}_{j}"
            # Disable if the cell is occupied or game finished
            is_disabled = disabled or cell != EMPTY_CELL
            if cols[j].button(label, key=key, disabled=is_disabled, use_container_width=True):
                handle_player_move(i, j)


# ---------- Move handling ----------
def handle_player_move(row, col):
    board = st.session_state.game_board
    if st.session_state.finished or board.turn is False:
        return
    if board.gameBoard[row][col] != EMPTY_CELL:
        return

    # Player move
    board.nextMove([col, row])
    board.rotateBoard()

    # Check end
    result = board.checkWin()
    if result != "NotYet":
        end_game(result)
        st.rerun()
        return

    # Infinite mode: random removal after player's move
    if st.session_state.infinimode != -1 and board.blank() < st.session_state.infinimode:
        board.randomRemove()
        st.session_state.last_removed = "A random piece was removed after your move."

    # Now robot's turn
    robot_move()
    st.rerun()


def robot_move():
    board = st.session_state.game_board
    robot = st.session_state.robot

    move = robot.getNextStep(copy.copy(board))
    board.nextMove(copy.copy(move))
    board.rotateBoard()

    result = board.checkWin()
    if result != "NotYet":
        end_game(result)
        return

    # Infinite mode: random removal after robot's move
    if st.session_state.infinimode != -1 and board.blank() < st.session_state.infinimode:
        board.randomRemove()
        st.session_state.last_removed = "A random piece was removed after the robot's move."
    else:
        st.session_state.last_removed = None


def end_game(result):
    st.session_state.finished = True
    if result == PLAYER_MARKER:
        st.session_state.winner = "player"
        st.session_state.message = "🎉 You win! Congratulations."
    elif result == ROBOT_MARKER:
        st.session_state.winner = "robot"
        st.session_state.message = "💀 You lose. Better luck next time."
    else:
        st.session_state.winner = "draw"
        st.session_state.message = "🤝 It's a draw!"


def reset_game():
    st.session_state.game_board = GameBoard()
    st.session_state.robot = Robot()
    st.session_state.finished = False
    st.session_state.message = "Your turn. Pick a cell."
    st.session_state.winner = None
    st.session_state.last_removed = None


# ---------- UI ----------
st.title("🎲 Twist Tac Four")
st.caption("A 4×4 rotating tic-tac-toe against an AI opponent.")

# Sidebar: setup + controls
with st.sidebar:
    st.header("Setup")
    if not st.session_state.started:
        st.session_state.infinimode = st.number_input(
            "Infinite Mode — remove a random piece when blanks < N (0 to disable):",
            min_value=0, max_value=16, value=3, step=1
        )
        if st.session_state.infinimode == 0:
            st.session_state.infinimode = -1

        if st.button("▶ Start Game", use_container_width=True):
            st.session_state.started = True
            reset_game()
            st.rerun()
    else:
        st.write(f"**Infinite Mode:** {'Disabled' if st.session_state.infinimode == -1 else st.session_state.infinimode}")
        if st.button("🔄 Restart Game", use_container_width=True):
            reset_game()
            st.rerun()
        if st.button("⚙ Change Settings", use_container_width=True):
            st.session_state.started = False
            st.rerun()

    st.divider()
    st.markdown("### How to Play")
    st.markdown(
        "- You are **O**, the robot is **X**.\n"
        "- You go first.\n"
        "- After every move, the board rotates:\n"
        "  - Outer ring **anti-clockwise**\n"
        "  - Inner ring **clockwise**\n"
        "- Align **4 in a row** (row, column, or diagonal) after rotation to win."
    )

# Main area
if not st.session_state.started:
    st.info("Configure the options in the sidebar and click **▶ Start Game** to begin.")
else:
    st.subheader(st.session_state.message)
    if st.session_state.last_removed:
        st.warning(st.session_state.last_removed)

    render_board(st.session_state.game_board, disabled=st.session_state.finished)

    if st.session_state.finished:
        st.success(st.session_state.message)
        if st.button("Play Again"):
            reset_game()
            st.rerun()