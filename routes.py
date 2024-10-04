from flask import Blueprint, render_template, request, redirect, url_for
from models import Project, Reference
from db import db

# Define a Blueprint for routes
main_routes = Blueprint('main', __name__)

# Home route to display projects
@main_routes.route('/')
def index():
    projects = Project.query.all()
    return render_template('index.html', projects=projects)

# Route to display references for a project
@main_routes.route('/project/<int:project_id>')
def project_references(project_id):
    project = Project.query.get_or_404(project_id)
    references = Reference.query.filter_by(project_id=project_id).order_by(Reference.author).all()
    return render_template('project.html', project=project, references=references)

# Route to add a project
@main_routes.route('/add_project', methods=['POST'])
def add_project():
    name = request.form['name']
    new_project = Project(name=name)
    db.session.add(new_project)
    db.session.commit()
    return redirect(url_for('main.index'))

# Route to add a reference under a project
@main_routes.route('/project/<int:project_id>/add_reference', methods=['POST'])
def add_reference(project_id):
    author = request.form['author']
    title = request.form['title']
    journal = request.form['journal']
    year = request.form['year']
    new_ref = Reference(author=author, title=title, journal=journal, year=year, project_id=project_id)
    db.session.add(new_ref)
    db.session.commit()
    return redirect(url_for('main.project_references', project_id=project_id))

# Route to edit a reference
@main_routes.route('/project/<int:project_id>/edit_reference/<int:id>', methods=['GET', 'POST'])
def edit_reference(project_id, id):
    ref = Reference.query.get_or_404(id)
    if request.method == 'POST':
        ref.author = request.form['author']
        ref.title = request.form['title']
        ref.journal = request.form['journal']
        ref.year = request.form['year']
        db.session.commit()
        return redirect(url_for('main.project_references', project_id=project_id))
    return render_template('edit_reference.html', ref=ref)

# Route to delete a reference
@main_routes.route('/project/<int:project_id>/delete_reference/<int:id>')
def delete_reference(project_id, id):
    ref = Reference.query.get(id)
    db.session.delete(ref)
    db.session.commit()
    return redirect(url_for('main.project_references', project_id=project_id))

# Route to generate a project report (simple placeholder for now)
@main_routes.route('/project/<int:project_id>/report')
def generate_report(project_id):
    project = Project.query.get_or_404(project_id)
    references = Reference.query.filter_by(project_id=project_id).all()
    # Logic to export report in desired format (e.g., CSV, BibTeX)
    return render_template('report.html', project=project, references=references)
