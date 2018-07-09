from app import db

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    #pub_date = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        #if pub_date is None:
        #    pub_date = datetime.utcnow()
        #self.pub_date = pub_date


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))

    def __init__(self, email, password):
        self.email = email
        self.password =password
    
 