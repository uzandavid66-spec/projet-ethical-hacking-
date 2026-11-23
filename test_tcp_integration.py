import socket
import unittest
from concurrent.futures import ThreadPoolExecutor

from src.c2.client_demo import envoyer_bonjour
from src.c2.serveur_demo import servir_client


class TestTCPIntegration(unittest.TestCase):
    def test_bonjour_recoit_ok_sur_tcp(self):
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
                reponse = envoyer_bonjour(port=port)
                traitement.result(timeout=4)

        self.assertEqual(reponse, "OK")