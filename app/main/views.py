from datetime import datetime
from . import main
from flask import g
from flask import render_template
from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import abort
from flask import jsonify
#import mysql.connector
import pymysql

from .forms import NameForm, RegisterForm, OrderForm, LoginForm
from .. import db
from ..models import User, Role


def connect_db():
    #conn = mysql.connector.connect(**current_app.config['DB_CONFIG'])
    conn2 = pymysql.connect(**current_app.config['DB_CONFIG2'])
    #conn.database = current_app.config['DB_NAME']
    #conn2.database = current_app.config['DB_NAME']
    return conn2  # win下没有权限新建文件夹


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
    dbase = getattr(g, 'db', None)  # g只为一个request存储信息，并且在所有方法可用，不要存在其他object为了线程环境
    if dbase is not None:
        dbase.close()


#@main.route('/show_entries', methods=['GET', 'POST'])
@main.route('/', methods=['GET', 'POST'])
def index():
    user_in = session.get('logged_in',None)  # 用于请求间需要存储的值
    cur = g.db.cursor()
    print('index come in')
    cur.execute('select title,text from entries natural left join users where user_name = %s order by entry_id desc',(user_in,))
    usr_list = User.query.all()
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    cur.close()
    return render_template('show_entries.html', entries=entries, usr_list=usr_list)


@main.route('/add', methods=['GET', 'POST'])
def add_entry():
    user_in = session.get('logged_in')
    if not user_in:
        abort(401)
    if request.method == 'POST':
        cur = g.db.cursor()
        cur.execute('select user_id from users where user_name = %s',(session.get('logged_in'),))
        user_id = cur.fetchone()#返回tuple
        cur.execute('insert into entries (user_id,title,text) values (%s,%s,%s)',
                    (user_id[0], request.form['title'],request.form['text']))
        g.db.commit()
        return redirect(url_for('show_entries'))
    return render_template('add_entry.html')


@main.route("/userlist", methods=['GET'])
def user_list():
    cur = g.db.cursor()
    cur.execute('select user_name from users')
    user_list_mysql = cur.fetchall()
    user_list_sqlite = User.query.all()
    return render_template('user_list.html', mysql_user=user_list_mysql, sqlite_user=user_list_sqlite)


@main.route("/installment", methods=['GET'])
def installment():

    return render_template('installment.html')


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
    return redirect(url_for('main.index'))


@main.context_processor
def utility_processor():
    def format_price(amount, currency=u'$'):
        return u'{1}{0:.2f}'.format(amount, currency)
    return dict(format_price=format_price)


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

@main.route('/showorder',methods=['GET', 'POST'])
def showOrder():
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

@main.route('/dataprocess',methods=['GET'])
def dataprocess():
    return ;

@main.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)

    print(request.args)
    return jsonify(
    {
            "result": a + b,
            "di": ["东城区", "西城区", "海淀区", "香河"]
    })

@main.route('/get_area')
def get_area():
    print("get_area func in");
    area_info={
        'dc': ['二环内'],
        'xc': ["内环到二环里", "二环外到三环"],
        'cy': ["三环以内", "三环到四环间", "四环五环间","五环六环间"],
        'ft': ["朝二环内", "三环内", "四环五环内"],
        'sjs': ["朝二环内", "三环内", "四环五环内"],
        'hd': ["朝二环内", "三环内", "四环五环内"],
        'mtg': ["朝二环内", "三环内", "四环五环内"],
        'fs': ["朝二环内", "三环内", "四环五环内"],
        'tz': ["六环内", "六环外"],
        'sy': ["马坡", "后沙峪"],
        'cp': ["城区", "六环内", "城区外"],
        'dx': ["四环五环间", "五环六环间", "六环以外","亦庄开发区"],
        'hr': ["城区"],
        'pg': ["城区"],
        'my': ["城区"],
        'yq': ["城区"]
    }
    pv = request.args.get('pval', "null", type=str)
    print("pv:"+str(pv))
    print(request.args)
    #默认设定mimetype='application/json'
    #json.dump()不设定mimetype,需要手动设定
    return jsonify(
    {
            "di": area_info.get(pv)
            #"str":c
    })
