def pref(u: str) -> set[str]:
    """
    Prend en paramètre un mot `u` et renvoie tous les prefixes de celui-ci
    """
    prefixes: set[str] = set()

    for i in range(len(u)):
        prefixes.add(u[:i])

    return prefixes


def suf(u: str) -> set[str]:
    """
    Prend en paramètre un mot `u` et renvoie tous les suffixes de celui-ci
    """
    suffixes: set[str] = set()

    for i in range(len(u) + 1):
        suffixes.add(u[i:])

    return suffixes


def fact(u: str) -> set[str]:
    """
    Calcule les facteurs du mot passé en paramètre
    """
    facteurs: set[str] = set()

    for i in range(len(u)):
        for j in range(i, len(u) + 1):
            facteurs.add(u[i:j])

    return facteurs


def mirroir(u: str) -> str:
    """
    Calcule le mirroir du mot passé en paramètre
    """
    resultat = ""

    for lettre in u:
        resultat = lettre + resultat

    return resultat


if __name__ == "__main__":
    mot = "coucou"
    print("prefixes:", pref(mot))
    print("suffixes:", suf(mot))
    print("facteurs:", fact(mot))
    print("mirroir:", mirroir(mot))
