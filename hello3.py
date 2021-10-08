"""basic Flask app - demo of using a variable in a route"""

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    greet = '<h1>Hello, Gators!</h1>'
    link = '<p><a href="user/Dave">Click me!</a></p>'
    return greet + link

@app.route('/user/<name>/<blog>')
def user(name, blog):
    personal = f'<h1>Hello, {name}, this is your {blog} blog!</h1>'
    # above - the curly braces {} hold a variable; when this runs,
    # the value will replace the braces and the variable name
    instruc = '<p>Change the name in the <em>browser address bar</em> \
        and reload the page.</p>'
    return personal + instruc

if __name__ == '__main__':
    app.run(debug=True)