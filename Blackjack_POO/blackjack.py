import random

# =========================
#       CLASSE CARTE
# =========================
class Card:
    def __init__(self, value, suit):
        self.value = value  # "A", "2", ..., "K"
        self.suit = suit    # "Pique", "Trèfle", "Carreau", "Cœur"

    def __str__(self):
        return f"{self.value} de {self.suit}"


# =========================
#       CLASSE PAQUET
# =========================
class Deck:
    def __init__(self, num_decks=1):
        valeurs = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        couleurs = ["Pique", "Trèfle", "Carreau", "Cœur"]

        self.cards = [
            Card(v, c)
            for _ in range(num_decks)
            for c in couleurs
            for v in valeurs
        ]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            raise ValueError("Le paquet est vide !")
        return self.cards.pop()


# =========================
#       CLASSE MAIN
# =========================
class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        self.cards.append(card)

    def __str__(self):
        return ", ".join(str(c) for c in self.cards)

    def raw_values(self):
        """Retourne les valeurs brutes des cartes pour debug si besoin."""
        return [c.value for c in self.cards]

    def score(self):
        """Calcule le score en gérant les As (1 ou 11)."""
        total = 0
        nb_as = 0

        for card in self.cards:
            v = card.value
            if v in ["J", "Q", "K"]:
                total += 10
            elif v == "A":
                total += 11
                nb_as += 1
            else:
                total += int(v)

        # Ajustement des As si on dépasse 21
        while total > 21 and nb_as > 0:
            total -= 10  # un As passe de 11 à 1
            nb_as -= 1

        return total

    def is_bust(self):
        return self.score() > 21

    def is_blackjack(self):
        return len(self.cards) == 2 and self.score() == 21

    def is_soft(self):
        """Retourne True si la main contient un As compté comme 11 (soft hand)."""
        total = 0
        nb_as = 0

        for card in self.cards:
            v = card.value
            if v in ["J", "Q", "K"]:
                total += 10
            elif v == "A":
                total += 11
                nb_as += 1
            else:
                total += int(v)

        # Si on a au moins un As et qu'on n'a pas eu besoin de descendre en dessous de 21
        return nb_as > 0 and total <= 21


# =========================
#       CLASSE JEU
# =========================
class BlackjackGame:
    def __init__(self, starting_balance=500, num_decks=1):
        self.balance = starting_balance
        self.bet = 0
        self.deck = Deck(num_decks=num_decks)
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    # ---------- UTILITAIRES ----------
    def reset_hands(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()

    def ensure_deck(self):
        """Si le paquet est presque vide, on en recrée un."""
        if len(self.deck.cards) < 15:
            print("\n🔄 Le paquet est presque vide, on le renouvelle.")
            self.deck = Deck(num_decks=1)

    # ---------- GESTION DES MISES ----------
    def ask_bet(self):
        while True:
            print(f"\n💰 Solde actuel : {self.balance} €")
            try:
                mise = int(input("Combien veux-tu miser ? (0 pour quitter) : "))
            except ValueError:
                print("Entre un nombre valide.")
                continue

            if mise == 0:
                return False  # signal pour quitter le jeu
            if mise < 0:
                print("La mise ne peut pas être négative.")
            elif mise > self.balance:
                print("Tu n'as pas assez d'argent pour cette mise.")
            else:
                self.bet = mise
                return True

    # ---------- DISTRIBUTION INITIALE ----------
    def initial_deal(self):
        self.reset_hands()
        self.ensure_deck()

        for _ in range(2):
            self.player_hand.add_card(self.deck.draw())
            self.dealer_hand.add_card(self.deck.draw())

    # ---------- AFFICHAGE ----------
    def show_hands(self, reveal_dealer=False):
        print("\n--- CARTES ---")
        print(f"Joueur : {self.player_hand} (score = {self.player_hand.score()})")
        if reveal_dealer:
            print(f"Croupier : {self.dealer_hand} (score = {self.dealer_hand.score()})")
        else:
            if self.dealer_hand.cards:
                print(f"Croupier : {self.dealer_hand.cards[0]} (+ carte cachée)")
            else:
                print("Croupier : (aucune carte)")

    # ---------- TOUR DU JOUEUR ----------
    def player_turn(self):
        # Gestion d’un éventuel Blackjack naturel
        if self.player_hand.is_blackjack():
            print("\n⭐ Blackjack du joueur !")
            return "stand"  # on ne joue pas plus

        action_done = False
        double_allowed = True  # double seulement au début

        while True:
            self.show_hands(reveal_dealer=False)

            if self.player_hand.is_bust():
                print("\n❌ Tu as dépassé 21 !")
                return "bust"

            print("\nActions possibles :")
            print("  [T] Tirer une carte")
            print("  [R] Rester")
            if double_allowed and self.balance >= self.bet:
                print("  [D] Doubler la mise (une carte puis rester)")

            choix = input("Ton choix : ").strip().lower()

            if choix == "t":
                self.player_hand.add_card(self.deck.draw())
                action_done = True
                double_allowed = False  # après avoir tiré une fois, plus de double
            elif choix == "r":
                if not action_done:
                    # il a le droit de rester dès le début, c'est ok
                    pass
                print("Tu restes.")
                return "stand"
            elif choix == "d" and double_allowed and self.balance >= self.bet:
                # Double down
                print(f"\n💸 Tu doubles ta mise : {self.bet} → {self.bet * 2} €")
                self.balance -= self.bet
                self.bet *= 2
                self.player_hand.add_card(self.deck.draw())
                self.show_hands(reveal_dealer=False)
                if self.player_hand.is_bust():
                    print("\n❌ Tu as dépassé 21 après le double !")
                    return "bust"
                print("Tu as doublé et tu restes.")
                return "stand"
            else:
                print("Choix invalide.")

    # ---------- TOUR DU CROUPIER (BOT) ----------
    def dealer_turn(self):
        print("\n--- Tour du croupier ---")
        self.show_hands(reveal_dealer=True)

        # Si le joueur a bust, pas besoin de jouer
        if self.player_hand.is_bust():
            print("Le joueur a déjà dépassé 21, le croupier ne prend pas de risque.")
            return

        # IA simple : le croupier tire jusqu'à :
        # - au moins 17
        # - et tire aussi sur soft 17 (règle courante de casino)
        while True:
            score = self.dealer_hand.score()
            soft = self.dealer_hand.is_soft()

            if score < 17:
                print(f"\nLe croupier a {score} ({'soft' if soft else 'hard'}), il tire une carte...")
                self.dealer_hand.add_card(self.deck.draw())
                self.show_hands(reveal_dealer=True)
                if self.dealer_hand.is_bust():
                    print("❌ Le croupier dépasse 21 !")
                    break
            elif score == 17 and soft:
                print(f"\nLe croupier a 17 soft, il tire une carte...")
                self.dealer_hand.add_card(self.deck.draw())
                self.show_hands(reveal_dealer=True)
                if self.dealer_hand.is_bust():
                    print("❌ Le croupier dépasse 21 !")
                    break
            else:
                print(f"\nLe croupier reste avec {score}.")
                break

    # ---------- RÉSOLUTION & GAINS ----------
    def settle_round(self):
        player_score = self.player_hand.score()
        dealer_score = self.dealer_hand.score()

        print("\n=== RÉSULTAT FINAL ===")
        self.show_hands(reveal_dealer=True)

        # Cas de Blackjack naturel (seulement 2 cartes au départ)
        player_blackjack = self.player_hand.is_blackjack()
        dealer_blackjack = self.dealer_hand.is_blackjack()

        if player_blackjack and not dealer_blackjack:
            gain = int(self.bet * 1.5)
            print(f"\n⭐ Blackjack ! Tu gagnes {gain} € (paie 3:2).")
            self.balance += self.bet + gain
            return

        if dealer_blackjack and not player_blackjack:
            print("\n😈 Le croupier a Blackjack, tu perds ta mise.")
            # mise déjà retirée
            return

        # Cas standard
        if self.player_hand.is_bust() and self.dealer_hand.is_bust():
            print("\nLes deux dépassent 21... Personne ne gagne, mais tu perds quand même ta mise.")
            # règle maison : le joueur perd, on peut adapter si tu veux
            return

        if self.player_hand.is_bust():
            print("\nTu as dépassé 21, tu perds ta mise.")
            return

        if self.dealer_hand.is_bust():
            print("\nLe croupier dépasse 21, tu gagnes ta mise !")
            self.balance += self.bet * 2
            return

        # Comparaison des scores
        if player_score > dealer_score:
            print("\n✅ Tu bats le croupier, tu gagnes ta mise !")
            self.balance += self.bet * 2
        elif player_score < dealer_score:
            print("\n❌ Le croupier a une meilleure main, tu perds ta mise.")
            # rien à faire, mise déjà retirée
        else:
            print("\n➖ Égalité, ta mise est rendue.")
            self.balance += self.bet

    # ---------- BOUCLE PRINCIPALE ----------
    def play(self):
        print("=== BIENVENUE AU BLACKJACK ===")

        while self.balance > 0:
            if not self.ask_bet():
                print("\nTu quittes la table.")
                break

            # On retire la mise du solde au début de la manche
            self.balance -= self.bet

            self.initial_deal()
            self.show_hands(reveal_dealer=False)

            # Tour du joueur
            result_player = self.player_turn()

            # Tour du croupier si le joueur n'a pas bust
            if result_player != "bust":
                self.dealer_turn()

            # Résolution
            self.settle_round()

            if self.balance <= 0:
                print("\n💀 Tu n'as plus d'argent, la table te remercie...")
                break

            continuer = input("\nVoulez-vous rejouer une manche ? (O/N) : ").strip().lower()
            if continuer != "o":
                print("\nTu quittes la table avec", self.balance, "€.")
                break


# =========================
#       LANCEMENT
# =========================
if __name__ == "__main__":
    game = BlackjackGame(starting_balance=500, num_decks=1)
    game.play()

    print("\n=== FIN DU JEU ===")