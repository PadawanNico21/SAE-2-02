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


def deterministe(auto: dict) -> bool:
    transitions_vus = dict()

    for etat in auto['etats']:
        transitions_vus[etat] = dict()

        for lettre in auto['alphabet']:
            transitions_vus[etat][lettre] = 0

    for transition in auto['transitions']:
        etat, lettre = transition[0], transition[1]

        if transitions_vus[etat][lettre] == 0:
            transitions_vus[etat][lettre] = 1 

        else : return False

    return True


def determinise(auto: dict) -> dict:
    
    a_faire = []
    faits = set()

    transitions = list(auto['transitions'])

    nouvelles_transtions = []

    for etat in auto['I']:
        val = frozenset([etat])
        a_faire.append(val)
        faits.add(val)

    while len(a_faire) > 0:
        etat = a_faire.pop()

        for lettre in auto['alphabet']:
            nouvel_etat = set()
            for t in transitions:
                if t[0] in etat and t[1] == lettre:
                    nouvel_etat.add(t[2])
            val = frozenset(nouvel_etat)
            if len(val) == 0:
                continue

            transitions.append([etat, lettre, val])

            nouvelles_transtions.append([etat, lettre, val])

            if val not in faits:
                a_faire.append(val)
                faits.add(val)
    
    etats_finaux = set()

    for transition in nouvelles_transtions:
        if len(auto['F'] & transition[2]) > 0:
            etats_finaux.add(transition[2])

    return {
        "alphabet": set(auto['alphabet']),
        "etats": faits,
        "transtitions": nouvelles_transtions,
        "I": set(auto['I']),
        "F": etats_finaux,
    }


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

    auto0 ={
        "alphabet":['a','b'],
        "etats": [0,1,2,3],
        "transitions":[[0,'a',1],[1,'a',1],[1,'b',2],[2,'a',3]], 
        "I":[0],
        "F":[3]
    }

    auto1 ={
        "alphabet":['a','b'],
        "etats": [0,1],
        "transitions":[[0,'a',0],[0,'b',1],[1,'b',1],[1,'a',1]], 
        "I":[0],
        "F":[1]
    }

    auto2={
        "alphabet":['a','b'],
        "etats": [0,1],
        "transitions":[[0,'a',0],[0,'a',1],[1,'b',1],[1,'a',1]], 
        "I":[0],
        "F":{1}
    }

    print(deterministe(auto0))
    print(deterministe(auto2))

    print(determinise(auto2))