def defauto_alphabet(defaut="ab") -> set:
    print("Veuilliez donnez l'alphabet de votre automate (par ex: abcd)")
    alphabet = input(f"({defaut}) > ")

    alphabet_set = set()
    if len(alphabet) == 0:
        print(f"Utilisation de l'alphabet par défaut {defaut}")
        alphabet = defaut

    for lettre in alphabet:
        alphabet_set.add(lettre)

    return alphabet_set


def defauto_etats() -> set:
    etats = set()

    print("Veuilliez saisir les états de votre automate, 'fin' pour stopper la saisie")

    texte = ""
    while texte != "fin":
        n = None
        while n == None:
            texte = input("> ")
            if texte == "fin":
                if len(etats) == 0:
                    print("Vous devez avoir au moins 1 état")
                    continue
                break
            try:
                n = int(texte)
                etats.add(n)
            except:
                print("Valeur incorrecte veuilliez recommencer")

    return etats


def defauto_etats_selection(etats: set, type: str) -> set:
    print(
        f"Veuilliez saisir les états {type} de votre automate, 'fin' pour stopper la saisie"
    )
    selection = set()

    texte = ""
    while texte != "fin":
        n = None
        while n == None:
            texte = input("> ")
            if texte == "fin":
                if len(etats) == 0:
                    print(f"Vous devez avoir au moins 1 état {type}")
                    continue
                break
            try:
                n = int(texte)
                if n not in etats:
                    print("Cet état n'existe pas")
                    n = None
                else:
                    selection.add(n)
            except:
                print("Valeur incorrecte veuilliez recommencer")
    return selection


def defauto_transition_pour(etat: int, etats: set, alphabet: set) -> list:
    print(f"Saisissez les transitions pour l'etat {etat}")

    transitions = []

    while True:
        lettre = ""
        sortie = ""
        print(f"Saisissez la lettre de la transition parmis {", ".join(alphabet)}")
        while lettre not in alphabet:
            lettre = input("> ")
        print("Saisissez l'état de sortie de la transition")
        while sortie not in etats:
            sortie = input("> ")
            try:
                sortie = int(sortie)
            except:
                print("Valeur incorrecte veuilliez recommencer")

        transtion = [etat, lettre, sortie]
        if transtion in transitions:
            print("Attention: Cette transition exite déjà, elle n'est pas ajoutée.")
        else:
            transitions.append(transtion)

        print(f"Arreter de saisir des transitions pour l'état {etat} ?")

        stop = input("[y/N] >")

        if stop.lower() == "y":
            return transitions


def defauto_transitions(etats: set, alphabet: set) -> list:
    transitions = []
    while True:
        print(
            f'Choisissez un état parmis {", ".join(map(str, etats))} ou \'fin\' pour stopper la saisie'
        )
        texte = ""
        while texte not in etats:
            texte = input("> ")
            if texte == "fin":
                return transitions
            try:
                texte = int(texte)
            except:
                print("Valeur incorrecte veuilliez recommencer")

        ajouts = defauto_transition_pour(texte, etats, alphabet)
        for transition in ajouts:
            if transition in transitions:
                print(
                    f"Attention: La transition '{transition[0]}---{transition[1]}-->{transition[2]}' exite déjà, elle n'est pas ajoutée."
                )
            else:
                transitions.append(transition)


def defauto() -> dict:
    print("----- ALPHABET ----")
    alphabet = defauto_alphabet()

    print("------ ETATS ------")
    etats = defauto_etats()

    i = defauto_etats_selection(etats, "initiaux")
    f = defauto_etats_selection(etats, "finaux")

    print("--- TRANSITIONS ---")
    transitions = defauto_transitions(etats, alphabet)

    print("Fin de la saisie de l'automate.")

    return {
        "alphabet": alphabet,
        "etats": etats,
        "I": i,
        "F": f,
        "transitions": transitions,
    }


def lirelettre(
    transitions: list[list[int | str]], etats: set[int], lettre: str
) -> set[int]:
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
    return len(liremot(auto["transitions"], auto["I"], mot) & auto["F"]) > 0


def langage_accept(automate: dict, n: int) -> set:
    initial = {}

    for etat in automate["I"]:
        for transition in automate["transitions"]:
            if transition[0] == etat:
                if transition[2] not in initial:
                    initial[transition[2]] = []
                initial[transition[2]].append(transition[1])

    return langage_accept_rec(automate, initial, set(), n - 1)


def langage_accept_rec(automate: dict, positions: dict, resultat_mots: set, n: int):
    if n <= 0:
        return resultat_mots

    nouvelle_positions = {}

    for etat, mots in positions.items():
        for mot in mots:
            for transition in automate["transitions"]:
                if transition[0] != etat:
                    continue

                if transition[2] not in nouvelle_positions:
                    nouvelle_positions[transition[2]] = []

                if transition[2] in automate["F"]:
                    resultat_mots.add(mot + transition[1])

                nouvelle_positions[transition[2]].append(mot + transition[1])

    return langage_accept_rec(automate, nouvelle_positions, resultat_mots, n - 1)


def liste_transitions_manquantes(auto: dict) -> dict:
    manquants = {}

    for etat in auto["etats"]:
        manquants[etat] = set()
        for lettre in auto["alphabet"]:
            manquants[etat].add(lettre)

    for etat, lettres in manquants.items():
        for transition in auto["transitions"]:
            for lettre in set(lettres):
                if transition[0] == etat and transition[1] == lettre:
                    lettres.remove(lettre)

    return manquants


def complet(auto: dict) -> bool:
    for lettres in liste_transitions_manquantes(auto).values():
        if len(lettres) != 0:
            return False

    return True


def complete(auto: dict) -> dict:
    manquants = liste_transitions_manquantes(auto)

    auto_modif = dict(auto)

    puis = max(auto_modif["etats"]) + 1
    auto_modif["etats"].add(puis)

    for etat, lettres in manquants.items():
        for lettre in lettres:
            auto_modif["transitions"].append([etat, lettre, puis])

    return auto_modif


def complement(auto: dict) -> dict:
    auto_complet = complete(auto)

    for etat in auto_complet["etats"]:
        if etat in auto_complet["F"]:
            auto_complet["F"].remove(etat)
        else:
            auto_complet["F"].add(etat)
    return auto_complet


def prefixe(auto: dict) -> dict:
    auto_prefixe = dict(auto)

    auto_prefixe["F"] = set(auto_prefixe["etats"])

    return auto_prefixe


def suffixe(auto: dict) -> dict:
    auto_suffixe = dict(auto)

    auto_suffixe["I"] = set(auto_suffixe["etats"])

    return auto_suffixe


def facteur(auto: dict) -> dict:
    return suffixe(prefixe(auto))


def mirroir(auto: dict) -> dict:
    auto_mirroir = dict(auto)

    auto_mirroir["I"], auto_mirroir["F"] = auto_mirroir["F"], auto_mirroir["I"]

    for transiton in auto_mirroir["transitions"]:
        transiton[0], transiton[2] = transiton[2], transiton[0]

    return auto_mirroir


def deterministe(auto: dict) -> bool:
    transitions_vus = dict()

    for etat in auto["etats"]:
        transitions_vus[etat] = dict()

        for lettre in auto["alphabet"]:
            transitions_vus[etat][lettre] = 0

    for transition in auto["transitions"]:
        etat, lettre = transition[0], transition[1]

        if transitions_vus[etat][lettre] == 0:
            transitions_vus[etat][lettre] = 1

        else:
            return False

    return True


def determinise(auto: dict) -> dict:

    depart = frozenset(auto["I"])

    a_faire = [depart]
    faits = set([depart])

    transitions = list(auto['transitions'])

    nouvelles_transtions = []

    while len(a_faire) > 0:
        etat = a_faire.pop()

        for lettre in auto["alphabet"]:
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
        if len(auto["F"] & transition[2]) > 0:
            etats_finaux.add(transition[2])

    return {
        "alphabet": set(auto["alphabet"]),
        "etats": faits,
        "transitions": nouvelles_transtions,
        "I": [depart],
        "F": etats_finaux,
    }


def renommage(auto: dict) -> dict:
    auto_renom = {
        "alphabet": auto['alphabet'],
        "etats": [],
        "transitions": [],
        "I": set(),
        "F": set()
    }
    liste_etats = list(auto["etats"])

    auto_renom['I'].add(liste_etats.index(auto['I'][0]))

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


if __name__ == "__main__":
    # defauto()

    auto = {
        "alphabet": {"a", "b"},
        "etats": {1, 2, 3, 4},
        "transitions": [[1, "a", 2], [2, "a", 2], [2, "b", 3], [3, "a", 4]],
        "I": {1},
        "F": {4},
    }

    auto1 = {
        "alphabet": ["a", "b"],
        "etats": [0, 1],
        "transitions": [[0, "a", 0], [0, "b", 1], [1, "b", 1], [1, "a", 1]],
        "I": [0],
        "F": [1],
    }

    auto3 = {
        "alphabet": ["a", "b"],
        "etats": {
            0,
            1,
            2,
        },
        "transitions": [[0, "a", 1], [0, "a", 0], [1, "b", 2], [1, "b", 1]],
        "I": {0},
        "F": {2},
    }

    print("lirelettre:", lirelettre(auto["transitions"], auto["etats"], "a"))
    print("liremot:", liremot(auto["transitions"], auto["etats"], "aba"))
    print("accepte aba:", accepte(auto, "aba"))
    print("accepte ba:", accepte(auto, "ba"))
    print("langage accepte longueur 5: ", langage_accept(auto, 5))
    # 1.3.6 Cela n'est pas possible car un automate peut accepter une infinité de mots

    print("Complet auto:", complet(auto))
    print("Complet auto1:", complet(auto1))

    print("Complete auto:", complete(auto))

    print("Complement auto3:", complement(auto3))

    print("Suffixe auto:", suffixe(auto))
    print("Prefixe auto:", prefixe(auto))
    print("Facteur auto:", facteur(auto))
    print("Mirroir auto:", mirroir(auto))

    auto0 = {
        "alphabet": ["a", "b"],
        "etats": [0, 1, 2, 3],
        "transitions": [[0, "a", 1], [1, "a", 1], [1, "b", 2], [2, "a", 3]],
        "I": [0],
        "F": [3],
    }

    auto1 = {
        "alphabet": ["a", "b"],
        "etats": [0, 1],
        "transitions": [[0, "a", 0], [0, "b", 1], [1, "b", 1], [1, "a", 1]],
        "I": [0],
        "F": [1],
    }

    auto2 = {
        "alphabet": ["a", "b"],
        "etats": [0, 1],
        "transitions": [[0, "a", 0], [0, "a", 1], [1, "b", 1], [1, "a", 1]],
        "I": {0},
        "F": {1},
    }

    print(deterministe(auto0))
    print(deterministe(auto2))

    auto2_det = {
        'alphabet': {'a', 'b'}, 'I': [[0]],
        'transitions': [[[0], 'a', [0, 1]], [[0, 1], 'a', [0, 1]], [[0, 1], 'b', [1]], [[1], 'a', [1]], [[1], 'b', [1]]],
        'etats': [[0], [0, 1], [1]], 'F': [[0, 1], [1]]
    }

    print(renommage(determinise(auto2))) # à modifier par print(renommage(determinise(auto2_det)))
