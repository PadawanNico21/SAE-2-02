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
    auto_det = {
        "alphabet": auto['alphabet'],
        "etats": set(),
        "transitions": [],
        "I": [],
        "F": []
    }

    if isinstance(auto['I'], list):
        auto_det['I'].append(auto['I'])

    transi_vus = []

    for transition in auto['transitions']:
        transi = [transition[0], transition[1]]

        if transi in transi_vus:
            # jsp
            pass

        else: transi_vus.append([transition[0], transition[1]])


def renommage(auto: dict) -> dict:
    auto_renom = {
        "alphabet": auto['alphabet'],
        "etats": [],
        "transitions": [],
        "I": set(),
        "F": set()
    }
    liste_etats = list(auto["etats"])

    for etat_initial in auto['I']:
         auto_renom['I'].add(liste_etats.index(etat_initial))

    for etat_final in auto['F']:
        auto_renom['F'].add(liste_etats.index(etat_final))

    for i in range(len(liste_etats)):
        auto_renom['etats'].append(i)
    
    for transition in auto['transitions']:
        etat_i, etat_f = liste_etats.index(transition[0]), liste_etats.index(transition[2])
        transition_renom = [auto_renom['etats'][etat_i], transition[1], auto_renom['etats'][etat_f]]

        auto_renom["transitions"].append(transition_renom)

    auto_renom["etats"] = set(auto_renom["etats"])

    return auto_renom


def inter(auto1: dict, auto2: dict) -> dict:
    if not deterministe(auto1):
        auto1 = renommage(determinise(auto1))

    if not deterministe(auto2):
        auto2 = renommage(determinise(auto2))
    
    transitions = []
    initiaux = set()
    finaux = set()

    for i1 in auto1['I']:
        for i2 in auto2['I']:
                initiaux.add((i1, i2))

    sorties = set(initiaux)

    ajout = True
    while ajout:
        ajout = False
        for transition_a in auto1['transitions']:
            for transition_b in auto2['transitions']:
                if transition_a[1] == transition_b[1]:
                    if (transition_a[0], transition_b[0]) not in sorties:
                        continue
                    sortie = (transition_a[2], transition_b[2])
                    ajout = sortie not in sorties
                    sorties.add((transition_a[2], transition_b[2]))

    for transition_a in auto1['transitions']:
        for transition_b in auto2['transitions']:
            if transition_a[1] == transition_b[1]:
                entree =(transition_a[0], transition_b[0])

                if entree in sorties:
                    transitions.append([entree, transition_a[1], (transition_a[2], transition_b[2])])


    for f1 in auto1['F']:
        for f2 in auto2['F']:
            finaux.add((f1, f2))

    auto_inter = {
        "alphabet": auto1['alphabet'] & auto2['alphabet'],
        "etats": set(),
        "transitions": transitions,
        "I": initiaux,
        "F": finaux
    }

    ajoute_etats(auto_inter)

    return auto_inter


def ajoute_etats(auto: dict) -> dict:
    """
    Prend en paramètre un automate avec des transitions et rajoute ses etats manquants 
    """
    for transition in auto['transitions']:
        auto['etats'].add(transition[0])
        auto['etats'].add(transition[2]) 


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
        "F":[1]
    }

    print(deterministe(auto0))
    print(deterministe(auto2))

    auto2_det = {
        'alphabet': {'a', 'b'}, 'I': [[0]],
        'transitions': [[[0], 'a', [0, 1]], [[0, 1], 'a', [0, 1]], [[0, 1], 'b', [1]], [[1], 'a', [1]], [[1], 'b', [1]]],
        'etats': [[0], [0, 1], [1]], 'F': [[0, 1], [1]]
    }

    print(renommage(auto2_det)) # à modifier par print(renommage(determinise(auto2_det)))

    auto4 = {
        "alphabet":{'a','b'},
        "etats": {0,1,2,},
        "transitions":[[0,'a',1],[1,'b',2],[2,'b',2],[2,'a',2]], 
        "I":{0},
        "F":{2}
    }
    
    auto5 = {
        "alphabet":{'a','b'},
        "etats": {0,1,2},
        "transitions":[[0,'a',0],[0,'b',1],[1,'a',1],[1,'b',2],[2,'a',2],[2,'b',0]],
        "I":{0},
        "F":{0,1}
    }

    print("\nIntersection :")
    print((inter(auto4,auto5)))