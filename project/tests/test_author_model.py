from project import db
from project.authors.models import Author

def test_author(test_app, test_db):
    db = test_db
    author_dict = dict(first='harry', last='truman')
    author = Author(**author_dict)
    db.session.add(author)
    db.session.commit()
    result = Author.query.first()
    assert result.first == 'harry'
