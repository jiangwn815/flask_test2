###存放蓝本的子包的构造文件，创建蓝图

from flask import Blueprint
from flask import g
from flask import current_app
import mysql.connector
import pymysql

# 由于create_app后才能使用app.route，定义路由太晚，因此用蓝本定义路由
# 蓝本中的路由是休眠状态，直到注册到程序后

# 创建蓝本
main = Blueprint('main', __name__,template_folder='../templates2')  # 1st:蓝本名字 2nd:蓝本所在的包

def before_main():
    conn = mysql.connector.connect(**current_app.config['DB_CONFIG'])
    conn2 = pymysql.connect(**current_app.config['DB_CONFIG2'])
    conn.database = current_app.config['DB_NAME']
    conn2.database = current_app.config['DB_NAME']
    g.db =  conn2

def teardown_main():
    db = getattr(g,'db',None) # g只为一个request存储信息，并且在所有方法可用，不要存在其他object为了线程环境
    if db is not None:
        db.close()

#main.before_request(before_main)
#main.teardown_request(teardown_main)
# 错误处理在main下面errors.py 视图函数在当前目录main下面views.py
# 避免循环导入依赖，放在最后导入
from . import views, errors
