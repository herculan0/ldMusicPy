from app import db

class Administrador(db.Model):
    __tablename__ = "administrador"

    id = db.Column(db.Integer, primary_key=True)
    nome_adm = db.Column(db.String(50), nullable=False)
    email_adm = db.Column(db.String(120), nullable=False, unique=True)
    
    login_id = db.Column(db.Integer, db.ForeignKey('login.id'))
    login = db.relationship('Login', backref='administrador', lazy=True)

class Login(db.Model):
    __tablename__ = "login"

    id = db.Column(db.Integer, primary_key=True)
    email_login = db.Column(db.String(120), nullable=False, unique=True)
    senha_login = db.Column(db.String(120))

class Instrutor(db.Model):
    __tablename__ = "instrutor"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    email_instrutor = db.Column(db.String(120), nullable=False, unique=True)
    tel_instrutor = db.Column(db.Integer, nullable=False, unique=True)

    login_id = db.Column(db.Integer, db.ForeignKey('login.id'))
    login = db.relationship('Login', backref='instrutor', lazy=True)

class Aluno(db.Model):
    __tablename__ = "aluno"

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    email_aluno = db.Column(db.String(120), nullable=False, unique=True)
    tel_aluno = db.Column(db.Integer, nullable=False, unique=True)

    login_id = db.Column(db.Integer, db.ForeignKey('login.id'))
    login = db.relationship('Login', backref='aluno', lazy=True)

class Instrumento(db.Model):
    __tablename = "instrumento"
    id = db.Column(db.Integer, primary_key=True)
    nome_instrumento = db.Column(db.string(20))

class Aluno_instrumento(db.Model):
    __tablename__ = "aluno_instrumento"

class Instrutor_instrumento(db.Model):
    __tablename__ = "instrutor_instrumento"

class Localizacao(db.Model):
    __tablename__ "localizacao"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)