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


@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    prompt = data.get("prompt")

    # Demo data
    employees = [
        {
            "name": "John Doe",
            "experience": "5 years",
            "availability": "40 hours/week",
            "skills": ["Python", "JavaScript", "SQL"],
            "previousProjects": ["Project Alpha", "Project Beta"]
        },
        {
            "name": "Jane Smith",
            "experience": "3 years",
            "availability": "30 hours/week",
            "skills": ["Java", "C++", "HTML"],
            "previousProjects": ["Project Gamma", "Project Delta"]
        },
        {
            "name": "Emily Johnson",
            "experience": "2 years",
            "availability": "20 hours/week",
            "skills": ["C#", "React", "CSS"],
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
