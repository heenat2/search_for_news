from flask import Flask, render_template, flash, request
from wtforms import Form, StringField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = StringField('query:')
    pageNum = StringField('pageNum:')
    state = StringField('state:')


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        name = request.form['query']
        page = request.form['pageNum']
        state = request.form['state']
        new_form = ReusableForm(request.form)
        new_form.state = "topic1:token1/token2/token3::topic2:token1/token2/token3"
        new_form.pageNum = page
        print name
        print page
        print state
        flash("topic1:token1/token2/token3::topic2:token1/token2/token3")
        flash("1::2")
        for i in range(int(page), int(page) + 5):
            flash('Hello ' + name + "_" + str(i))
        return render_template('index.html', form=new_form)
    else:
        return render_template("index.html", form=ReusableForm(request.form))


if __name__ == "__main__":
    app.run()
