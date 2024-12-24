from flask import Flask, render_template, redirect, request, url_for
import requests
from config import VK_CLIENT_ID, VK_CLIENT_SECRET, VK_REDIRECT_URI  # , SECRET_KEY

app = Flask(__name__, static_url_path='', static_folder="static", template_folder="templates")

app.jinja_env.globals.update(BOTID = "8000167095") #айди бота из токена до знака ":"
app.jinja_env.globals.update(BOTNAME = "nmigunovaAppAuthbot") #имя вашего бота с приставкой bot
app.jinja_env.globals.update(BOTDOMAIN = "https://nmigunova.pythonanywhere.com") 


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth')
def auth():
    return render_template('auth.html')

@app.route('/auth/auth_vk')
def auth_vk():
    # Получаем код авторизации
    code = request.args.get('code')
    print(code)
    if code:
        print(code)
        # Обмен кода на токен
        token_url = 'https://oauth.vk.com/access_token'
        params = {
            'client_id': VK_CLIENT_ID,
            'client_secret': VK_CLIENT_SECRET,
            'redirect_uri': VK_REDIRECT_URI,
            'code': code
        }
        # Отправляем запрос на token_url с параметрами, указаннами выше
        response = requests.get(token_url, params=params)
        data = response.json()
        
        if 'access_token' in data: # или 'error' not in data
            # Успешная авторизация
            access_token = data['access_token']
            user_id = data['user_id']
            print(access_token) # debug
            return redirect(url_for("index"))
        else:
            return 'Ошибка авторизации'
    else:
        # Перенаправляем на страницу авторизации VK
        auth_url = f'https://oauth.vk.com/authorize?client_id={VK_CLIENT_ID}&display=page&redirect_uri={VK_REDIRECT_URI}&scope=email&response_type=code&v=5.131'
        return redirect(auth_url)

@app.route("/auth/auth_tg")
def auth_tg():
    user_id = request.args.get("id")
    print(user_id)
    first_name = request.args.get("first_name")
    photo_url = request.args.get("photo_url")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()

