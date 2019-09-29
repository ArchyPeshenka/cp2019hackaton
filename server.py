from flask import Flask, request
import json
from preprocess import DataWorker

app = Flask(__name__)
FlaskDataWorker = DataWorker()
FlaskDataWorker.load_data('data.csv')

@app.route('/', methods=['POST'])
def get_data():
	FlaskDataWorker.append_batch(eval(request.form['data']))
	FlaskDataWorker.save_data('data.csv', inplace=True)
	return 'None'

@app.route('/chk')
def check_con():
	return 'True'

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)['data']