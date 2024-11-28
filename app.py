from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_tenant', methods=['POST'])
def add_tenant():
    name = request.form.get('name')
    unit = request.form.get('unit')
    phone = request.form.get('phone')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
