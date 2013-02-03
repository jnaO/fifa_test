from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello(name=None):
    return render_template('path/test/hello.html', name=name)

@app.route('/history')
def history():
    return 'Past cups!'

@app.route('/history/<cup_name>')
def history_cup(cup_name):
    return render_template('history/past_cup.html', name=cup_name)
    # return 'Cup %s!' % cup_name

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         return 'logged in'
#     else:
#         show_the_login_form()

if __name__ == '__main__':
    app.debug = True
    app.run()