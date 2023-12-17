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

storyPrelude = [
   {1 : "A city is plagued by a zom "},
]

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
