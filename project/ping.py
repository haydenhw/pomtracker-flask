from flask import Blueprint
import json
from project.db import db
from project.authors.models import Author

ping_blueprint = Blueprint('ping', __name__)

@ping_blueprint.route('/ping')
def ping():
    author_dict = dict(first='harry', last='truman')
    author = Author(**author_dict)
    db.session.add(author)
    db.session.commit()
    result = Author.query.first()
    return {
        'port': json.dumps({'first': result.first, 'last': result.last}),
        'status': 'success',
        'message': 'pong'
    }
