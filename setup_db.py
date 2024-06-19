from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    job_title = Column(String)
    department = Column(String)
    employment_type = Column(String)
    location = Column(String)
    contact_info = Column(String)
    image = Column(String)  # Added image column
    skills = relationship('Skill', back_populates='employee')
    availability = relationship('Availability', uselist=False, back_populates='employee')
    projects = relationship('EmployeeProjects', back_populates='employee')

class Skill(Base):
    __tablename__ = 'skill_table'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee_table.id'))
    skill_name = Column(String)
    proficiency_level = Column(String)
    last_updated = Column(DateTime)
    employee = relationship('Employee', back_populates='skills')

class Availability(Base):
    __tablename__ = 'availability_table'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee_table.id'))
    total_hours = Column(Integer)
    hours_working = Column(Integer)
    hours_available = Column(Integer)
    utilization = Column(Float)
    upcoming_leave = Column(String)
    employee = relationship('Employee', back_populates='availability')

class Project(Base):
    __tablename__ = 'project_table'
    id = Column(Integer, primary_key=True)
    project_name = Column(String)
    starting_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    description = Column(String)
    employees = relationship('EmployeeProjects', back_populates='project')

class EmployeeProjects(Base):
    __tablename__ = 'employee_projects_table'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee_table.id'))
    project_id = Column(Integer, ForeignKey('project_table.id'))
    total_hours = Column(Integer)
    hours_working = Column(Integer)
    hours_available = Column(Integer)
    utilization = Column(Float)
    employee = relationship('Employee', back_populates='projects')
    project = relationship('Project', back_populates='employees')

# Set up the database
def setup_db():
    engine = create_engine('sqlite:///employees.db')
    Base.metadata.create_all(engine)

# Add sample data
def add_sample_data():
    engine = create_engine('sqlite:///employees.db')
    Session = sessionmaker(bind=engine)
    session = Session()


    sample_employees = [
        Employee(
            name="Kiara Bohringer",
            job_title="Project Manager",
            department="Construction",
            employment_type="Full-time",
            location="New York, USA",
            contact_info="kiara@example.com",
            image="/static/images/kiara.png",
            skills=[
                Skill(skill_name="Project Management", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="Python", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0))
            ],
            availability=Availability(total_hours=35, hours_working=0, hours_available=35, utilization=0.0, upcoming_leave="None"),
            projects=[
                EmployeeProjects(project=Project(project_name="Construction Project A", starting_date=datetime(2023, 1, 1, 0, 0), end_date=datetime(2023, 6, 1, 0, 0), status="Completed", description="A construction project")),
                EmployeeProjects(project=Project(project_name="Robotics Project A", starting_date=datetime(2023, 7, 1, 0, 0), end_date=datetime(2023, 12, 1, 0, 0), status="Ongoing", description="A robotics project")),
                EmployeeProjects(project=Project(project_name="Defuser Project", starting_date=datetime(2023, 9, 1, 0, 0), end_date=datetime(2024, 3, 1, 0, 0), status="Ongoing", description="A defuser project"))
            ]
        ),
        Employee(
            name="Erik Torsten",
            job_title="Software Engineer",
            department="IT",
            employment_type="Part-time",
            location="San Francisco, USA",
            contact_info="erik@example.com",
            image="/static/images/erik.png",
            skills=[
                Skill(skill_name="Java", proficiency_level="Proficient", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="Python", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="Project Management", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0))
            ],
            availability=Availability(total_hours=20, hours_working=5, hours_available=15, utilization=0.25, upcoming_leave="July 15-22"),
            projects=[
                EmployeeProjects(project=Project(project_name="Roadwork Project Z", starting_date=datetime(2023, 1, 1, 0, 0), end_date=datetime(2023, 6, 1, 0, 0), status="Completed", description="A roadwork project")),
                EmployeeProjects(project=Project(project_name="Construction Project A", starting_date=datetime(2023, 7, 1, 0, 0), end_date=datetime(2023, 12, 1, 0, 0), status="Ongoing", description="A construction project")),
                EmployeeProjects(project=Project(project_name="Robotics Project A", starting_date=datetime(2023, 9, 1, 0, 0), end_date=datetime(2024, 3, 1, 0, 0), status="Ongoing", description="A robotics project")),
                EmployeeProjects(project=Project(project_name="Defuser Project", starting_date=datetime(2024, 1, 1, 0, 0), end_date=datetime(2024, 6, 1, 0, 0), status="Ongoing", description="A defuser project"))
            ]
        ),
        Employee(
            name="Aamir Cypher",
            job_title="Data Analyst",
            department="Analytics",
            employment_type="Full-time",
            location="Chicago, USA",
            contact_info="aamir@example.com",
            image="/static/images/cypher.png",
            skills=[
                Skill(skill_name="Data Analysis", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="Python", proficiency_level="Proficient", last_updated=datetime(2023, 1, 1, 0, 0))
            ],
            availability=Availability(total_hours=40, hours_working=20, hours_available=20, utilization=0.5, upcoming_leave="August 10-20"),
            projects=[
                EmployeeProjects(project=Project(project_name="Architecture Project A", starting_date=datetime(2023, 1, 1, 0, 0), end_date=datetime(2023, 6, 1, 0, 0), status="Completed", description="An architecture project")),
                EmployeeProjects(project=Project(project_name="Data Analysis Project B", starting_date=datetime(2023, 7, 1, 0, 0), end_date=datetime(2023, 12, 1, 0, 0), status="Ongoing", description="A data analysis project"))
            ]
        ),
        Employee(
            name="Sophia Mendez",
            job_title="UX Designer",
            department="Design",
            employment_type="Contractor",
            location="Los Angeles, USA",
            contact_info="sophia@example.com",
            image="/static/images/sophia.png",
            skills=[
                Skill(skill_name="UX Design", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="Adobe XD", proficiency_level="Advanced", last_updated=datetime(2023, 1, 1, 0, 0))
            ],
            availability=Availability(total_hours=30, hours_working=24, hours_available=6, utilization=0.8, upcoming_leave="September 5-12"),
            projects=[
                EmployeeProjects(project=Project(project_name="App Redesign Project", starting_date=datetime(2023, 1, 1, 0, 0), end_date=datetime(2023, 6, 1, 0, 0), status="Completed", description="An app redesign project")),
                EmployeeProjects(project=Project(project_name="Website Design Project C", starting_date=datetime(2023, 7, 1, 0, 0), end_date=datetime(2023, 12, 1, 0, 0), status="Ongoing", description="A website design project"))
            ]
        ),
        Employee(
            name="Michael Johnson",
            job_title="Network Engineer",
            department="IT",
            employment_type="Full-time",
            location="Miami, USA",
            contact_info="michael@example.com",
            image="/static/images/Michel.png",
            skills=[
                Skill(skill_name="Network Security", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="Cisco Networking", proficiency_level="Advanced", last_updated=datetime(2023, 1, 1, 0, 0))
            ],
            availability=Availability(total_hours=40, hours_working=42, hours_available=-2, utilization=1.05, upcoming_leave="October 1-10"),
            projects=[
                EmployeeProjects(project=Project(project_name="Network Upgrade Project", starting_date=datetime(2023, 1, 1, 0, 0), end_date=datetime(2023, 6, 1, 0, 0), status="Completed", description="A network upgrade project")),
                EmployeeProjects(project=Project(project_name="Security Enhancement Project", starting_date=datetime(2023, 7, 1, 0, 0), end_date=datetime(2023, 12, 1, 0, 0), status="Ongoing", description="A security enhancement project"))
            ]
        ),
        Employee(
            name="John Doe",
            job_title="Database Manager",
            department="IT",
            employment_type="Full-time",
            location="New York, USA",
            contact_info="john@example.com",
            image="static/images/John.png",
            skills=[
                Skill(skill_name="Python", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="React", proficiency_level="Proficient", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="SQL", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0))
            ],
            availability=Availability(total_hours=40, hours_working=40, hours_available=0, utilization=1.0, upcoming_leave="None"),
            projects=[
                EmployeeProjects(project=Project(project_name="Project Alpha", starting_date=datetime(2023, 1, 1, 0, 0), end_date=datetime(2023, 6, 1, 0, 0), status="Completed", description="Project Alpha")),
                EmployeeProjects(project=Project(project_name="Project Beta", starting_date=datetime(2023, 7, 1, 0, 0), end_date=datetime(2023, 12, 1, 0, 0), status="Ongoing", description="Project Beta"))
            ]
        ),
        Employee(
            name="Jane Smith",
            job_title="Intermediate Website Developer",
            department="IT",
            employment_type="Part-time",
            location="San Francisco, USA",
            contact_info="jane@example.com",
            image="static/images/Jane.png",
            skills=[
                Skill(skill_name="Java", proficiency_level="Proficient", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="C++", proficiency_level="Proficient", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="HTML", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0))
            ],
            availability=Availability(total_hours=30, hours_working=30, hours_available=0, utilization=1.0, upcoming_leave="None"),
            projects=[
                EmployeeProjects(project=Project(project_name="Project Gamma", starting_date=datetime(2023, 1, 1, 0, 0), end_date=datetime(2023, 6, 1, 0, 0), status="Completed", description="Project Gamma")),
                EmployeeProjects(project=Project(project_name="Project Delta", starting_date=datetime(2023, 7, 1, 0, 0), end_date=datetime(2023, 12, 1, 0, 0), status="Ongoing", description="Project Delta"))
            ]
        ),
        Employee(
            name="Emily Johnson",
            job_title="Senior Software Developer",
            department="IT",
            employment_type="Full-time",
            location="Chicago, USA",
            contact_info="emily@example.com",
            image="static/images/Emily.png",
            skills=[
                Skill(skill_name="C#", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="JavaScript", proficiency_level="Expert", last_updated=datetime(2023, 1, 1, 0, 0)),
                Skill(skill_name="CSS", proficiency_level="Proficient", last_updated=datetime(2023, 1, 1, 0, 0))
            ],
            availability=Availability(total_hours=40, hours_working=15, hours_available=25, utilization=0.375, upcoming_leave="None"),
            projects=[
                EmployeeProjects(project=Project(project_name="Project Epsilon", starting_date=datetime(2023, 1, 1, 0, 0), end_date=datetime(2023, 6, 1, 0, 0), status="Completed", description="Project Epsilon")),
                EmployeeProjects(project=Project(project_name="Project Zeta", starting_date=datetime(2023, 7, 1, 0, 0), end_date=datetime(2023, 12, 1, 0, 0), status="Ongoing", description="Project Zeta"))
            ]
        )
    ]

    session.add_all(sample_employees)
    session.commit()

if __name__ == '__main__':
    setup_db()
    add_sample_data()
