class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(128))
    funcao_id = db.Column(db.String, db.ForeignKey("funcao.id"))
    sobre_mim = db.Column(db.Text())
    data_cadastro = db.Column(db.DateTime(), default=datetime.utcnow)
    confirmado = db.Column(db.Boolean, default=1)

    aluno = db.relationship('Aluno', backref='usuario', lazy=True)
    instrutor = db.relationship('Adminsitrador', backref='usuario', lazy=True)
    administrador = db.relationship('Aluno', backref='usuario', lazy=True)

class Aluno(db.Model):
    __tablename__ = "aluno"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Instrutor(db.Model):
    __tablename__ = "instrutor"

    id = db.Column(db.Integer, primary_key=True)
    instumento = db.Column(db.String, nullable=False)
    youtube_video = db.Column(db.String, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))

class Adminsitrador(db.Model):
    __tablename__ = "administrador"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


class Instrumento(db.Model):
    __tablename = "instrumento"
    id = db.Column(db.Integer, primary_key=True)
    nome_instrumento = db.Column(db.string(20))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))


db.create_all()