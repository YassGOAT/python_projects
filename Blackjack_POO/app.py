from flask import Flask, render_template, redirect, url_for
from blackjack import BlackjackGame

app = Flask(__name__)
app.secret_key = "change_this_secret_key"  # à changer plus tard

# Pour l'instant : une seule partie globale
game = BlackjackGame()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start")
def start():
    game.start_new_game()
    return redirect(url_for("game_page"))

@app.route("/game")
def game_page():
    return render_template(
        "game.html",
        player_hand=game.player_hand,
        dealer_hand=game.dealer_hand,
        player_score=game.player_hand.score(),
        dealer_score=game.dealer_hand.score() if game.finished else None,
        finished=game.finished,
        message=game.message
    )

@app.route("/hit")
def hit():
    # tirer une carte pour le joueur
    game.player_hit()
    return redirect(url_for("game_page"))

@app.route("/stand")
def stand():
    # le joueur reste, le croupier joue, puis on résout
    game.player_stand()
    game.dealer_turn()
    game.resolve_round()
    return redirect(url_for("game_page"))


if __name__ == "__main__":
    app.run(debug=True)
