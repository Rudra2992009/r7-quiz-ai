PRE_MADE_QUESTIONS = {
    "10th": {
        "Math": [
            "What is the value of π?",
            "Solve for x: 2x + 3 = 15.",
            "Define a prime number.",
            "What is the area of a circle with radius 5 cm?",
            "Explain Pythagoras theorem.",
            "What is a linear equation?",
            "Convert 25% to a fraction.",
            "What is the sum of angles in a triangle?",
            "Calculate the perimeter of a square with side 4 cm.",
            "Define a composite number."
        ],
        "Science": [
            "What are the three states of matter?",
            "Define photosynthesis.",
            "What is the function of the heart?",
            "Explain Newton's first law of motion.",
            "What is an atom?",
            "Define the water cycle.",
            "What is the importance of the ozone layer?",
            "Name the human body's five senses.",
            "What is DNA?",
            "Explain the greenhouse effect."
        ]
    },
    "12th": {
        "Math": [
            "Define a differential equation.",
            "Explain the binomial theorem.",
            "What is integration by parts?",
            "State the fundamental theorem of calculus.",
            "Define a matrix.",
            "What is the determinant of a square matrix?",
            "Explain Laplace transform.",
            "What is a vector space?",
            "Solve for x in a quadratic equation.",
            "What is a scalar product?"
        ],
        "Physics": [
            "State Newton's second law of motion.",
            "What is kinetic energy?",
            "Define work done.",
            "Explain the laws of thermodynamics.",
            "What is Hooke's law?",
            "Define acceleration.",
            "What is momentum?",
            "Explain the principle of conservation of energy.",
            "What is gravitational force?",
            "State Ohm's law."
        ]
    }
}

from flask import request

@app.route('/premade', methods=['POST'])
def premade():
    data = request.get_json() or {}
    class_ = data.get('class', '10th').lower()
    subject = data.get('subject', '').title()
    questions = PRE_MADE_QUESTIONS.get(class_, {}).get(subject, [])
    if not questions:
        questions = ["No pre-made questions available for this class and subject."]
    return jsonify(questions)
