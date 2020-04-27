from wezeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    senha_hash = db.column(db.String(128))

    @property
    def senha(self):
        raise AttributeError('senha não é um atributo que se possa ler')

    @password.setter
    def senha(self, senha):
        self.senha_hash = generate_senha_hash(senha)

    def verifica_senha(self, senha):
        return check_senha_hash(self.senha_hash, senha)
