from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

class MathGame:
    def __init__(self):
        self.numbers = []
        self.operation = '+'
        self.difficulty = 'easy'

    def generate_numbers(self):
        count = 2 if self.difficulty == 'easy' else 3
        self.numbers = [random.randint(1, 10) for _ in range(count)]
        return self.numbers

    def calculate_correct_answer(self):
        result = self.numbers[0]
        for num in self.numbers[1:]:
            if self.operation == '+':
                result += num
            elif self.operation == '-':
                result -= num
            elif self.operation == '×':
                result *= num
            elif self.operation == '÷':
                result /= num
        return result

game = MathGame()

@app.route('/')
def index():
    game.generate_numbers()
    return render_template('index.html', 
                         numbers=game.numbers, 
                         operation=game.operation,
                         difficulty=game.difficulty)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = float(request.json.get('answer', 0))
    correct_answer = game.calculate_correct_answer()
    is_correct = abs(user_answer - correct_answer) < 0.01
    return jsonify({'correct': is_correct, 'correct_answer': correct_answer})

@app.route('/update_operation', methods=['POST'])
def update_operation():
    game.operation = request.json.get('operation', '+')
    game.generate_numbers()
    return jsonify({'numbers': game.numbers})

@app.route('/update_difficulty', methods=['POST'])
def update_difficulty():
    game.difficulty = request.json.get('difficulty', 'easy')
    game.generate_numbers()
    return jsonify({'numbers': game.numbers})

if __name__ == '__main__':
    app.run(debug=True) 