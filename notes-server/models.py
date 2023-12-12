from app import db

class Note(db.Model):
    __tablename__='notes'
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(500))

    def __init__(self, title, content):
        self.title=title
        self.content=content