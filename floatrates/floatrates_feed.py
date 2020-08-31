from flask import Flask, render_template, request
import requests, locale

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


# global filter tidak menerima argument/parameter
@app.template_filter()
def number_format_temp(value):
    locale.setlocale(locale.LC_NUMERIC, '')
    return locale.format_string("%.*f", (2, value), True)

# jika memerlukan argument/parameter input, gunakan context_processor
@app.context_processor
def number_format():
    def _number_format(value, digit):
        locale.setlocale(locale.LC_NUMERIC, '')
        return locale.format_string("%.*f", (digit, value), True)
    return dict(number_format=_number_format)


if __name__ == '__main__':
    app.run(debug=True)



