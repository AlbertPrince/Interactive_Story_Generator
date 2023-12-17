# app.py

import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from openai import OpenAI

app = Flask(__name__)

# Configure your PostgreSQL database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy extension
db = SQLAlchemy(app)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Define your model
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)



# user_age = input("Enter your age: ")
# user_background = input("Describe your background: ")
# user_skills = input("List your skills: ")

story = {
    'user': {
        'age': 25,
        'background': 'Mechanic',
        'skills': 'Can fix and upgrade mechanical parts. Can also craft weapons and tools'
    },
    'characters': {
        'sister1': {'age': 26, 'background': 'Medical student', 'skills': 'Basic medical knowledge'},
        'sister2': {'age': 23, 'background': 'Computer programmer', 'skills': 'Technical expertise'},
        'little_brother': {'age': 10, 'background': 'Student', 'skills': 'Agility and curiosity'}
    },
    'scene': "City of Shadows",
    'objectives': [
        "Gather Supplies",
        "Plan the Route",
        "Navigate the Streets",
        "Survival Choices"
    ],
    'current_objective_index': 0
}

def present_choices(choices):
    print("Choose one:")
    for i, choice in enumerate(choices, start=1):
        print(f"{i}. {choice}")

def handle_user_choice():
    choices = ["Option 1", "Option 2"]  # Replace with actual choices
    present_choices(choices)
    user_choice = int(input("Enter your choice (1 or 2): "))
    
    # Update story based on user's choice
    if story['current_objective_index'] == 0:  # Gather Supplies
        handle_gather_supplies_choice(user_choice)
    elif story['current_objective_index'] == 1:  # Plan the Route
        handle_plan_route_choice(user_choice)
    # Add similar logic for other objectives...


# Example: Main loop to drive the story
def main_story_loop():
    while not end_of_story:
        choices = get_available_choices()  # Implement this function to get current choices
        present_choices(choices)
        user_choice = int(input("Enter your choice: "))
        outcome = handle_user_choice(user_choice)
        print(outcome)

def generate_story_element(prompt):
    response = client.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=150
    )
    return response['choices'][0]['text']


# Routes
@app.route('/')
def index():
    return jsonify({'message': 'Hello, this is your Flask backend with PostgreSQL!'})




@app.route('/generate_story', methods=['POST'])
def generate_story(prompt):
    data = request.get_json()
    # Implement story generation logic based on data
    # response = client.Completion.create(
    #     engine="text-davinci-002",  # Choose the GPT-3 engine
    #     prompt=prompt,
    #     max_tokens=500,  # Adjust as needed
    #     temperature=0.7,  # Adjust for creativity vs. coherence
    #     n = 1  # Number of responses to generate
    # )
    response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)

    return response.choices[0].text.strip()

    # Example: Save data to PostgreSQL
    new_story = Story(title=data['title'], content=data['content'])
    db.session.add(new_story)
    db.session.commit()

    return jsonify({'message': 'Story generated successfully!'})

if __name__ == '__main__':
    # Create database tables before running the app
    db.create_all()
    
    # Run the Flask app
    app.run(debug=True)
