import random

class Card:
    def __init__(self, value, suit):
        self.value = value      # "A", "2", ..., "K"
        self.suit = suit        # "Pique", "Trèfle", "Carreau", "Cœur"

    def __str__(self):
        return f"{self.value} de {self.suit}"


class Deck:
    def __init__(self):
        values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        suits = ["Pique", "Trèfle", "Carreau", "Cœur"]
        self.cards = [Card(v, s) for s in suits for v in values]
        random.shuffle(self.cards)

    def draw(self):
        if not self.cards:
            # on recrée un paquet si vide
            self.__init__()
        return self.cards.pop()


class Hand:
    def __init__(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def score(self):
        total = 0
        aces = 0
        for c in self.cards:
            if c.value in ["J","Q","K"]:
                total += 10
            elif c.value == "A":
                total += 11
                aces += 1
            else:
                total += int(c.value)

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total

    def is_bust(self):
        return self.score() > 21


class BlackjackGame:
    def __init__(self):
        self.balance = 500
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.finished = False
        self.message = ""

    def start_new_game(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.finished = False
        self.message = ""

        # on recrée le deck si presque vide
        if len(self.deck.cards) < 15:
            self.deck = Deck()

        # distribution initiale
        self.player_hand.add(self.deck.draw())
        self.player_hand.add(self.deck.draw())
        self.dealer_hand.add(self.deck.draw())
        self.dealer_hand.add(self.deck.draw())

    def player_hit(self):
        if self.finished:
            return
        self.player_hand.add(self.deck.draw())
        if self.player_hand.is_bust():
            self.finished = True
            self.message = "Tu as dépassé 21. Tu as perdu."

    def player_stand(self):
        if self.finished:
            return
        self.finished = True

    def dealer_turn(self):
        # le croupier ne joue que si le joueur n'a pas déjà bust
        if self.player_hand.is_bust():
            return

        while self.dealer_hand.score() < 17:
            self.dealer_hand.add(self.deck.draw())

    def resolve_round(self):
        ps = self.player_hand.score()
        ds = self.dealer_hand.score()

        if ps > 21:
            self.message = "Tu as dépassé 21. Tu as perdu."
        elif ds > 21:
            self.message = "Le croupier dépasse 21. Tu gagnes !"
        elif ps > ds:
            self.message = "Tu gagnes !"
        elif ps < ds:
            self.message = "Le croupier gagne."
        else:
            self.message = "Égalité."
