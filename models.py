from db import db

# Define the Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    references = db.relationship('Reference', backref='project', lazy=True)

# Define the Reference model
class Reference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewed = db.Column(db.Boolean, nullable=False, default=False)
    author = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    journal = db.Column(db.String(200))
    year = db.Column(db.Integer)
    volume = db.Column(db.String(50))  # Add volume field
    issue = db.Column(db.String(50))   # Add issue field
    pages = db.Column(db.String(50))   # Add pages field
    doi = db.Column(db.String(200))    # Add DOI field
    original_string = db.Column(db.String(1024))    # Add DOI field
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    
    # Method to convert the model instance to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'reviewed': self.reviewed,
            'author': self.author,
            'title': self.title,
            'journal': self.journal,
            'year': self.year,
            'volume': self.volume,
            'issue': self.issue,
            'pages': self.pages,
            'doi': self.doi,
            'project_id': self.project_id
        }
