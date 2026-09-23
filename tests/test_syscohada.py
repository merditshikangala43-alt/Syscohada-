import unittest
from decimal import Decimal

import syscohada


class SyscohadaTests(unittest.TestCase):
    def test_neuf_classes(self):
        self.assertEqual([c["numero"] for c in syscohada.classes()], list("123456789"))

    def test_compte_principal_et_numero_saisi(self):
        resultat = syscohada.compte("5711")
        self.assertEqual((resultat["numero"], resultat["numero_saisi"]), ("57", "5711"))

    def test_recherche_sans_accents(self):
        self.assertTrue(any(c["numero"] == "52" for c in syscohada.rechercher("banques")))
        self.assertTrue(any(c["numero"] == "58" for c in syscohada.rechercher("accreditifs")))

    def test_nature(self):
        self.assertEqual(syscohada.nature("5711"), "bilan")

    def test_numero_invalide(self):
        with self.assertRaises(ValueError):
            syscohada.compte("57A1")

    def test_tva_arrondi_cdf(self):
        ht = Decimal("101")
        tva = syscohada.montant_tva(ht, decimales=0)
        ttc = syscohada.ht_vers_ttc(ht, decimales=0)
        self.assertEqual(ht + tva, ttc)

    def test_retour_ttc_vers_ht(self):
        self.assertEqual(syscohada.ttc_vers_ht("116", decimales=0), Decimal("100"))


if __name__ == "__main__":
    unittest.main()
