"""
Structures de données classiques en Python : Pile, File, ABR
"""

## 1. Pile (Stack)
class Pile:
    def __init__(self):
        self.elements = []

    def est_vide(self):
        return len(self.elements) == 0

    def empiler(self, element):
        self.elements.append(element)

    def depiler(self):
        if self.est_vide():
            raise IndexError("Pile vide")
        return self.elements.pop()

    def sommet(self):
        if self.est_vide():
            raise IndexError("Pile vide")
        return self.elements[-1]

    def taille(self):
        return len(self.elements)

    def afficher(self):
        print("Pile :", self.elements)

    def inverser(self):
        self.elements.reverse()

    def copier(self):
        nouvelle_pile = Pile()
        nouvelle_pile.elements = self.elements.copy()
        return nouvelle_pile

## 2. File (Queue)
class File:
    def __init__(self):
        self.elements = []

    def est_vide(self):
        return len(self.elements) == 0

    def enfiler(self, element):
        self.elements.append(element)

    def defiler(self):
        if self.est_vide():
            raise IndexError("File vide")
        return self.elements.pop(0)

    def tete(self):
        if self.est_vide():
            raise IndexError("File vide")
        return self.elements[0]

    def taille(self):
        return len(self.elements)

    def afficher(self):
        print("File :", self.elements)

    def inverser(self):
        self.elements.reverse()

    def file_circulaire(self, capacite):
        self.capacite = capacite
        self.elements = [None] * capacite
        self.debut = 0
        self.fin = 0
        self.pleine = False

    def enfiler_circulaire(self, element):
        if self.pleine:
            raise IndexError("File circulaire pleine")
        self.elements[self.fin] = element
        self.fin = (self.fin + 1) % self.capacite
        if self.fin == self.debut:
            self.pleine = True

    def defiler_circulaire(self):
        if self.est_vide():
            raise IndexError("File circulaire vide")
        element = self.elements[self.debut]
        self.debut = (self.debut + 1) % self.capacite
        self.pleine = False
        return element

## 3. ABR (Arbre Binaire de Recherche)
class Noeud:
    def __init__(self, valeur):
        self.valeur = valeur
        self.gauche = None
        self.droite = None

class ABR:
    def __init__(self):
        self.racine = None

    def inserer(self, valeur):
        if self.racine is None:
            self.racine = Noeud(valeur)
        else:
            self._inserer_recursif(self.racine, valeur)

    def _inserer_recursif(self, noeud, valeur):
        if valeur < noeud.valeur:
            if noeud.gauche is None:
                noeud.gauche = Noeud(valeur)
            else:
                self._inserer_recursif(noeud.gauche, valeur)
        else:
            if noeud.droite is None:
                noeud.droite = Noeud(valeur)
            else:
                self._inserer_recursif(noeud.droite, valeur)

    def rechercher(self, valeur):
        return self._rechercher_recursif(self.racine, valeur)

    def _rechercher_recursif(self, noeud, valeur):
        if noeud is None:
            return False
        if noeud.valeur == valeur:
            return True
        elif valeur < noeud.valeur:
            return self._rechercher_recursif(noeud.gauche, valeur)
        else:
            return self._rechercher_recursif(noeud.droite, valeur)

    def supprimer(self, valeur):
        self.racine = self._supprimer_recursif(self.racine, valeur)

    def _supprimer_recursif(self, noeud, valeur):
        if noeud is None:
            return noeud
        if valeur < noeud.valeur:
            noeud.gauche = self._supprimer_recursif(noeud.gauche, valeur)
        elif valeur > noeud.valeur:
            noeud.droite = self._supprimer_recursif(noeud.droite, valeur)
        else:
            if noeud.gauche is None:
                return noeud.droite
            elif noeud.droite is None:
                return noeud.gauche
            noeud.valeur = self._trouver_min(noeud.droite).valeur
            noeud.droite = self._supprimer_recursif(noeud.droite, noeud.valeur)
        return noeud

    def _trouver_min(self, noeud):
        while noeud.gauche is not None:
            noeud = noeud.gauche
        return noeud

    def parcours_infixe(self):
        elements = []
        self._parcours_infixe_recursif(self.racine, elements)
        return elements

    def _parcours_infixe_recursif(self, noeud, elements):
        if noeud:
            self._parcours_infixe_recursif(noeud.gauche, elements)
            elements.append(noeud.valeur)
            self._parcours_infixe_recursif(noeud.droite, elements)

    def parcours_prefixe(self):
        elements = []
        self._parcours_prefixe_recursif(self.racine, elements)
        return elements

    def _parcours_prefixe_recursif(self, noeud, elements):
        if noeud:
            elements.append(noeud.valeur)
            self._parcours_prefixe_recursif(noeud.gauche, elements)
            self._parcours_prefixe_recursif(noeud.droite, elements)

    def parcours_postfixe(self):
        elements = []
        self._parcours_postfixe_recursif(self.racine, elements)
        return elements

    def _parcours_postfixe_recursif(self, noeud, elements):
        if noeud:
            self._parcours_postfixe_recursif(noeud.gauche, elements)
            self._parcours_postfixe_recursif(noeud.droite, elements)
            elements.append(noeud.valeur)

    def hauteur(self):
        return self._hauteur_recursif(self.racine)

    def _hauteur_recursif(self, noeud):
        if noeud is None:
            return 0
        return 1 + max(self._hauteur_recursif(noeud.gauche), self._hauteur_recursif(noeud.droite))

    def afficher(self):
        print("Parcours infixe :", self.parcours_infixe())

# Exemple d'utilisation
if __name__ == "__main__":
    print("=== Pile ===")
    pile = Pile()
    pile.empiler(1)
    pile.empiler(2)
    pile.afficher()  # Affiche [1, 2]
    print("Dépilé :", pile.depiler())  # Affiche 2

    print("\n=== File ===")
    file = File()
    file.enfiler(1)
    file.enfiler(2)
    file.afficher()  # Affiche [1, 2]
    print("Défiler :", file.defiler())  # Affiche 1

    print("\n=== ABR ===")
    abr = ABR()
    abr.inserer(5)
    abr.inserer(3)
    abr.inserer(7)
    abr.afficher()  # Affiche [3, 5, 7]
    abr.supprimer(3)
    abr.afficher()  # Affiche [5, 7]
    print("Hauteur :", abr.hauteur())  # Affiche 2