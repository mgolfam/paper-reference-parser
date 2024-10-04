from db import db

# Define the Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    references = db.relationship('Reference', backref='project', lazy=True)

# Define the Reference model
class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    journal = db.Column(db.String(200))
    year = db.Column(db.Integer)
    volume = db.Column(db.String(50))  # Add volume field
    issue = db.Column(db.String(50))   # Add issue field
    pages = db.Column(db.String(50))   # Add pages field
    doi = db.Column(db.String(200))    # Add DOI field
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
