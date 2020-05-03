import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or ('ldmusic')
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or ('smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or ('587'))
#    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', true).lower() in ['true', 'on', 1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    LDM_EMAIL_SUBJECT_PREFIX =  '[ldMusic]'
    LDM_MAIL_SENDER = 'Administrador ldMusic <ldmusic00@gmail.com>'
    LDM_ADMIN = os.environ.get('LDM_ADMIN')
#    SQLALCHEMY_TRACK_MODIFICATIONS = FALSE

class  DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or ('mysql+pymysql://admin:ldmusic@db:3306/ldMusic?charset=utf8mb4')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or ('mysql+pymysql://admin:ldmusic@db:3306/ldMusic?charset=utf8mb4')

#class ProductionConfig(config):
#   SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing' : TestingConfig,

    'default': DevelopmentConfig
}

