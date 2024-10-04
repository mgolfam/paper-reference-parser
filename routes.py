from flask import Blueprint, render_template, request, redirect, url_for
from models import Project, Reference
from db import db

# Define a Blueprint for routes
main_routes = Blueprint('main', __name__)

# Home route to display projects and form to add a new project
@main_routes.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

# Route to add a project
@main_routes.route('/add_project', methods=['POST'])
def add_project():
    name = request.form['name']
    new_project = Project(name=name)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('main.index'))

# Route to display references for a selected project
@main_routes.route('/project/<int:project_id>')
def project_references(project_id):
    project = Project.query.get_or_404(project_id)
    references = Reference.query.filter_by(project_id=project_id).order_by(Reference.author).all()
    return render_template('project.html', project=project, references=references)
