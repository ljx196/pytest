from sympy import *
import json
from flask import Flask, redirect, url_for, request
x, y, z, t = symbols('x y z t')
k, m, n = symbols('k m n', integer=True)
f, g, h = symbols('f g h', cls=Function)

app = Flask(__name__)

@app.route('/trigsimp', methods=['POST', 'GET'])
def trigsimps():
    data = request.get_data()
    # print(data)
    json_data = json.loads(data)
    # Exp = request.form.get('Exp')
    Exp = json_data.get("Exp")
    # print(Exp)
    rst = trigsimp(Exp)
    return str(rst)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6367)