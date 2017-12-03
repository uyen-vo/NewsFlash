from flask import Flask, jsonify, render_template, request
import jinja2

app = Flask(__name__, static_folder='static')
app.jinja_loader = jinja2.FileSystemLoader('../NewsFlash')

@app.route('/get_images')
def add_numbers():
	a = request.args.get('a', 0, type=str)
	print a
	return jsonify(result= "hellyeah")


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
