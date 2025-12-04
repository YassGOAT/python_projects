from flask import Flask, render_template, redirect, url_for, request
from blackjack import BlackjackGame

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

game = BlackjackGame(starting_balance=500)

@app.route("/")
def index():
    error = request.args.get("error")
    return render_template("index.html", balance=game.balance, error=error)

@app.route("/start", methods=["POST"])
def start():
    try:
        bet_str = request.form.get("bet", "0")
        bet = int(bet_str)
    except ValueError:
        return redirect(url_for("index", error="Mise invalide."))

    if not game.can_bet(bet):
        return redirect(url_for("index", error="Mise impossible (montant trop élevé ou nul)."))

    game.start_new_game(bet)
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
        message=game.message,
        balance=game.balance,
        bet=game.bet,
    )

@app.route("/hit")
def hit():
    game.player_hit()
    if game.finished:
        # joueur bust → on finit la manche et on résout
        game.dealer_turn()   # ne fera rien si joueur bust
        game.resolve_round()
    return redirect(url_for("game_page"))

@app.route("/stand")
def stand():
    game.player_stand()
    game.dealer_turn()
    game.resolve_round()
    return redirect(url_for("game_page"))

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/reset-balance")
def reset_balance():
    game.reset_balance()
    return redirect(url_for("index"))
