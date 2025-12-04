from flask import Flask, render_template, redirect, url_for, request
from blackjack import BlackjackGame

app = Flask(__name__)
app.secret_key = "change_this_secret_key"

# Une instance globale du jeu
game = BlackjackGame(starting_balance=500)


@app.route("/")
def index():
    error = request.args.get("error")
    return render_template(
        "index.html",
        balance=game.balance,
        error=error,
        player_name=game.player_name,
        dealer_name=game.dealer_name,
    )


@app.route("/start", methods=["POST"])
def start():
    # nom du joueur
    name = request.form.get("player_name", "").strip()
    if name:
        game.player_name = name

    # mise
    try:
        bet_str = request.form.get("bet", "0")
        bet = int(bet_str)
    except ValueError:
        return redirect(url_for("index", error="Mise invalide."))

    if not game.can_bet(bet):
        return redirect(url_for("index", error="Mise impossible (montant trop élevé ou nulle)."))

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
        player_name=game.player_name,
        dealer_name=game.dealer_name,
    )


@app.route("/hit")
def hit():
    game.player_hit()
    if game.finished:
        game.dealer_turn()   # ne fait rien si le joueur est bust
        game.resolve_round()
    return redirect(url_for("game_page"))


@app.route("/stand")
def stand():
    game.player_stand()
    game.dealer_turn()
    game.resolve_round()
    return redirect(url_for("game_page"))


@app.route("/reset-balance")
def reset_balance():
    game.reset_balance()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
