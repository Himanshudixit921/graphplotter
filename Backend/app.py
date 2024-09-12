import matplotlib
matplotlib.use('Agg')  # Use Agg backend for non-GUI operations

from flask import Flask, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, symbols, lambdify
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define symbols
x, y = symbols('x y')

# Route to accept an equation and return a graph
@app.route('/plot', methods=['POST'])
def plot_graph():
    try:
        data = request.json
        equation = data.get('equation', 'x**2 + y**2 - 144')  # default equation
        expr = sympify(equation)

        # Check if the equation is implicitly defined
        if y in expr.free_symbols:
            # Generate x and y values for plotting
            x_vals = np.linspace(-12, 12, 400)
            y_vals_pos = np.sqrt(144 - x_vals**2)
            y_vals_neg = -np.sqrt(144 - x_vals**2)

            plt.figure()
            plt.plot(x_vals, y_vals_pos, label='Positive branch')
            plt.plot(x_vals, y_vals_neg, label='Negative branch')
            plt.title(f'Graph of {equation}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.axhline(0, color='black',linewidth=0.5)
            plt.axvline(0, color='black',linewidth=0.5)
            plt.grid(True)
            plt.legend()

        else:
            # Convert Sympy expression to a lambda function
            f = lambdify(x, expr, 'numpy')

            # Plot the graph
            x_vals = np.linspace(-10, 10, 400)
            y_vals = f(x_vals)

            plt.figure()
            plt.plot(x_vals, y_vals)
            plt.title(f'Graph of {equation}')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.grid(True)

        # Save plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()

        # Return the image to the client
        return send_file(img, mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
