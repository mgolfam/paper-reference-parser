import re
from flask import Blueprint, render_template, request, redirect, url_for
from models import Project, Reference
import json
from db import db
from reference_parser import BruteForceReferenceParser  # Import the new parser class
from nlp_parser import nlp_parser  # Import the new parser class


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

def parse_reference_string1(reference_string):
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

def parse_reference_string(reference_string):
    try:
        # Updated regex to handle more complex volume/issue structures
        match = re.search(
            r'(.+?) \((\d{4}[a-z]?)\)\. (.+?)\. (.+?)(?:, (\d+(?:\(.+?\))?))?(?:, (\d+–\d+))?\.?(.*)',
            reference_string, re.DOTALL
        )
        if match:
            author = match.group(1).strip()
            year = match.group(2).strip()
            title = match.group(3).strip()
            journal = match.group(4).strip()
            volume_issue = match.group(5).strip() if match.group(5) else None
            pages = match.group(6).strip() if match.group(6) else None
            doi = match.group(7).strip() if match.group(7) else None

            # Split volume and issue if they are in the format 80(2/3/4)
            if volume_issue and '(' in volume_issue:
                volume, issue = volume_issue.split('(', 1)
                issue = issue.strip(')')
            else:
                volume = volume_issue
                issue = None

            return author, title, journal, year, volume, issue, pages, doi
        else:
            raise ValueError("Invalid reference format")
    except Exception as e:
        raise ValueError(f"Failed to parse reference: {str(e)}")

def parse_reference_string(reference_string):
    try:
        # Adjusted regex to be more flexible with optional DOI, pages, and volume/issue formats
        match = re.search(
            r'(.+?) \((\d{4}[a-z]?)\)\. (.+?)\. (.+?)(?:, (\d+(?:\(.+?\))?))?(?:, (\d+–\d+))?\.?(.*)',
            reference_string, re.DOTALL
        )
        if match:
            author = match.group(1).strip()
            year = match.group(2).strip()
            title = match.group(3).strip()
            journal = match.group(4).strip()
            volume_issue = match.group(5).strip() if match.group(5) else None
            pages = match.group(6).strip() if match.group(6) else None
            doi = match.group(7).strip() if match.group(7) else None

            # Handle volume and issue formats like "80(2/3/4)" or "80"
            if volume_issue and '(' in volume_issue:
                volume, issue = volume_issue.split('(', 1)
                issue = issue.strip(')')
            else:
                volume = volume_issue
                issue = None

            # Return the components
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
        # parser = BruteForceReferenceParser(plain_reference)  # Instantiate the parser
        parsed_refs = nlp_parser(plain_reference)

        for parsed_ref in parsed_refs:
            # Save the parsed reference to the database
            # Use 'authors' instead of 'author'
            new_ref = Reference(
                author=parsed_ref['authors'],  # Fix this line
                title=parsed_ref['title'],
                journal=parsed_ref['journal'],
                year=parsed_ref['year'],
                volume=parsed_ref['volume'],
                issue=parsed_ref['issue'],
                pages=parsed_ref['pages'],
                doi=parsed_ref['doi'],
                project_id=project_id,
                original_string=parsed_ref['original_string']
            )
            db.session.add(new_ref)
            
        db.session.commit()
    else:
        # Handle the form input (individual fields)
        author = request.form['author']
        title = request.form['title']
        journal = request.form['journal']
        year = request.form['year']
        doi = request.form['doi']
        new_ref = Reference(
            author=author,
            title=title,
            journal=journal,
            year=year,
            doi=doi,
            project_id=project_id
        )
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
    if id:
        # If ID is provided, fetch the reference for editing
        ref = Reference.query.get_or_404(id)
    else:
        # If no ID is provided, create a new reference object
        ref = None
    
    if request.method == 'POST':
        # Handle form submission for both adding and editing references
        author = request.form['author']
        title = request.form['title']
        journal = request.form['journal']
        year = request.form['year']
        volume = request.form['volume']
        issue = request.form['issue']
        pages = request.form['pages']
        doi = request.form['doi']
        
        if ref:
            # If reference exists, update the existing fields
            ref.author = author
            ref.title = title
            ref.journal = journal
            ref.year = year
            ref.volume = volume
            ref.issue = issue
            ref.pages = pages
            ref.doi = doi
            ref.reviewed = True
        else:
            # If no reference, create a new reference with project_id
            ref = Reference(
                author=author,
                title=title,
                journal=journal,
                year=year,
                volume=volume,
                issue=issue,
                pages=pages,
                doi=doi,
                project_id=project_id
            )
            db.session.add(ref)
        
        db.session.commit()
        return redirect(url_for('main.project_references', project_id=project_id))
    print(json.dumps(ref.to_dict(), indent=4))
    return render_template('edit_reference.html', ref=ref)

# Route to delete a reference
@main_routes.route('/project/<int:project_id>/delete_reference/<int:id>')
def delete_reference(project_id, id):
    ref = Reference.query.get_or_404(id)
    db.session.delete(ref)
    db.session.commit()
    return redirect(url_for('main.project_references', project_id=project_id))

# Route to generate and display sorted references in journal format
@main_routes.route('/project/<int:project_id>/print')
def print_references(project_id):
    project = Project.query.get_or_404(project_id)
    # Sort references by author and year for a journal-like format
    references = Reference.query.filter_by(project_id=project_id).order_by(Reference.author, Reference.year).all()
    return render_template('print_references.html', project=project, references=references)

@main_routes.route('/project/<int:project_id>/add_reference', methods=['GET'])
def add_reference_form(project_id):
    project = Project.query.get_or_404(project_id)
    return render_template('edit_reference.html', ref={}, project=project)
