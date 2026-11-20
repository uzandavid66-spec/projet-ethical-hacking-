import unittest
from unittest.mock import MagicMock, patch

from src.c2.client_demo import envoyer_bonjour


class TestClient(unittest.TestCase):
    def test_bonjour_recoit_ok(self):
        connexion = MagicMock()
        connexion.makefile.return_value.__enter__.return_value.readline.return_value = (
            b"OK\n"
        )

        with patch("src.c2.client_demo.socket.create_connection") as ouvrir_connexion:
            ouvrir_connexion.return_value.__enter__.return_value = connexion
            reponse = envoyer_bonjour(port=5000)

        ouvrir_connexion.assert_called_once_with(("127.0.0.1", 5000), timeout=3)
        connexion.sendall.assert_called_once_with(b"Bonjour\n")
        self.assertEqual(reponse, "OK")

    def test_connexion_refusee(self):
        with patch("src.c2.client_demo.socket.create_connection", side_effect=ConnectionRefusedError):
            with self.assertRaises(ConnectionRefusedError):
                envoyer_bonjour(port=5000)


if __name__ == "__main__":
    unittest.main()