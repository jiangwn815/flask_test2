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
    return True


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
    print("get_area func in")
    area_info = {
        'dc': ['二环内103'],
        'xc': ["二环内103", "二环到三环间104", "三环外113"],
        'cy': ["二环到三环间104", "三环到四环间111", "四环到五环间114", "五环到六环间115"],
        'ft': ["二环到三环间104", "三环到四环间111", "四环到五环间114", "六环外116"],
        'sjs': ["八大处100", "苹果园109", "古城105"],
        'hd': ["三环内112", "三环到四环间111", "四环到五环间114", "五环到六环间115"],
        'mtg': ["城区101"],
        'fs': ["良乡117", "城关118", "长阳119"],
        'tz': ["马驹桥镇106", "次渠镇102"],
        'sy': ["马坡地区107", "仁和地区110"],
        'cp': ["城区101", "天通苑124", "回龙观123"],
        'dx': ["四环到五环间114", "五环到六环间115", "亦庄开发区122"],
        'hr': ["城区101"],
        'pg': ["城区101"],
        'my': ["城区101"],
        'yq': ["城区101"]
    }
    store_info = {
        'cp101': ['昌崔路营业厅200', '鼓楼北街营业厅201'],
        'cp123': ['回龙观营业厅202'],
        'cp124': ['天通苑营业厅203', '天通中苑营业厅204'],
        'cy104': ['东大桥营业厅205', '富力城营业厅206', '静安营业厅207', '永安里营业厅208'],
        'cy111': ['大北窑营业厅209', '平乐园营业厅210', '三元桥营业厅211'],
        'cy114': [' 财满接嘉园营业厅212', '朝阳北路营业厅213', '大郊亭营业厅214', '大山子营业厅215', '东八里庄营业厅216', '酒仙桥营业厅217',
                  '望京桥营业厅218', '望京营业厅219', '亚运村营业厅220'],
        'cy115': ['常营营业厅221', '东坝营业厅222', '杨闸营业厅223'],
        'dc103': ['朝阳门营业厅224', '广渠门营业厅225', '小街桥营业厅226'],
        'dx114': ['狼垡营业厅227', '西红门营业厅228'],
        'dx115': ['黄村营业厅229'],
        'dx122': ['经济技术开发区营业厅230'],
        'fs117': ['良乡营业厅231', '西潞营业厅232'],
        'fs118': ['城关营业厅233'],
        'fs119': ['长阳营业厅234'],
        'ft104': ['方庄营业厅235', '木樨园桥营业厅236'],
        'ft111': ['成寿寺营业厅237', '光彩营业厅238', '宋家庄营业厅239', '洋桥营业厅240'],
        'ft114': ['大成路营业厅241', '东高地营业厅242', '丰台南路营业厅243', '科丰桥营业厅244'],
        'ft116': ['杜家坎营业厅245'],
        'hd111': ['牡丹园营业厅246', '四通桥营业厅247', '长春桥营业厅248', '中关村南路营业厅249'],
        'hd112': ['公主坟营业厅250', '航天桥营业厅251', '莲花桥营业厅252'],
        'hd114': ['田村营业厅253', '五道口营业厅254', '杏石口营业厅255', '中关村大街营业厅256'],
        'hd115': ['安河桥北营业厅257', '清河营业厅258', '上地西路营业厅259'],
        'hr101': ['怀柔营业厅260'],
        'mtg101': ['滨河路营业厅261'],
        'my101': ['密云县营业厅262'],
        'pg101': ['平谷府前西街营业厅263'],
        'sjs100': ['八大处营业厅264'],
        'sjs105': ['古城营业厅265'],
        'sjs109': ['杨庄营业厅266'],
        'sy107': ['马坡营业厅267'],
        'sy110': ['石园营业厅268'],
        'tz102': ['台湖营业厅269'],
        'tz106': ['九棵树营业厅270', '新华大街营业厅271'],
        'xc104': ['德胜营业厅272', '官园营业厅273', '马连道营业厅274', '三里河营业厅275'],
        'xc103': ['虎坊路营业厅276', '西单营业厅277', '新街口营业厅278'],
        'xc113': ['马甸营业厅279'],
        'yq101': ['妫水北街营业厅280']

    }

    pv = request.args.get('pval', "null", type=str)
    sv = request.args.get('sval', "null", type=str)
    print("pv:"+str(pv))
    print("sv:" + str(sv))
    print(request.args)
    #默认设定mimetype='application/json'
    #json.dump()不设定mimetype,需要手动设定
    return jsonify({
            "di": area_info.get(pv),
            "si": store_info.get(sv)
            #"str":c
    })
