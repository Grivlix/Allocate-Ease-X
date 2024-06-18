from flask import Flask, render_template, request, jsonify
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from setup_db import Base, Employee, Skill, Project  # Ensure correct import path

app = Flask(__name__)

# Configure the database (This is just for demonstration, you can keep your actual setup)
#engine = create_engine('sqlite:///employees.db')
#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template("projects.html")

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    prompt = data.get("prompt")

    # Demo data
    employees = [
        {
            "image": "/static/images/John.png",
            "name": "John Doe",
            "currentRole": "Database Manager",
            "experience": "5 years",
            "availability": "40 hours/week",
            "skills": ["Python", "React", "SQL"],
            "previousProjects": ["Project Alpha", "Project Beta"]
        },
        {
            "image": "/static/images/Jane.png",
            "name": "Jane Smith",
            "currentRole": "Intermediate Website Developer",
            "experience": "3 years",
            "availability": "30 hours/week",
            "skills": ["Java", "C++", "HTML"],
            "previousProjects": ["Project Gamma", "Project Delta"]
        },
        {
            "image": "/static/images/Emily.png",
            "name": "Emily Johnson",
            "currentRole": "Senior Software Developer",
            "experience": "10 years",
            "availability": "15 hours/week",
            "skills": ["C#", "JavaScript", "CSS"],
            "previousProjects": ["Project Epsilon", "Project Zeta"]
        }
    ]

    # Simulated response based on the prompt (simple logic for demonstration)
    top_rec = employees[0]
    others = employees[1:]

    recommendations = {"top": top_rec, "others": others}

    return jsonify(recommendations)


if __name__ == '__main__':
    app.run(debug=True)
