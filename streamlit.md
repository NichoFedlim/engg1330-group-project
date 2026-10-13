# Twist Tac Four — 4×4 Rotating Tic-Tac-Toe with AI

A strategy game where every move rotates the board. Play against an AI opponent
with depth-4 lookahead.

## Play Online
👉 https://twist-tac-four.streamlit.app *(replace with your deployed URL)*

## Run Locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Or Run in the Terminal
```bash
python game.py
```

## Files
- game.py — core game logic (board, AI, rotation, win detection)
- opening.py — CLI title screen and menu (used by the terminal version)
- streamlit_app.py — web interface
- requirements.txt

## How to Play
- You are O, the robot is X. You go first.
- After every move, the outer ring rotates anti-clockwise and the inner
ring rotates clockwise.
- Align 4 in a row (row, column, diagonal) after rotation to win.
- Infinite Mode: when blanks fall below N, a random piece is removed.

## Author
Nicholas Fedlim and Friends

---

## 5. Deploy to Streamlit Cloud (free)

1. Push all files to GitHub:
   ```bash
   git add .
   git commit -m "Add Streamlit web version"
   git push
   ```
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click New app → select your repo → set:
    - Main file path: streamlit_app.py
    - Branch: main
4. Click Deploy. It builds in ~2 minutes.