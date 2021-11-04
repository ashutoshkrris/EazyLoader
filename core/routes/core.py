from datetime import datetime, timedelta
from flask.helpers import make_response
from core import app, mail
from flask import render_template, send_file, request, flash, url_for, redirect, Response, current_app
from decouple import config
from werkzeug.exceptions import NotFound, InternalServerError, MethodNotAllowed
from core.utils.blogs import fetch_posts, get_blog_post
from flask_mail import Message
from core.utils.contributors import get_contributors


ADMIN_EMAIL = config('ADMIN_EMAIL', default=None)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')

            msg = Message("EazyLoader Notification",
                          sender=("EazyLoader", ADMIN_EMAIL), recipients=[ADMIN_EMAIL])
            msg.html = render_template('email_template.html', name=name, email=email,
                                       message=message, ip_addr=str(request.remote_addr))
            mail.send(msg)
            flash("We've received your details, thank you!", "success")
            return redirect(url_for('index', _anchor="contact"))

        except Exception as e:
            print(e)
            flash('Something went wrong! Try Again.', "error")
            return redirect(url_for('index', _anchor="contact"))

    return render_template('index.html', title='Home')


# Custom routes to check errors.
@app.route("/tos")
def tos():
    return render_template('tos.html', title='Terms of Service')


@app.route("/blogs")
def blog():
    posts = fetch_posts()
    return render_template('blog/blog.html', title='Blogs', posts=posts)


@app.get('/post/<id>/<slug>')
def single_page(id, slug):
    post = get_blog_post(id, slug)
    return render_template('blog/single.html', post=post, title=f"{post['fields']['title']}")


@app.route("/donate")
def donate():
    return render_template('donate.html', title='Make your donation now')


@app.errorhandler(NotFound)
def handle_not_found(e):
    return render_template('error/404.html', title="404 Not Found")


@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    return render_template('error/500.html', title='500 Internal Server Error')


@app.errorhandler(MethodNotAllowed)
def method_not_allowed(e):
    return render_template('error/405.html', title="405 Method Not Allowed")


@app.get('/contributors')
def contributors_page():
    contributors = get_contributors()
    return render_template('contributors.html', title="Contributors", contributors=contributors)


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    pages = []

    # get static routes
    # use arbitary 10 days ago as last modified date
    lastmod = datetime.now() - timedelta(days=10)
    lastmod = lastmod.strftime('%Y-%m-%d')
    for rule in current_app.url_map.iter_rules():
        # omit auth and admin routes and if route has parameters. Only include if route has GET method
        if 'GET' in rule.methods and len(rule.arguments) == 0 \
                and not rule.rule.startswith('/admin') \
                and not rule.rule.startswith('/auth') \
                and not rule.rule.startswith('/test'):
            pages.append([f'{request.url_root[:-1]}' + rule.rule, lastmod])

    sitemap_template = render_template(
        'sitemap/sitemap_template.xml', pages=pages)
    response = make_response(sitemap_template)
    response.headers['Content-Type'] = 'application/xml'
    return response
