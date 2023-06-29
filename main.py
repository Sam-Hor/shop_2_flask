from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout

app = Flask(__name__)
# обращение к настройкам - указание настройки база данных какая используется - создается
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # объект на основе класса


class Item(db.Model):  # работает с товарами на сайте (база данных)
    # primary_key=True введение первичного ключа - присваивание номера в базе
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    # text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title

# отслеживание переходов на разные страницы: через декоратор @. '/' - main
@app.route('/')
def index():
    items = Item.query.order_by(Item.price).all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id) # получить товар по его id чтобы далее взять его цену
    api = Api(merchant_id=1396424,
    secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "USD",
        "amount": str(item.price) + "00" #добавление 'копеек' для fondy
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

# страница добавления товара в базу данных
@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Ошибка ввода"
    else:
        return render_template('create.html')

with app.app_context():
    db.create_all()
    
if __name__ == '__main__':  # какой главный файл запускается -  проверка
    app.run(debug=True)     # app.run(debug=True) показ bug на сайте
