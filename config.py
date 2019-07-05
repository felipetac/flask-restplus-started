import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config(object):

    # Statement for enabling the development environment
    DEBUG = False

    TESTING = False

    # Define the database - we are working with
    # SQLite for this example
    #SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = False

    # Use a secure, unique and absolutely secret key for
    # signing the data.
    #CSRF_SESSION_KEY = "secret"

    # JWT Secret key
    SECRET_KEY = "25ef26bae776093bb5ff6ff9aa3a27dcc83d3b5c188d624d"

    # JWT Algorithm
    JWT_ALGORITHM = 'HS512'

    # Definição da linguagem padrão
    BABEL_DEFAULT_LOCALE = 'pt'

    # Tipo de Algoritmo para encriptação da senha
    PASSWORD_SCHEMES = ['pbkdf2_sha512']

    # Quantidade de itens na paginação
    PER_PAGE = 10

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'app.db')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' # in-memory database

class ProductionConfig(Config):
    POSTGRES_URL = os.environ.get("POSTGRES_URL")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PW = os.environ.get("POSTGRES_PW")
    POSTGRES_DB = os.environ.get("POSTGRES_DB")

    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' + \
        '{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                        pw=POSTGRES_PW,
                                        url=POSTGRES_URL,
                                        db=POSTGRES_DB)

CONFIG = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
