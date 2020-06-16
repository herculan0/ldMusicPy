from flask_table import Table, Col


class Resultados(Table):
    id = Col('ID')
    nome = Col('Nome')
    instrumento = Col('Instrumento')
    cidade = Col('Cidade')