# Structures de données classiques en Python

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

    def parcours_infixe(self):
        elements = []
        self._parcours_infixe_recursif(self.racine, elements)
        return elements

    def _parcours_infixe_recursif(self, noeud, elements):
        if noeud:
            self._parcours_infixe_recursif(noeud.gauche, elements)
            elements.append(noeud.valeur)
            self._parcours_infixe_recursif(noeud.droite, elements)

# Exemple d'utilisation
if __name__ == "__main__":
    pile = Pile()
    pile.empiler(1)
    pile.empiler(2)
    print("Pile :", pile.depiler())  # Affiche 2

    file = File()
    file.enfiler(1)
    file.enfiler(2)
    print("File :", file.defiler())  # Affiche 1

    abr = ABR()
    abr.inserer(5)
    abr.inserer(3)
    abr.inserer(7)
    print("ABR :", abr.parcours_infixe())  # Affiche [3, 5, 7]