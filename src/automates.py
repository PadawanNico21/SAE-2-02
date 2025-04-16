def defauto():
    # A faire
    pass

def lirelettre(transitions: list[list[int | str]], etats: set[int], lettre: str) -> set[int]:
    """
        Renvoie les états dans lesquels on peut arriver en partant d'un état de `etats` et en lisant la lettre `lettre`
    """
    resultat: set[int] = set()

    for transition in transitions:
        if transition[1] == lettre and transition[0] in etats:
            resultat.add(transition[2])

    return resultat

def liremot(transitions: list[list[int | str]], etats: set[int], mot: str) -> set[int]:
    etats_suivants = set(etats)

    for lettre in mot:
        etats_suivants = lirelettre(transitions, etats_suivants, lettre)
        if len(etats_suivants) == 0:
            return etats_suivants

    return etats_suivants


def accepte(auto: dict, mot: str) -> bool:
    return len(liremot(auto['transitions'], auto['I'], mot) & auto['F']) > 0
    

if __name__ == "__main__":
    auto = {
        "alphabet": {"a", "b"},
        "etats": {1, 2, 3, 4},
        "transitions": [[1, "a", 2], [2, "a", 2], [2, "b", 3], [3, "a", 4]],
        "I": {1},
        "F": {4},
    }
    print("lirelettre:", lirelettre(auto["transitions"], auto["etats"], "a"))
    print("liremot:", liremot(auto["transitions"], auto["etats"], "aba"))
    print("accepte aba:", accepte(auto, "aba"))
    print("accepte ba:", accepte(auto, "ba"))
