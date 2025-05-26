import os
import random

class Question:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer.lower()

    def ask_question(self, number):
        print(f"\nQuestion {number}: {self.question}")
        for option in sorted(self.choices):
            print(f"{option}) {self.choices[option]}")

        while True:
            user_input = input("Your answer (a/b/c/d): ").lower()
            if user_input in self.choices:
                return user_input == self.answer
            else:
                print("Invalid input. Please enter a, b, c, or d.")

class QuizLoader:
    def __init__(self, base_path="Quizzes"):
        self.base_path = base_path

    def list_categories(self):
        return [category for category in os.listdir(self.base_path)
                if os.path.isdir(os.path.join(self.base_path, category))]
   
    def list_quizzes(self, category):
        category_path = os.path.join(self.base_path, category)
        return [file for file in os.listdir(category_path) if file.endswith(".txt")]

    def load_questions(self, filepath):
        questions = []
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                blocks = file.read().split("################")
                for block in blocks:
                    lines = block.strip().split("\n")
                    if len(lines) < 6:
                        continue
                    question_text = lines[0].replace("Question: ", "")
                    choices = {line[0]: line[3:] for line in lines[1:5] if line[1] == ")"}
                    answer = lines[5].replace("Answer: ", "").strip().lower()
                    questions.append(Question(question_text, choices, answer))
            return questions
        except Exception as e:
            print(f"Error loading questions: {e}")
            return []

class QuizRunner:
    def __init__(self, questions):
        self.questions = questions

    def start(self):
        random.shuffle(self.questions)
        score = 0
        for i, question in enumerate(self.questions, 1):
            if question.ask(i):
                score += 1
        print(f"\nQuiz Complete! Your score: {score} / {len(self.questions)}")

class QuizPlayer:
    def __init__(self):
        self.loader = QuizLoader()

    def run(self):
        if not os.path.exists(self.loader.base_path):
            print("No quizzes available.")
            return

        categories = self.loader.list_categories()
        if not categories:
            print("No categories found.")
            return

        print("\nCategories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")

        try:
            category_index = int(input("\nSelect a category by number: ")) - 1
            selected_category = categories[category_index]
        except (ValueError, IndexError):
            print("Invalid category selection.")
            return

        quizzes = self.loader.list_quizzes(selected_category)
        if not quizzes:
            print("No quiz files in this category.")
            return

        print(f"\nAvailable Quizzes in '{selected_category}':")
        for i, quiz in enumerate(quizzes, 1):
            print(f"{i}. {quiz}")

        try:
            quiz_index = int(input("\nSelect a quiz file by number: ")) - 1
            selected_quiz = quizzes[quiz_index]
        except (ValueError, IndexError):
            print("Invalid quiz file selection.")
            return

        quiz_path = os.path.join(self.loader.base_path, selected_category, selected_quiz)
        questions = self.loader.load_questions(quiz_path)

        if questions:
            runner = QuizRunner(questions)
            runner.start()
        else:
            print("No valid questions found.")
