def defauto_alphabet(defaut="ab") -> set:
    """
    Demande de saisir l'alphabet d'un automate
    """
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
    """
    Demande de saisir les différents états d'un automate
    """
    etats = set()

    print("Veuilliez saisir les états de votre automate, 'fin' pour stopper la saisie")

    texte = ""
    while texte != "fin":
        n = None
        # Boucle tant que la valeur entrée n'est pas un nombre
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
    """
    Demande de séléctionner des états d'un automate pour une raison {type}
    """
    print(
        f"Veuilliez saisir les états {type} de votre automate, 'fin' pour stopper la saisie"
    )
    selection = set()

    texte = ""
    while texte != "fin":
        n = None
        # Boucle tant que la valeur entrée n'est pas un nombre
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
    """
    Demande de saisir les transitions pour l'état {etat}
    """
    print(f"Saisissez les transitions pour l'état {etat}")

    transitions = []

    while True:
        lettre = ""
        sortie = ""
        print(f"Saisissez la lettre de la transition parmis {', '.join(alphabet)}")
        # Boucle tant que la valeur entrée n'est pas dans l'alphabet
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
    """
    Demande de saisir les transitions d'un automate (pour tous les états)
    """
    transitions = []
    while True:
        print(
            f'Choisissez un état parmis {', '.join(map(str, etats))} ou \'fin\' pour stopper la saisie'
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
    """
    Demande de saisir un automate et le renvoie
    """
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
    """
    Lis un mot à partir des transitions
    """
    etats_suivants = set(etats)

    for lettre in mot:
        etats_suivants = lirelettre(transitions, etats_suivants, lettre)
        if len(etats_suivants) == 0:
            return etats_suivants

    return etats_suivants


def accepte(auto: dict, mot: str) -> bool:
    """
    Renvoie True si l'automate accepte le mot
    """
    return len(liremot(auto["transitions"], auto["I"], mot) & auto["F"]) > 0


def deterministe(auto: dict) -> bool:
    """
    Renvoie vrai si l'automate passé en paramètre est deterministe
    """
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
    """
    Determinise l'automate passé en paramètre
    """
    depart = frozenset(auto["I"])

    a_faire = [depart]
    faits = set([depart])

    transitions = list(auto["transitions"])

    nouvelles_transtions = []

    # Parcours tous les états non marqués
    while len(a_faire) > 0:
        etat = a_faire.pop()

        # Cherche les transitions de l'état et créer un nouvel état
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

    # Calcule les étas finaux
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
    """
    Renomme les états de l'automate passé en paramètre
    """
    auto_renom = {
        "alphabet": auto["alphabet"],
        "etats": [],
        "transitions": [],
        "I": set(),
        "F": set(),
    }
    liste_etats = list(auto["etats"])

    for etat_initial in auto["I"]:
        auto_renom["I"].add(liste_etats.index(etat_initial))

    for etat_final in auto["F"]:
        auto_renom["F"].add(liste_etats.index(etat_final))

    for i in range(len(liste_etats)):
        auto_renom["etats"].append(i)

    for transition in auto["transitions"]:
        etat_i, etat_f = liste_etats.index(transition[0]), liste_etats.index(
            transition[2]
        )
        transition_renom = [
            auto_renom["etats"][etat_i],
            transition[1],
            auto_renom["etats"][etat_f],
        ]

        auto_renom["transitions"].append(transition_renom)

    auto_renom["etats"] = set(auto_renom["etats"])

    return auto_renom


def inter(auto1: dict, auto2: dict) -> dict:
    """
    Réalise l'intersection des automates auto1 et auto2
    """
    if not deterministe(auto1):
        auto1 = renommage(determinise(auto1))

    if not deterministe(auto2):
        auto2 = renommage(determinise(auto2))

    transitions = []
    initiaux = set()
    finaux = set()

    # Caclule les états initiaux
    for i1 in auto1["I"]:
        for i2 in auto2["I"]:
            initiaux.add((i1, i2))

    sorties = set(initiaux)

    # Calcules les états pouvant être parcourus dans l'automate produits
    ajout = True
    while ajout:
        ajout = False
        for transition_a in auto1["transitions"]:
            for transition_b in auto2["transitions"]:
                if transition_a[1] == transition_b[1]:
                    if (transition_a[0], transition_b[0]) not in sorties:
                        continue
                    sortie = (transition_a[2], transition_b[2])
                    ajout = sortie not in sorties
                    sorties.add((transition_a[2], transition_b[2]))

    # Parcours les transitions
    for transition_a in auto1["transitions"]:
        for transition_b in auto2["transitions"]:
            if transition_a[1] == transition_b[1]:
                entree = (transition_a[0], transition_b[0])

                # Vérifie que l'état est accessible
                if entree in sorties:
                    transitions.append(
                        [entree, transition_a[1], (transition_a[2], transition_b[2])]
                    )

    # Parcours les états finaux
    for f1 in auto1["F"]:
        for f2 in auto2["F"]:
            finaux.add((f1, f2))

    auto_inter = {
        "alphabet": auto1["alphabet"] & auto2["alphabet"],
        "etats": set(),
        "transitions": transitions,
        "I": initiaux,
        "F": finaux,
    }

    # Complète l'ensemble des états de l'automate
    ajoute_etats(auto_inter)

    return auto_inter


def ajoute_etats(auto: dict) -> dict:
    """
    Prend en paramètre un automate avec des transitions et rajoute ses etats manquants
    """
    for transition in auto["transitions"]:
        auto["etats"].add(transition[0])
        auto["etats"].add(transition[2])


def difference(auto1: dict, auto2: dict) -> dict:
    """
    Réalise la différence des automates auto1 et auto2
    """
    if not complet(auto1):
        auto1 = complete(auto1)
    if not complet(auto2):
        auto2 = complete(auto2)

    auto_difference = inter(auto1, auto2)

    liste_etats_finaux = list(auto_difference["F"])
    i = 0
    fin = len(liste_etats_finaux)

    while i < fin:
        etat_final = liste_etats_finaux[i]

        if etat_final[1] in auto2["F"]:
            auto_difference["F"].remove(etat_final)

        i += 1

    for transition in auto_difference["transitions"]:
        if transition[0][0] in auto1["F"] and transition[0][1] not in auto2["F"]:
            auto_difference["F"].add(transition[0])
        elif transition[2][0] in auto1["F"] and transition[2][1] not in auto2["F"]:
            auto_difference["F"].add(transition[2])

    return auto_difference


def langage_accept(automate: dict, n: int) -> set:
    """
    Renvoie tous les mots de longueur <= n accepté par l'automate passé en paramètre
    """
    initial = {}

    # Construit le dictionnaire contenant les lettres en fonction des états
    for etat in automate["I"]:
        for transition in automate["transitions"]:
            if transition[0] == etat:
                if transition[2] not in initial:
                    initial[transition[2]] = []
                initial[transition[2]].append(transition[1])

    return langage_accept_rec(automate, initial, set(), n - 1)


def langage_accept_rec(automate: dict, positions: dict, resultat_mots: set, n: int):
    """
    ATTENTION: Merci d'utiliser la fonction langage_accept

    Recursive
    Renvoie tous les mots de longueur <= n accepté par l'automate passé en paramètre
    """
    if n <= 0:
        return resultat_mots

    nouvelle_positions = {}

    # Construit le dictionnaire nouvelle_positions
    # de manière nouvelles_positions[transition] = positions[transition] * lettres_acceptés
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
    """
    Liste toutes les transitions manquantes de l'automate pour qu'il soit considiré complet
    """
    manquants = {}

    # Construit le dictionnaire avec tous les états en clef et l'ensemble de l'alphabet en valeur
    for etat in auto["etats"]:
        manquants[etat] = set()
        for lettre in auto["alphabet"]:
            manquants[etat].add(lettre)

    # Supprime les lettres acceptés par chaque état
    for etat, lettres in manquants.items():
        for transition in auto["transitions"]:
            for lettre in set(lettres):
                if transition[0] == etat and transition[1] == lettre:
                    lettres.remove(lettre)

    return manquants


def complet(auto: dict) -> bool:
    """
    Renvoie vrais si l'automate passé en paramètre est complet
    """
    for lettres in liste_transitions_manquantes(auto).values():
        if len(lettres) != 0:
            return False

    return True


def complete(auto: dict) -> dict:
    """
    Complete l'automate pour qu'il soit complet
    """
    manquants = liste_transitions_manquantes(auto)

    auto_modif = dict(auto)

    puis = max(auto_modif["etats"]) + 1
    auto_modif["etats"].add(puis)

    # Ajoute les transitions manquantes
    for etat, lettres in manquants.items():
        for lettre in lettres:
            auto_modif["transitions"].append([etat, lettre, puis])

    return auto_modif


def complement(auto: dict) -> dict:
    """
    Réalise l'inverse de l'automate
    """
    auto_complet = complete(auto)

    # Inverse les états finaux
    for etat in auto_complet["etats"]:
        if etat in auto_complet["F"]:
            auto_complet["F"].remove(etat)
        else:
            auto_complet["F"].add(etat)
    return auto_complet


def prefixe(auto: dict) -> dict:
    """
    Renvoie l'automate qui accepte tous les préfixes de celui passé en paramètre
    """
    auto_prefixe = dict(auto)

    auto_prefixe["F"] = set(auto_prefixe["etats"])

    return auto_prefixe


def suffixe(auto: dict) -> dict:
    """
    Renvoie l'automate qui accepte tous les suffixes de celui passé en paramètre
    """
    auto_suffixe = dict(auto)

    auto_suffixe["I"] = set(auto_suffixe["etats"])

    return auto_suffixe


def facteur(auto: dict) -> dict:
    """
    Renvoie l'automate qui accepte tous les facteurs de celui passé en paramètre
    """
    return suffixe(prefixe(auto))


def mirroir(auto: dict) -> dict:
    """
    Renvoie l'automate qui accepte tous les mots mirroirs de celui passé en paramètre
    """
    auto_mirroir = dict(auto)

    # Inverse les états initiaux et finaux
    auto_mirroir["I"], auto_mirroir["F"] = auto_mirroir["F"], auto_mirroir["I"]

    # Inverse le sens des transitions
    for transiton in auto_mirroir["transitions"]:
        transiton[0], transiton[2] = transiton[2], transiton[0]

    return auto_mirroir


def position_classe(classes: dict, etat: int):
    """
    Renvoie la position de l'etat dans les classes d'équivalences
    """
    for key, etats in classes.items():
        if etat in etats:
            return key


def equivalence(auto: dict) -> list:
    """
    Calcules les classe d'équivalences de l'automate passé en paramètre
    """
    classes = {"AUTRES": auto["etats"] - auto["F"], "FINAUX": auto["F"]}
    taille = 0

    # Boucle tant que la classe change
    while taille != len(classes):
        taille = len(classes)
        storage = {}

        # Calcule la liste des équivalence par etat et par lettre
        for lettre in auto["alphabet"]:
            for transition in auto["transitions"]:
                if transition[1] == lettre:
                    if transition[0] not in storage:
                        storage[transition[0]] = [
                            position_classe(classes, transition[0])
                        ]
                    position = position_classe(classes, transition[2])
                    storage[transition[0]].append((lettre, position))

        classes = {}
        # Construit le dictionnaire des classes d'équivalence
        for etat, equivalence in storage.items():
            if tuple(equivalence) not in classes:
                classes[tuple(equivalence)] = []
            classes[tuple(equivalence)].append(etat)
    resultat = []
    for classe in classes.values():
        resultat.append(tuple(classe))

    return resultat


def vers_classe(etat: int, classes: list) -> tuple:
    """
    Convertis l'état dans sa classe d'équivalence
    """
    for classe in classes:
        if etat in classe:
            return classe


def minimise(auto: dict):
    """
    Minimise l'automate passé en paramètre
    """
    classes_equivalences = equivalence(auto)

    initiaux = set()
    finaux = set()

    for initial in auto["I"]:
        initiaux.add(vers_classe(initial, classes_equivalences))

    for final in auto["F"]:
        finaux.add(vers_classe(final, classes_equivalences))

    transitions = []

    for transition in auto["transitions"]:
        nouvelle_transition = [
            vers_classe(transition[0], classes_equivalences),
            transition[1],
            vers_classe(transition[2], classes_equivalences),
        ]

        if nouvelle_transition not in transitions:
            transitions.append(nouvelle_transition)

    return {
        "alphabet": set(auto["alphabet"]),
        "etats": set(classes_equivalences),
        "I": initiaux,
        "F": finaux,
        "transitions": transitions,
    }


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
        "alphabet": {"a", "b"},
        "etats": {0, 1},
        "transitions": [[0, "a", 0], [0, "b", 1], [1, "b", 1], [1, "a", 1]],
        "I": {0},
        "F": {1},
    }

    auto3 = {
        "alphabet": {"a", "b"},
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
        "alphabet": {"a", "b"},
        "etats": {0, 1, 2, 3},
        "transitions": [[0, "a", 1], [1, "a", 1], [1, "b", 2], [2, "a", 3]],
        "I": {0},
        "F": {3},
    }

    auto1 = {
        "alphabet": {"a", "b"},
        "etats": {0, 1},
        "transitions": [[0, "a", 0], [0, "b", 1], [1, "b", 1], [1, "a", 1]],
        "I": {0},
        "F": {1},
    }

    auto2 = {
        "alphabet": {"a", "b"},
        "etats": {0, 1},
        "transitions": [[0, "a", 0], [0, "a", 1], [1, "b", 1], [1, "a", 1]],
        "I": {0, 1},
        "F": {1},
    }

    print(deterministe(auto0))
    print(deterministe(auto2))

    print(renommage(determinise(auto2)))

    auto4 = {
        "alphabet": {"a", "b"},
        "etats": {
            0,
            1,
            2,
        },
        "transitions": [[0, "a", 1], [1, "b", 2], [2, "b", 2], [2, "a", 2]],
        "I": {0},
        "F": {2},
    }

    auto5 = {
        "alphabet": {"a", "b"},
        "etats": {0, 1, 2},
        "transitions": [
            [0, "a", 0],
            [0, "b", 1],
            [1, "a", 1],
            [1, "b", 2],
            [2, "a", 2],
            [2, "b", 0],
        ],
        "I": {0},
        "F": {0, 1},
    }

    auto6 = {
        "alphabet": {"a", "b"},
        "etats": {0, 1, 2, 3, 4, 5},
        "transitions": [
            [0, "a", 4],
            [0, "b", 3],
            [1, "a", 5],
            [1, "b", 5],
            [2, "a", 5],
            [2, "b", 2],
            [3, "a", 1],
            [3, "b", 0],
            [4, "a", 1],
            [4, "b", 2],
            [5, "a", 2],
            [5, "b", 5],
        ],
        "I": {0},
        "F": {0, 1, 2, 5},
    }

    print("\nIntersection :")
    print((inter(auto4, auto5)))

    print("\nDifférence")
    print(difference(auto4, auto5))

    print("Minimisation:")
    print(minimise(auto6))
    print(renommage(minimise(auto6)))
