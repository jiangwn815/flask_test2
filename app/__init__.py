from flask import Flask
# from flask.ext.bootstrap import Bootstrap
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from datetime import datetime
'''
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
'''
from config import config

# 延迟创建程序实例，把创建过程移到可显式调用的工厂函数中。
# 这种方法不仅可以给脚本留出配置程序的时间，还能够创建多个程序实例，
# 构造文件导入了大多数正在使用的Flask扩展。由于尚未初始化所需的程序实例，所以没有初始化扩展，创建扩展类时没有向构造函数传入参数。


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
'''
mail = Mail()
moment = Moment()

pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
'''


# 过滤器1
def format_price2(amount, currency=u'€'):
    return u'{1}{0:.2f}'.format(amount, currency)


# 过滤器2
def date22(date_value):
        return datetime.strftime(date_value, '%Y-%m-%d %H:%M:%S')


def create_app(config_name):
    # 创建程序实例
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.jinja_env.filters['format_price2'] = format_price2 # 注册过滤器
    app.jinja_env.filters['date_filter'] = date22 # 注册过滤器


    config[config_name].init_app(app)
    # 初始化扩展
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    '''
    mail.init_app(app)


    login_manager.init_app(app)
    pagedown.init_app(app)

    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        sslify = SSLify(app)
    '''
    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)  # 注册前蓝图中的路由处于休眠，注册后才成为程序的一部分
    '''
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    '''
    return app
