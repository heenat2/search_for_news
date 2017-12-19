from markupsafe import Markup
from gensim.models import Word2Vec
from search import Search
from flask import Flask, render_template, flash, request
from wtforms import Form, StringField

# App config.
from lda_infer_topics2 import TopicInference

DEBUG = False
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
global search
global lda_inference
global w2v


class ReusableForm(Form):
    name = StringField('query:')
    pageNum = StringField('pageNum:')
    state = StringField('state:')


def get_topic_string(results):
    top_topics = lda_inference.infer_topics(results)
    return '::'.join(map(lambda x: x + ":" + get_w2v_similarity(x), top_topics))


def get_w2v_similarity(term):
    if term in w2v:
        term_list = [term_cos_tup[0] for term_cos_tup in w2v.wv.most_similar(positive=[term],topn=10)]
        return '/'.join(term_list)
    else:
        return ' '


@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        query = request.form['query']
        page = request.form['pageNum']
        state = request.form['state']
        if not page:
            page = 0
        print query
        print page
        print state
        search_results = search.get_results_for_query(query + " " + ' '.join(state.split("::")), max_results=100)
        topic_string = get_topic_string(search_results)
        flash(topic_string)
        new_form = ReusableForm(request.form)
        new_form.pageNum = page
        new_form.state = topic_string
        flash("1::2")
        for doc in search_results:
            flash(Markup("<a href='" + doc.get_url() + "'>"
                         + doc.get_title() + "</a><br></br>" + "<div>" +
                         doc.get_text() + "</div>"))

        return render_template('index.html', form=new_form)
    else:
        return render_template("index.html", form=ReusableForm(request.form))


if __name__ == "__main__":
    global search
    search = Search()
    global lda_inference
    lda_inference = TopicInference('resource/corpusdata.dictionary',
                                   'models/lda_model/LDAModel50Symmetric/ldamodel')
    global w2v
    w2v = Word2Vec.load('models/word_2_vec/w2vmodel')
    app.run(threaded=False)
