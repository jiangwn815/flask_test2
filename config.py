import os
basedir = os.path.abspath(os.path.dirname(__file__))
#print(basedir)
class Config:
    SECRET_KEY = 'hard to see sosn'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI =  'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DATABASE = 'C:\\Users\\jiangwn815\\Documents\\DB\\gittest\\flaskr\\tmp\\flaskr.db'
    DB_CONFIG = {
        'user':'root',
        'password':'mypassword'
    }
    DB_CONFIG2 = {
        'user': 'root',
        'passwd': 'mypassword'
    }
    DB_NAME = 'flask_db'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.189.cn'
    #MAIL_PORT = '24'

config = {
'development':DevelopmentConfig,
'default':DevelopmentConfig
}