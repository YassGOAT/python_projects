import random

class Blackjack:
    def __init__(self):
        self.valeurs = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
        self.couleurs = ["Pique", "Trèfle", "Carreau", "Cœur"]
        self.cartes = [(v, c) for c in self.couleurs for v in self.valeurs]
        random.shuffle(self.cartes)

        self.main_joueur = []
        self.main_bot = []

    def tirer_carte(self, joueur):
        """Tire une carte du paquet et l'ajoute à la main du joueur."""
        carte = self.cartes.pop()

        if joueur == "joueur":
            self.main_joueur.append(carte)
        else:
            self.main_bot.append(carte)

        return carte

    def valeur_carte(self, carte):
        """Retourne la valeur brute d'une carte (A = 11 par défaut)."""
        valeur = carte[0]
        if valeur in ["J", "Q", "K"]:
            return 10
        elif valeur == "A":
            return 11
        else:
            return int(valeur)

    def calculer_score(self, main):
        """Calcule le score d'une main en gérant les As (1 ou 11)."""
        total = 0
        nb_as = 0

        for carte in main:
            v = self.valeur_carte(carte)
            total += v
            if carte[0] == "A":
                nb_as += 1

        # Ajustement des As si on dépasse 21
        while total > 21 and nb_as > 0:
            total -= 10   # un As passe de 11 à 1
            nb_as -= 1

        return total

    def afficher_main(self, joueur, cacher_bot=False):
        """Affiche la main et le score du joueur donné.
        cacher_bot=True pour ne montrer qu'une carte du bot au début."""
        if joueur == "joueur":
            main = self.main_joueur
            nom = "Joueur"
            cartes_str = ", ".join([f"{v} de {c}" for (v, c) in main])
            score = self.calculer_score(main)
            print(f"{nom} : {cartes_str} (score = {score})")
        else:
            main = self.main_bot
            nom = "Bot"
            if cacher_bot and len(main) > 0:
                # On montre seulement la première carte
                v, c = main[0]
                print(f"{nom} : {v} de {c} (+ carte cachée)")
            else:
                cartes_str = ", ".join([f"{v} de {c}" for (v, c) in main])
                score = self.calculer_score(main)
                print(f"{nom} : {cartes_str} (score = {score})")

    def distribuer_initial(self):
        """Distribue 2 cartes au joueur et au bot."""
        self.main_joueur = []
        self.main_bot = []
        random.shuffle(self.cartes)

        for _ in range(2):
            self.tirer_carte("joueur")
            self.tirer_carte("bot")

    def tour_joueur(self):
        """Boucle principale pour le joueur : tirer ou rester."""
        while True:
            print("\n--- Tour du joueur ---")
            self.afficher_main("joueur")
            self.afficher_main("bot", cacher_bot=True)

            score_joueur = self.calculer_score(self.main_joueur)
            if score_joueur == 21:
                print("Blackjack !")
                break
            if score_joueur > 21:
                print("Tu as dépassé 21 !")
                break

            choix = input("T pour tirer, R pour rester : ").strip().lower()

            if choix == "t":
                self.tirer_carte("joueur")
            elif choix == "r":
                print("Tu restes.")
                break
            else:
                print("Choix invalide, tape T ou R.")

    def tour_bot(self):
        """Le bot tire jusqu'à au moins 17."""
        print("\n--- Tour du bot ---")
        self.afficher_main("bot")  # maintenant on montre tout

        while self.calculer_score(self.main_bot) < 17:
            print("Le bot tire une carte...")
            self.tirer_carte("bot")
            self.afficher_main("bot")

        score_bot = self.calculer_score(self.main_bot)
        if score_bot > 21:
            print("Le bot a dépassé 21 !")

    def verifier_gagnant(self):
        """Détermine le gagnant à partir des mains actuelles."""
        score_joueur = self.calculer_score(self.main_joueur)
        score_bot = self.calculer_score(self.main_bot)

        print("\n=== Résultat final ===")
        self.afficher_main("joueur")
        self.afficher_main("bot")

        if score_joueur > 21 and score_bot > 21:
            return "Les deux ont dépassé 21, personne ne gagne vraiment..."
        if score_joueur > 21:
            return "Le bot a gagné !"
        if score_bot > 21:
            return "Le joueur a gagné !"
        if score_joueur > score_bot:
            return "Le joueur a gagné !"
        if score_bot > score_joueur:
            return "Le bot a gagné !"
        return "Égalité !"

    def jouer_manche(self):
        """Lance une manche complète de Blackjack."""
        self.distribuer_initial()
        self.tour_joueur()

        # Si le joueur n’a pas bust, le bot joue
        if self.calculer_score(self.main_joueur) <= 21:
            self.tour_bot()

        print(self.verifier_gagnant())

if __name__ == "__main__":
    game = Blackjack()
    game.jouer_manche()


# Exemple d'utilisation
game = Blackjack()

# Distribution initiale
for _ in range(2):
    game.tirer_carte("joueur")
    game.tirer_carte("bot")

game.afficher_main("joueur")
game.afficher_main("bot")

print(game.verifier_gagnant())
