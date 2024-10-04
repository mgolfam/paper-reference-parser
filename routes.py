import re
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

def parse_reference_string(reference_string):
    try:
        # Improved regex to handle authors, multiple lines, and optional DOI/URL
        match = re.search(
            r'(.+?) \((\d{4}[a-z]?)\)\. (.+?)\. (.+?)(?:, (\d+)(?:\((\d+)\))?)?(?:, (\d+–\d+))?\.?(.*)',
            reference_string, re.DOTALL
        )
        if match:
            author = match.group(1).strip()
            year = match.group(2).strip()
            title = match.group(3).strip()
            journal = match.group(4).strip()
            volume = match.group(5).strip() if match.group(5) else None
            issue = match.group(6).strip() if match.group(6) else None
            pages = match.group(7).strip() if match.group(7) else None
            doi = match.group(8).strip() if match.group(8) else None
            return author, title, journal, year, volume, issue, pages, doi
        else:
            raise ValueError("Invalid reference format")
    except Exception as e:
        raise ValueError(f"Failed to parse reference: {str(e)}")



# Route to handle adding a reference using both form or plain string input
@main_routes.route('/project/<int:project_id>/add_reference', methods=['POST'])
def add_reference(project_id):
    if 'plain_reference' in request.form and request.form['plain_reference']:
        # If plain string reference is provided
        plain_reference = request.form['plain_reference']
        try:
            author, title, journal, year, volume, pages, doi = parse_reference_string(plain_reference)
            new_ref = Reference(author=author, title=title, journal=journal, year=year, project_id=project_id)
            db.session.add(new_ref)
            db.session.commit()
        except ValueError as e:
            return str(e), 400  # Return error if parsing fails
    else:
        # Handle the form input
        author = request.form['author']
        title = request.form['title']
        journal = request.form['journal']
        year = request.form['year']
        new_ref = Reference(author=author, title=title, journal=journal, year=year, project_id=project_id)
        db.session.add(new_ref)
        db.session.commit()
    
    return redirect(url_for('main.project_references', project_id=project_id))

# Route to display references for a selected project
@main_routes.route('/project/<int:project_id>')
def project_references(project_id):
    project = Project.query.get_or_404(project_id)
    references = Reference.query.filter_by(project_id=project_id).order_by(Reference.author).all()
    return render_template('project.html', project=project, references=references)

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
    ref = Reference.query.get_or_404(id)
    db.session.delete(ref)
    db.session.commit()
    return redirect(url_for('main.project_references', project_id=project_id))
