def concatene(a: set[str], b: set[str]) -> set[str]:
    """
    Concatene les mots des ensembles a et b
    """
    resultat: set[str] = set()

    for droite in a:
        for gauche in b:
            resultat.add(droite + gauche)

    return resultat


def puis(langage: set[str], n: int) -> set[str]:
    """
    Renvoie le langage `langage^n`
    """
    resultat: set[str] = {""}

    for _ in range(n):
        resultat = concatene(resultat, langage)

    return resultat


# 1.2.3 -> On ne peut pas faire de fonction calculant l'étoile d'un langage car la mémoire d'un ordinateur est finis
# alors que l'étoile d'un langage représente une infinitée de mots


def tousmots(alphabet: set[str], n: int) -> set[str]:
    """
    Réalise l'étoile de l'alphabet passé en paramètre pour tous les mots qui ont une longeur inférieurs ou égale à n
    """

    resultat: set[str] = set()

    for i in range(n + 1):
        resultat |= puis(alphabet, i)

    return resultat


if __name__ == "__main__":
    L1 = {"aa", "ab", "ba", "bb"}
    L2 = {"a", "b", ""}
    print("Concaténation L_1 et L_2:", concatene(L1, L2))
    print("L^2:", puis(L1, 2))
    print("A^*, |A| <= 3:", tousmots({"a", "b"}, 3))
