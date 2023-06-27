from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')             # отслеживание переходов на разные страницы: через декоратор @. '/' - main
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':  # какой главный файл запускается -  проверка
    app.run(debug=True)     # app.run(debug=True) показ bug на сайте

 