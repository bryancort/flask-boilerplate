#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/v1/healthcheck')
def health():
    return jsonify({'status': 'ok'}), 200


@app.route('/v1/testing', methods=['GET'])
def test_get():
    return jsonify({'data': 'test GET successful'}), 200


@app.route('/v1/testing', methods=['PUT'])
def test_put():
    return jsonify({'data': 'test PUT successful'}), 200


@app.route('/v1/testing', methods=['POST'])
def test_post():
    return jsonify({'data': 'test POST successful'}), 200


@app.route('/v2/testing/<id>', methods=['GET'])
def test_get_v2(id):
    return jsonify({'id': id}), 200


@app.route('/v2/testing/<id>', methods=['PUT'])
def test_put_v2(id):
    payload = request.get_json(silent=True) or request.form.to_dict() or {}
    return jsonify({'id': id, 'payload': payload}), 200


@app.route('/v2/testing/<id>', methods=['POST'])
def test_post_v2(id):
    payload = request.get_json(silent=True) or request.form.to_dict() or {}
    return jsonify({'id': id, 'payload': payload}), 200


@app.route('/v3/testing', methods=['GET'])
def test_get_v3():
    query_params = request.args.to_dict()
    return jsonify({'data': 'all our testing records', 'query': query_params}), 200


@app.route('/v3/testing/<id>', methods=['GET'])
def test_get_v3_with_id(id):
    query_params = request.args.to_dict()
    return jsonify({'data': f'testing record with id {id}', 'id': id, 'query': query_params}), 200


@app.route('/v3/testing/<id>', methods=['PUT'])
def test_put_v3(id):
    payload = request.get_json(silent=True) or request.form.to_dict() or {}
    query_params = request.args.to_dict()
    return jsonify({'data': f'updated testing record with id {id}', 'id': id, 'payload': payload, 'query': query_params}), 200


@app.route('/v3/testing', methods=['POST'])
def test_post_v3():
    payload = request.get_json(silent=True) or request.form.to_dict() or {}
    query_params = request.args.to_dict()
    return jsonify({'data': 'newly created testing record', 'payload': payload, 'query': query_params}), 200

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
