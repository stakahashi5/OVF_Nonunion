from flask import Flask, render_template, request
from model import predict
from form import OVFForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key_here"

@app.route('/', methods=['GET', 'POST'])
def index():
    form = OVFForm()
    prediction = None

    if form.validate_on_submit():
        data = {
            'Age': form.Age.data,
            'sex_2.0': 1 if form.sex.data == 2 else 0,
            'VAS0': form.VAS0.data,
            'MRIday': form.MRIday.data,
            'KypFle0': form.KypFle0.data,
            'Level3_2': 1 if form.Level3.data == 2 else 0,
            'Level3_3': 1 if form.Level3.data == 3 else 0,
            'T203_2': 1 if form.T203.data == 2 else 0,
            'T203_3': 1 if form.T203.data == 3 else 0,
            'Poste02_1': 1 if form.Poste02.data == 1 else 0
        }

        processed_data = list(data.values())

        pred_proba = predict(processed_data)
        print(pred_proba)
        prediction = f"Risk: {pred_proba * 100:.2f}%"
        print(prediction)

    return render_template('index.html', form=form, prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)