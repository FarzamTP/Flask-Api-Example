import numpy as np
from flask import Flask
from flask import request
from flask import jsonify
from scipy.optimize import linprog

# TODO:
# [] Plot a plan

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'This is a prototype for Flask-Api-Request!'


@app.route('/solve', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        """
        Minimize          w = 10 * y1 + 15 * y2 + 25 * y3
        Subject to:       y1 + y2 + y3 >= 1000
                          y1 - 2 * y2    >= 0
                                      y3 >= 340
        with              y1             >= 0
                                y2       >= 0
        """

        """
        A = request.args.get('A')
        b = request.args.get('b')
        c = request.args.get('c')
        """

        A = np.array([[-1, -1, -1],
                      [-1, 2, 0],
                      [0, 0, -1],
                      [-1, 0, 0],
                      [0, -1, 0]])

        b = np.array([-1000, 0, -340, 0, 0])
        c = np.array([10, 15, 25])

        res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

        return {"opt-val": np.around(res.fun, 3),
                "X": list(np.around(res.x, decimals=3))}


if __name__ == '__main__':
    app.run()
