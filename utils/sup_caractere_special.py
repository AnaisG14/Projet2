def sup_caractere_special(text):
    """retourne le texte sans les caractères spéciaux : .:/\n et espaces afin de les utiliser
    comme nom de fichier"""
    caracteres_speciaux = [".", "/", ":", "\n", " ", "'", "\"", "*", "?"]
    for car in caracteres_speciaux:
        if car in text:
            text = text.replace(car, "")
    return text