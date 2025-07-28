from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'inventory.json'


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/')
def home():
    items = load_data()
    return render_template('home.html', items=items)


@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = request.form['quantity']
    description = request.form['description']
    data = load_data()
    new_id = max([item['id'] for item in data], default=0) + 1
    data.append({'id': new_id, 'name': name, 'quantity': int(quantity), 'description': description})
    save_data(data)
    return redirect(url_for('home'))


@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    data = load_data()
    data = [item for item in data if item['id'] != item_id]
    save_data(data)
    return redirect(url_for('home'))


@app.route('/edit/<int:item_id>', methods=['POST'])
def edit_item(item_id):
    data = load_data()
    for item in data:
        if item['id'] == item_id:
            item['name'] = request.form['name']
            item['quantity'] = int(request.form['quantity'])
            item['description'] = request.form['description']
            break
    save_data(data)
    return redirect(url_for('home'))


@app.route('/get_item/<int:item_id>')
def get_item(item_id):
    data = load_data()
    item = next((i for i in data if i['id'] == item_id), None)
    return jsonify(item) if item else ('', 404)


if __name__ == '__main__':
    app.run(debug=True)
