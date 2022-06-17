import flask, json, bcrypt, sqlite3, datetime, smtplib, ssl, requests
from email.mime.text import MIMEText
from os import urandom, chdir, path
from functools import wraps
from importlib.machinery import SourceFileLoader
from cardreader_server_adress import host as cardreader_host, port as cardreader_port

cardreader_api_key = None
with open("api_key_for_cardreader.json", "r") as f:
    cardreader_api_key = json.load(f)

app = flask.Flask(__name__)
app.secret_key = urandom(24)

def silashik_operation(username, cash_change, description):
    print(username, cash_change, description)
    try:
        db = sqlite3.connect('./ssData.sqlite3')
    except:
        return {'ok': False, 'error': "Couldn't open database"}
    try:
        c = db.cursor()
        c.execute('SELECT cash FROM history WHERE username=(?) ORDER BY created_at DESC LIMIT 1', (username,))
        cash = c.fetchone()[0]
        c.execute('INSERT INTO history VALUES (?, ?, ?, ?, ?)', (username, description, cash_change, cash + cash_change, datetime.datetime.now()))
        db.commit()
        return {'ok': True}
    except:
        return {'ok': False, 'error': 'Something went wrong. Does the user exist?'}
    finally:
        db.close()

def get_cash(username):
    db = sqlite3.connect('./ssData.sqlite3')
    c = db.cursor()
    c.execute('SELECT cash FROM history WHERE username=(?) ORDER BY created_at DESC LIMIT 1', (username,))
    ans = c.fetchone()
    db.close()
    try:
        return ans[0]
    except:
        return None

def get_authorized():
    username = flask.session.get('username')
    if username is None:
        return (None, None)
    return (username, get_cash(username))

def if_logged(func):
    @wraps(func)
    def result(*args, **kwargs):
        username, cash = get_authorized()
        if username is None:
            return flask.redirect('/', 302)
        return func(*args, **kwargs)
    return result

@app.route("/", methods=['GET', 'POST'])
def index():
    if(flask.request.method == 'GET'):
        username, cash = get_authorized()
        if(username is None):
            return flask.render_template('login.html')
        db = sqlite3.connect('./ssData.sqlite3')
        c = db.cursor()
        c.execute('SELECT medal FROM userdata WHERE username=(?)', (username,))
        medal, = c.fetchone()
        c.execute('SELECT description, cash_change, created_at FROM history WHERE username=(?) ORDER BY created_at DESC LIMIT 5', (username,))
        his = [(desc, '{:+}'.format(cash_change), when) for desc, cash_change, when in c.fetchall()]
        if(len(his) < 5):
            his += [('&mdash;', '&mdash;', '&mdash;')] * (5 - len(his))
        his = ['<tr class="s_row"><td>{}</td><td>{}</td><td>{}</td></tr>'.format(desc, cash_change, when) for desc, cash_change, when in his]
        return flask.render_template('main.html', data='\n'.join(his), cash=cash, medal=''.join(['<img src="{}" />'.format(flask.url_for('static', filename='medal.jpg')) for _ in range(medal)]))
    else:
        username = flask.request.form["login"]
        password = flask.request.form["password"]
        db = sqlite3.connect('./ssData.sqlite3')
        c = db.cursor()
        c.execute('SELECT encoded_password FROM userdata WHERE username=(?)', (username,))
        encoded_password = c.fetchone()
        try:
            encoded_password = encoded_password[0].encode('utf-8')
        except:
            encoded_password = None
        db.close()
        if (encoded_password is not None) and (bcrypt.checkpw(password.encode('utf-8'), encoded_password)):
            flask.session['username'] = username
            return flask.redirect('/', 302)
        else:
            return flask.render_template('login.html', msg='<b>Неверная пара логин-пароль</b>')

@app.route("/logout", strict_slashes=False)
def logout():
    flask.session.pop('username', None)
    return flask.redirect('/', 302)

@app.route("/shop")
@if_logged
def shop():
    username, cash = get_authorized()
    db = sqlite3.connect('./ssData.sqlite3')
    c = db.cursor()
    c.execute('SELECT name, price, products_picture1 FROM shop_products')
    insert = '\n'.join('''<div class="col-6">
                                <a href="/shop/{0}"><div class="col-12">
                                    <img src="{1}" class="col-12">
                                    <div class="row">
                                        <div class="col-3"></div>
                                        <div class="col-6">
                                            <p class="sm_header">{0}</p>
                                            <div class="row col-12">
                                                <img src="{3}" class="col-6" style="height: 100%">
                                                <p class="sm_header col-6">{2}</p>
                                            </div>
                                        </div>
                                        <div class="col-3"></div>
                                    </div>                                 
                                </div></a>
                            </div>'''.format(product_name, flask.url_for('static', filename=pic), price, flask.url_for('static', filename='Silashik_holder2.png')) for product_name, price, pic in c.fetchall())
    db.close()
    return flask.render_template('shop.html', products=insert, cash=cash)

@app.route("/shop/<product_name>")
@if_logged
def shop_product(product_name):
    username, cash = get_authorized()
    db = sqlite3.connect('./ssData.sqlite3')
    c = db.cursor()
    c.execute('SELECT price, characteristics, description, products_picture2 FROM shop_products WHERE name=(?)', (product_name,))
    try:
        price, characteristics, description, pic = c.fetchone()
    except Exception as e:
        return flask.abort(404)
    db.close()
    return flask.render_template('product.html', pic_src=flask.url_for('static', filename=pic), desc=description, char=characteristics, price=price, link=('#" onclick="alert(\'Недостаточно средств\');' if cash < price else '/buy/{}'.format(product_name)), page_title=product_name, cash=cash)

@app.route("/help")
def description():
    username, cash = get_authorized()
    if cash is None:
        cash = ''
    return flask.render_template('help.html', cash=cash)

@app.route("/change_password", methods=['GET', 'POST'])
@if_logged
def password_changer():
    username, cash = get_authorized()
    if(flask.request.method == 'GET'):
        return flask.render_template('change_password.html', cash=cash)
    else:
        old_password = flask.request.form["old_password"]
        new_password = flask.request.form["new_password"]
        new_password_repeat = flask.request.form["new_password_repeat"]
        db = sqlite3.connect('./ssData.sqlite3')
        c = db.cursor()
        c.execute('SELECT encoded_password FROM userdata WHERE username=(?)', (username,))
        encoded_password = c.fetchone()
        try:
            encoded_password = encoded_password[0].encode('utf-8')
        except:
            encoded_password = None
        if (encoded_password is not None) and (bcrypt.checkpw(old_password.encode('utf-8'), encoded_password)):
            if new_password != new_password_repeat:
                db.close()
                return flask.render_template('change_password.html', msg='<b>Новые пароли не совпали</b>', cash=cash)
            else:
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                db = sqlite3.connect('./ssData.sqlite3')
                c = db.cursor()
                c.execute('UPDATE userdata SET encoded_password=(?) WHERE username=(?)', (hashed, username))
                db.commit()
                db.close()
                return flask.render_template('change_password.html', msg='<b>Пароль успешно сменён</b>', cash=cash)
        else:
            db.close()
            return flask.render_template('change_password.html', msg='<b>Не удалось провести стандартную операцию со старым паролем. Рекомендуется обратиться к администратору SilaederStore</b>', cash=cash)

@app.route("/buy/<product>")
@if_logged
def buy(product):
    username, cash = get_authorized()
    db = sqlite3.connect('./ssData.sqlite3')
    c = db.cursor()
    c.execute('SELECT name, price, characteristics, description FROM shop_products WHERE name=(?)', (product,))
    try:
        name, price, characteristics, description = c.fetchone()
    except:
        return flask.abort(404)
    result = ''
    if cash < price:
        result = 'Недостаточно средств'
    else:
        if(name == 'Медалька'):
            c.execute('SELECT medal FROM userdata WHERE username=(?)', (username,))
            medal, = c.fetchone()
            c.execute('UPDATE userdata SET medal=(?) WHERE username=(?)', (medal + 1, username))
            db.commit()
            silashik_operation(username, -price, 'Покупка "{}"'.format(product))
            db.close()
            result = "Теперь медалька будет отображаться на главной странице SilaederStore!"
        else:
            from secrets import gmail_login, gmail_password, buy_alert_recipient
            try:
                context = ssl.create_default_context()
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
                server.login(gmail_login, gmail_password)
                c.execute('SELECT first_name, last_name FROM userdata WHERE username=(?)', (username,))
                first_name, last_name = c.fetchone()
                msg = MIMEText('Здравствуйте! Автоматическая система уведомлений SilaederStore сообщает, что пользователь {} {} приобрел {} за {} силашиков'.format(first_name, last_name, product, price), _charset="UTF-8")
                server.sendmail('SilaederStore mail service', buy_alert_recipient, msg.as_string())
                server.quit()
            except:
                result = 'Произошла ошибка при попытке связаться с сервером gmail. Пожалуйста, сообщите об этом <a href="http://vk.com/kolay_ne">мне</a>'
            if(result == ''):
                silashik_operation(username, -price, 'Покупка "{}"'.format(product))
                result = "Покупка выполнена успешно"
    db.close()
    return '''<html><head></head><body>
    <script type="text/javascript">
    alert('{}');
    document.location.href = '/shop/{}';
    </script></body></html>'''.format(result, product)

def exec_cardreader_method(method_name, data, api_key):
    data['api_key'] = api_key
    r = requests.post('http://{}:{}/api/{}'.format(cardreader_host, cardreader_port, method_name),
        data=data)
    return r.json()

@app.route("/school_entries", methods=['GET', 'POST'])
@if_logged
def school_entries():
    username, cash = get_authorized()
    db = sqlite3.connect('ssData.sqlite3')
    c = db.cursor()
    c.execute('SELECT status FROM userdata WHERE username=(?)', (username,))
    status, = c.fetchone()
    db.close()
    last, ok, must = json.loads(exec_cardreader_method('get_uservisible_data', {'username': username}, cardreader_api_key)['data'])
    result = ''
    if flask.request.method == 'GET':
        return flask.render_template('cardreader.html', last_enter=last, must=must, ok=ok, teacher_block=('' if status == 2 else 'display: none;'), cash=cash)
    else:
        db = sqlite3.connect('ssData.sqlite3')
        c = db.cursor()
        c.execute('SELECT status FROM userdata WHERE username=(?)', (username,))
        status, = c.fetchone()
        if(status != 2):
            return flask.abort(403)
        try:
            name, last_name, date, time = (flask.request.form[x] for x in ('name', 'last_name', 'date', 'time'))
            date = tuple(int(x) for x in date.split('.'))
            assert(len(date) == 3)
            time = tuple(int(x) for x in time.split(':'))
            assert(len(time) == 2)
        except:
            result = 'Не все данные указаны или данные имеют неверный формат'
        if result == '':
            c.execute('SELECT username FROM userdata WHERE first_name=(?) AND last_name=(?)', (name, last_name))
            excepting_username = [x[0] for x in c.fetchall()]
            db.close()
            if len(excepting_username) == 0:
                result = 'В базе нет такого человека'
            elif len(excepting_username) > 1:
                result = 'В базе несколько человек с такими именем и фамилией. Обратитесь к администратору SilaederStore'
            else:
                excepting_username = excepting_username[0]
                try:
                    dt = datetime.datetime(day=date[0], month=date[1], year=date[2], hour=time[0], minute=time[1])
                    exec_cardreader_method('get_uservisible_data', {'username': username, 'dt': str(dt).split('.')[0]}, api_key)
                except:
                    result = 'Не удалось создать исключение. Если вы уверены, что данные корректны, крайне рекомендуется обратиться к администратору SilaederStore'
        if result == '':
            result = 'Исключение успешно создано!'
        return flask.render_template('cardreader.html', last_enter=last, must=must, ok=ok, teacher_block=('' if status == 2 else 'display: none;'), tb_error_msg='<b>{}</b>'.format(result), cash=cash)

@app.route("/api/silashik_operation", methods=['POST'])
def silashik_operation_execer():
    with open("api_keys_allowed_mainblock.json", "r") as f:
        api_keys = json.load(f)
    if(set(flask.request.form.keys()) != set(['username', 'cash_change', 'description', 'api_key'])):
        return json.dumps({'ok': False, 'error': 'Wrong arguments given. You have to send exactly: username, cash_change, description, api_key'})
    username, cash_change, description, api_key = (flask.request.form[i] for i in ['username', 'cash_change', 'description', 'api_key'])
    cash_change = int(cash_change)
    if(api_key not in api_keys):
        return json.dumps({'ok': False, 'error': 'Unknown api key'})
    return json.dumps(silashik_operation(username, cash_change, description))

if __name__ == '__main__':
    chdir(path.dirname(path.abspath(__file__)))
    app.run('0.0.0.0', 5006)
