from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lol')
def lol():
    with open('predictions/lol_prediction.json', 'r') as lol_file:
        lol_data = json.load(lol_file)  # Assuming this is a list of predictions
    return render_template('lol.html', predictions=lol_data)


@app.route('/cs2')
def cs2():
    with open('predictions/cs2_prediction.json', 'r') as cs2_file:
        cs2_data = json.load(cs2_file)  # Load directly as it's a list
    return render_template('cs2.html', predictions=cs2_data)

if __name__ == "__main__":
    app.run(debug=True)
