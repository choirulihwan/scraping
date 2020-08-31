from flask import Flask, render_template, request
import requests

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def index():
    currencies = ['idr', 'usd', 'eur', 'gbp']
    data = request.form.get('curr')
    print(data)

    if data is None or data == "-":
        url = 'http://www.floatrates.com/daily/idr.json'
    else:
        url = 'http://www.floatrates.com/daily/{}.json'.format(data)

    json_data = requests.get(url).json()
    return render_template('idr_rates.html', datas=json_data.values(), currencies=currencies, selected=data)


# global filter
@app.template_filter()
def number_format(value):
    return format(int(value), ',d')


if __name__ == '__main__':
    app.run(debug=True)



