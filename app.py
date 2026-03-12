from flask import Flask, render_template, request, jsonify
import chess

app = Flask(__name__)

# This handles the actual chess rules (King, Queen, Knight movement, etc.)
game_board = chess.Board()

# --- ROUTES ---

@app.route('/')
def index():
    """Renders the main chessboard."""
    return render_template('index.html')

@app.route('/rules')
def rules_page():
    """Renders the rules page with data passed from Python."""
    chess_rules = {
        "title": "ŠKOLNÍ ŠACHY - PRAVIDLA",
        "pieces": [
            {"name": "Král (♔)", "move": "1 pole jakýmkoliv směrem. Nesmí vstoupit do šachu."},
            {"name": "Dáma (♕)", "move": "Libovolný počet polí vodorovně, svisle i diagonálně."},
            {"name": "Věž (♖)", "move": "Libovolný počet polí vodorovně nebo svisle."},
            {"name": "Střelec (♗)", "move": "Libovolný počet polí diagonálně. Zůstává na své barvě."},
            {"name": "Jezdec (♘)", "move": "Skáče do tvaru písmene 'L'. Jako jediný přeskakuje figurky."},
            {"name": "Pěšec (♙)", "move": "Vpřed o 1 pole (o 2 při prvním tahu). Bere diagonálně."}
        ],
        "special": [
            "Rošáda: Tah králem a věží (pokud se nehýbali).",
            "En Passant: Speciální braní pěšcem.",
            "Proměna: Pěšec se na konci desky změní na silnější figuru."
        ]
    }
    return render_template('rules.html', rules=chess_rules)

# --- GAME API ---

@app.route('/move', methods=['POST'])
def make_move():
    """Validates the move using the python-chess library."""
    global game_board
    data = request.json
    move_uci = data.get('move') # Example: "e2e4"
    
    try:
        move = chess.Move.from_uci(move_uci)
        
        # Checking against the rules of Chess
        if move in game_board.legal_moves:
            game_board.push(move)
            return jsonify({
                "status": "success",
                "fen": game_board.fen(),
                "turn": "white" if game_board.turn == chess.WHITE else "black",
                "check": game_board.is_check(),
                "checkmate": game_board.is_checkmate(),
                "stalemate": game_board.is_stalemate()
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "Neplatný tah! Tato figurka se takto hýbat nemůže."
            })
    except:
        return jsonify({"status": "error", "message": "Chyba v komunikaci se serverem."})

@app.route('/reset', methods=['POST'])
def reset_game():
    """Restarts the board to starting position."""
    global game_board
    game_board = chess.Board()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # Starts the server
    print("Server běží na http://127.0.0.1:5000")
    app.run(debug=True) 