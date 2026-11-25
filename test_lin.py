import io
import socket
import subprocess
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from src.c2.serveur_demo import servir_client
from src.lin import client_local, diagnostic_ipv4, lecture_fictive


class TestClientLocal(unittest.TestCase):
    def test_echange_reel(self):
        with socket.socket() as serveur:
            serveur.bind(("127.0.0.1", 0))
            serveur.listen(1)
            serveur.settimeout(3)
            port = serveur.getsockname()[1]

            def traiter_connexion():
                connexion, _ = serveur.accept()
                with connexion:
                    connexion.settimeout(3)
                    servir_client(connexion)

            with ThreadPoolExecutor(max_workers=1) as executor:
                traitement = executor.submit(traiter_connexion)
                with redirect_stdout(io.StringIO()) as sortie:
                    self.assertEqual(client_local.main(["--port", str(port)]), 0)
                traitement.result(timeout=4)

        self.assertEqual(sortie.getvalue().strip(), "OK")

    def test_serveur_arrete(self):
        with socket.socket() as serveur:
            # Réserver un port libre sans démarrer d'écoute.
            serveur.bind(("127.0.0.1", 0))
            port = serveur.getsockname()[1]
            with redirect_stderr(io.StringIO()) as sortie:
                self.assertEqual(client_local.main(["--port", str(port)]), 1)
        self.assertIn(f"Connexion refusée sur 127.0.0.1:{port}", sortie.getvalue())

    def test_port_invalide(self):
        with redirect_stderr(io.StringIO()) as sortie, self.assertRaises(SystemExit) as erreur:
            client_local.main(["--port", "0"])
        self.assertEqual(erreur.exception.code, 2)
        self.assertIn("entre 1 et 65535", sortie.getvalue())

    def test_erreurs_echange(self):
        for erreur, message in [
            (TimeoutError(), "Délai dépassé"),
            (OSError("test"), "Échange impossible"),
            (UnicodeDecodeError("utf-8", b"\xff", 0, 1, "test"), "non valide en UTF-8"),
        ]:
            with self.subTest(erreur=erreur):
                with patch.object(client_local, "envoyer_bonjour", side_effect=erreur):
                    with redirect_stderr(io.StringIO()) as sortie:
                        self.assertEqual(client_local.main([]), 1)
                self.assertIn(message, sortie.getvalue())

    def test_reponse_inattendue(self):
        with patch.object(client_local, "envoyer_bonjour", return_value=""):
            with redirect_stderr(io.StringIO()) as sortie:
                self.assertEqual(client_local.main([]), 1)
        self.assertIn("Réponse inattendue", sortie.getvalue())


class TestDiagnosticIPv4(unittest.TestCase):
    def test_filtre_boucle_locale(self):
        resultat = subprocess.CompletedProcess(
            args=[], returncode=0, stdout="""[
                {"ifname":"lo","flags":["LOOPBACK"],"addr_info":[{"local":"192.0.2.2"}]},
                {"ifname":"eth0","addr_info":[{"local":"127.10.0.1"},{"local":"192.0.2.3"}]}
            ]"""
        )
        with patch.object(diagnostic_ipv4.subprocess, "run", return_value=resultat):
            with redirect_stdout(io.StringIO()) as sortie:
                self.assertEqual(diagnostic_ipv4.main(), 0)
        self.assertEqual(sortie.getvalue().strip(), "eth0 : 192.0.2.3")

    def test_commande_indisponible(self):
        with patch.object(diagnostic_ipv4.subprocess, "run", side_effect=FileNotFoundError("ip")):
            with redirect_stderr(io.StringIO()) as sortie:
                self.assertEqual(diagnostic_ipv4.main(), 1)
        self.assertIn("Diagnostic IPv4 impossible", sortie.getvalue())


class TestLectureFictive(unittest.TestCase):
    def test_lecture_et_parcours(self):
        contenu, fichiers = lecture_fictive.lire_et_lister()
        self.assertIn("Bonjour", contenu)
        self.assertEqual(fichiers, [Path("bonjour.txt"), Path("exemples/note.txt")])

    def test_fichier_absent(self):
        with tempfile.TemporaryDirectory() as dossier:
            with patch.object(lecture_fictive, "DONNEES", Path(dossier)):
                with redirect_stderr(io.StringIO()) as sortie:
                    self.assertEqual(lecture_fictive.main(), 1)
        self.assertIn("bonjour.txt doit être un fichier ordinaire", sortie.getvalue())

    def test_liens_symboliques_ignores(self):
        with tempfile.TemporaryDirectory() as dossier:
            racine = Path(dossier)
            donnees = racine / "donnees"
            donnees.mkdir()
            (donnees / "bonjour.txt").write_text("Fictif", encoding="utf-8")
            (donnees / "lien_dossier").symlink_to(racine, target_is_directory=True)
            (donnees / "lien_fichier").symlink_to(donnees / "bonjour.txt")
            with patch.object(lecture_fictive, "DONNEES", donnees):
                self.assertEqual(lecture_fictive.lire_et_lister(), ("Fictif", [Path("bonjour.txt")]))
