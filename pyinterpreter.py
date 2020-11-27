from flask import Flask, redirect, url_for, request
import json
from sympy import *

app = Flask(__name__)

@app.route('/interpreter', methods=['POST', 'GET'])
def interpreter():
    data = request.get_data()
    json_data = json.loads(data)
    cmds = json_data.get("cmds")
    print(cmds)
    for cmd in cmds:
        exec(cmd, globals())

    print(ans)
    return str(ans)

if __name__ == '__main__':
    app.run(debug=True)
