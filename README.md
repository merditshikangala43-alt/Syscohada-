# syscohada

Une première sélection de comptes SYSCOHADA révisé sous forme de données JSON et CSV, accompagnée d'un module Python de recherche et de calcul de TVA pour la RDC.

**État du projet : version 0.1.1, en construction.** Les données recensent les neuf classes et les comptes principaux présents dans cette sélection. Il ne s'agit pas du plan comptable complet : les sous-comptes, dont `5711`, `401` et `4431`, ne figurent pas individuellement dans le jeu de données. Les libellés restent à confronter au texte officiel avant une utilisation comptable ou réglementaire.

## Données pour Excel

Le fichier [`data/plan_comptable.csv`](data/plan_comptable.csv) peut être importé dans Excel. Définissez la colonne `numero` comme **texte** afin de préserver les numéros de comptes. La même sélection est fournie en [JSON](syscohada/data/plan_comptable.json).

Chaque ligne du CSV contient `numero`, `libelle`, `nature`, `classe`, `type`. Les lignes de type `classe` décrivent les classes ; celles de type `compte` décrivent les comptes principaux.

## Python

Depuis la racine du dépôt :

```bash
python -m pip install .
```

```python
import syscohada

syscohada.classes()                 # les neuf classes
syscohada.compte("5711")           # renvoie le compte principal 57 « Caisse »
syscohada.rechercher("tresorerie")  # recherche sans tenir compte des accents
syscohada.nature("5711")            # « bilan »
syscohada.ht_vers_ttc("100", decimales=0)
syscohada.ttc_vers_ht("116", decimales=0)
```

`compte("5711")` effectue une correspondance sur les **deux premiers chiffres** et ne confirme donc ni le libellé ni l'existence du sous-compte `5711`. La recherche parcourt uniquement les comptes principaux actuellement présents.

Le module expose les régimes `normal` et `exportation` configurés dans [`tva_rdc.json`](syscohada/data/tva_rdc.json). Les taux et règles d'application dépendent des textes en vigueur à la date de l'opération : vérifiez-les avant tout usage réel. Les montants utilisent `Decimal` ; le paramètre `decimales` permet de choisir l'arrondi, par exemple `0` pour des montants entiers en CDF.

## Vérification et contribution

```bash
python -m unittest discover -s tests -v
```

Pour signaler un libellé erroné ou proposer des comptes supplémentaires, ouvrez une issue avec le numéro du compte et la référence officielle correspondante. Voir [CONTRIBUTING.md](CONTRIBUTING.md).

Feuille de route : vérification des libellés, ajout progressif des subdivisions, documentation des sources et extension des exports. Ce projet communautaire n'est pas une publication officielle de l'OHADA ou de la DGI.

Licence du code et de la compilation originale : MIT. L'utilisation des textes et des libellés issus de sources officielles reste soumise aux droits éventuellement applicables à ces sources.
