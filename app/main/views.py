from datetime import datetime
from . import main
from flask import g
from flask import render_template
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import session
import mysql.connector

from .forms import NameForm, RegisterForm, OrderForm, LoginForm
from .. import db
from ..models import User, Role


def connect_db():
    conn = mysql.connector.connect(**current_app.config['DB_CONFIG'])
    conn.database = current_app.config['DB_NAME']
    return conn  # win下没有权限新建文件夹


@main.before_request
def before_request():
    g.db = connect_db()  # 处理请求时临时对象，每次请求会重设，用于与视图函数共享对象
    #db.create_all()
    #admin_role = Role(name='admin')

# after request发生错误不一定保证会执行所以用teardown
# response构建后就会调用这些函数
# 函数不允许修改request


@main.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)  # g只为一个request存储信息，并且在所有方法可用，不要存在其他object为了线程环境
    if db is not None:
        db.close()


#@main.route('/show_entries', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
def index():
    user_in = session.get('logged_in',None)  # 用于请求间需要存储的值
    cur = g.db.cursor()
    print('index come in')
    cur.execute('select title,text from entries natural left join users where user_name = %s order by entry_id desc',
                (user_in,))
    usr_list = User.query.all()
    #print(usr_list)


    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    cur.close()
    return render_template('show_entries.html', entries=entries, usr_list=usr_list)


@main.route('/register', methods=['GET', 'POST'])  # HEAD&OPTIONS由flask自动处理
def register():
    cur = g.db.cursor()
    form = RegisterForm()
    email = None
    password = None
    # print('register come in')
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        cur.execute('insert into users(user_name,password,salt) values (%s,%s,%s)', (email, password, 'salt'))
        user = User(email=email,username=password,created_date=datetime.utcnow())
        g.db.commit()
        db.session.add(user)
        cur.close()
        return redirect(url_for('main.index',t='12324'))
        # return redirect(url_for('www.baidu.com'))
    cur.close()
    # print('register come in2222')
    return render_template('register.html', form=form)


@main.route('/placeorder',methods=['GET', 'POST'])
def placeOrder():
    form = OrderForm()
    tod = str(datetime.now())
    tod = tod[0:4]+tod[5:7]+tod[8:10]
    print('TOD', tod)
    SERNUM = "240651"
    if request.method == 'POST' and form.validate():
        id_no = form.id_no.data
        usr_name = form.usr_name.data
        mobile_no = form.mobile_no.data
        ps_text = form.ps_text.data

        return redirect(url_for('main.index',id=id_no,un=usr_name,mn=mobile_no,pt=ps_text))
    return render_template('placeorder.html', form=form)

@main.route('/multimedia',methods=['GET', 'POST'])
def multimedia():
    return render_template('multimedia.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    cur = g.db.cursor()
    error = None
    form = LoginForm()
    if request.method == 'POST'and form.validate():
        #user_name = request.form['username']
        #password = request.form['password']
        user_name = form.name.data
        password = form.password.data

        cur.execute('SELECT user_name FROM users where user_name = %s',(user_name,))
        if not cur.fetchone():
            error="查无此用户"
        else:
            cur.execute('SELECT password,salt FROM users where user_name = %s',(user_name,))
            pw,salt = cur.fetchone()
            if pw != password:
                error = '用户名或密码错误'
            else:
                error = 'Right one!'
                session['logged_in'] = user_name
                return redirect(url_for('main.index'))

        cur.close()

    return render_template('login.html', error=error, form=form)


@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    # flash('You were logged out')
    return redirect(url_for('main.show_entries'))


@main.context_processor
def utility_processor():
    def format_price(amount, currency=u'$'):
        return u'{1}{0:.2f}'.format(amount, currency)
    return dict(format_price=format_price)



