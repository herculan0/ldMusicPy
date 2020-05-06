import unittest
from app.models import Usuario

class UserModelTestCase(unittest.TestCase):
    def test_senha_setter(self):
        u = Usuario(senha = 'cat')
        self.assertTrue(u.senha_hash is not None)

    def test_no_senha_getter(self):
        u = Usuario(senha = 'cat')
        with self.assertRaises(AttributeError):
            u.senha

    def test_senha_salts_are_random(self):
        u = Usuario(senha = 'cat')
        u2 = Usuario(senha= 'cat')
        self.assertTrue(u.senha_hash != u2.senha_hash)
