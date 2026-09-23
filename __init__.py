"""syscohada — Plan comptable SYSCOHADA révisé et outils TVA RDC.

Exemple :
    >>> import syscohada
    >>> syscohada.compte("521")["libelle"]
    'Banques'
"""

import json
import unicodedata
from decimal import Decimal, ROUND_HALF_UP
from importlib import resources

__version__ = "0.1.1"
__all__ = ["classes", "classe", "compte", "rechercher", "nature",
           "taux_tva", "montant_tva", "ht_vers_ttc", "ttc_vers_ht"]


def _charger(nom):
    with resources.files("syscohada.data").joinpath(nom).open(encoding="utf-8") as f:
        return json.load(f)


_PLAN = _charger("plan_comptable.json")
_TVA = _charger("tva_rdc.json")
_CLASSES = {c["numero"]: c for c in _PLAN["classes"]}
_COMPTES = {}
for _c in _PLAN["classes"]:
    for _cpt in _c["comptes"]:
        _COMPTES[_cpt["numero"]] = {**_cpt, "classe": _c["numero"], "nature": _c["nature"]}


def _normaliser(texte):
    texte = unicodedata.normalize("NFD", str(texte).lower())
    return "".join(ch for ch in texte if unicodedata.category(ch) != "Mn")


def _numero_valide(numero):
    numero = str(numero).strip()
    if not numero.isdigit():
        raise ValueError(f"Numéro de compte invalide : {numero!r}")
    return numero


# ---------- Plan comptable ----------

def classes():
    """Liste des 9 classes (numéro, libellé, nature)."""
    return [{k: c[k] for k in ("numero", "libelle", "nature")} for c in _PLAN["classes"]]


def classe(numero):
    """Retourne une classe et ses comptes. Accepte '5', 5 ou '521' (prend le 1er chiffre)."""
    numero = _numero_valide(numero)[0]
    if numero not in _CLASSES:
        raise KeyError(f"Classe inconnue : {numero}")
    return _CLASSES[numero]


def compte(numero):
    """Retourne le compte principal (2 chiffres) correspondant à un numéro.

    '521100' -> compte 52 Banques.
    """
    numero = _numero_valide(numero)
    if len(numero) < 2:
        raise ValueError("Un compte a au moins 2 chiffres ; utilisez classe() pour 1 chiffre.")
    principal = numero[:2]
    if principal not in _COMPTES:
        raise KeyError(f"Compte principal inconnu : {principal}")
    return {**_COMPTES[principal], "numero_saisi": numero}


def rechercher(texte):
    """Recherche par mot-clé dans les libellés (insensible aux accents et à la casse)."""
    cible = _normaliser(texte)
    return [c for c in _COMPTES.values() if cible in _normaliser(c["libelle"])]


def nature(numero):
    """'bilan', 'gestion' ou 'hors_bilan_analytique'."""
    return classe(numero)["nature"]


# ---------- TVA RDC ----------

def _dec(x):
    return Decimal(str(x))


def _arrondi(x, decimales):
    return x.quantize(Decimal(1).scaleb(-decimales), rounding=ROUND_HALF_UP)


def taux_tva(regime="normal"):
    """Retourne le taux TVA RDC configuré pour le régime demandé.

    Les régimes exposés par cette version sont ``normal`` (16 %) et
    ``exportation`` (0 %). Les régimes particuliers ne sont pas généralisés
    sans vérification du texte fiscal applicable.
    """
    if regime not in _TVA["taux"]:
        raise KeyError(f"Régime inconnu : {regime}. Choix : {list(_TVA['taux'])}")
    return _dec(_TVA["taux"][regime])


def montant_tva(montant_ht, regime="normal", decimales=2):
    return _arrondi(_dec(montant_ht) * taux_tva(regime), decimales)


def ht_vers_ttc(montant_ht, regime="normal", decimales=2):
    return _arrondi(_dec(montant_ht) * (1 + taux_tva(regime)), decimales)


def ttc_vers_ht(montant_ttc, regime="normal", decimales=2):
    return _arrondi(_dec(montant_ttc) / (1 + taux_tva(regime)), decimales)
