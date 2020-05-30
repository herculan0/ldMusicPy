class Administrador(db.Model):
    __tablename__ = "administrador"

    id = db.Column(db.Integer, primary_key=True)
    nome_adm = db.Column(db.String(50), nullable=False)
    email_adm = db.Column(db.String(120), nullable=False, unique=True)

class Login(db.Model):
    __tablename__ = "login"

    id = db.Column(db.Integer, primary_key=True)
    email_login = db.Column(db.String(120), nullable=False, unique=True)
    senha_login = db.Column(db.String(120))

class Instrutor(db.Model):
    __tablename__ = "login"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    email_instrutor = db.Column(db.String(120), nullable=False, unique=True)
    tel_instrutor = db.Column(db.Integer, nullable=False, unique=True)

