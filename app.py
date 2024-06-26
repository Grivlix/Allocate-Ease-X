from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload
from setup_db import Base, Employee, Skill, Project, Availability, EmployeeProjects
import random

app = Flask(__name__)

# Configure the database (update the connection string as needed)
engine = create_engine('sqlite:///employees.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/spreadsheet')
def show_spreadsheet():
    employees = session.query(Employee).options(joinedload(Employee.availability)).all()
    return render_template('spreadsheet.html', employees=employees)

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    prompt = data.get("prompt")

    # Fetch all employees from the database
    employees = session.query(Employee).all()

    # Transform employee data to match the expected format
    employee_data = []
    for employee in employees:
        skills = [{"skill_name": skill.skill_name, "proficiency_level": skill.proficiency_level} for skill in employee.skills]
        previous_projects = [project.project.project_name for project in employee.projects if project.project.status == "Completed"]
        active_projects = [project.project.project_name for project in employee.projects if project.project.status != "Completed"]

        employee_data.append({
            "image": employee.image,
            "name": employee.name,
            "job_title": employee.job_title,
            "employment_type": employee.employment_type,
            "contact_info": employee.contact_info,
            "available_hours_per_week": employee.availability.hours_available,
            "utilization": employee.availability.utilization,
            "skills": skills,
            "previous_projects": previous_projects,
            "active_projects": active_projects,
            "upcoming_leave": employee.availability.upcoming_leave  # Added upcoming leave info
        })

    # Randomly select 3 employees
    selected_employees = random.sample(employee_data, 3)

    # Format the response
    recommendations = {
        "top": selected_employees[0],
        "others": selected_employees[1:]
    }

    return jsonify(recommendations)

@app.route('/assign', methods=['POST'])
def assign_employee():
    data = request.json
    employee_id = data.get("employee_id")
    project_id = data.get("project_id")
    task_hours = data.get("task_hours")

    # Find the employee and project in the database
    employee = session.query(Employee).filter_by(id=employee_id).one()
    project = session.query(Project).filter_by(id=project_id).one()

    # Create a new EmployeeProjects entry
    assignment = EmployeeProjects(
        employee_id=employee.id,
        project_id=project.id,
        total_hours=task_hours,
        hours_working=0,
        hours_available=task_hours,
        utilization=0.0
    )

    # Add and commit the new assignment
    session.add(assignment)
    session.commit()

    return jsonify({"message": "Employee assigned successfully"})

if __name__ == '__main__':
    app.run(debug=True)
