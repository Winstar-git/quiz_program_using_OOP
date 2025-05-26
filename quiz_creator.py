import os

class Question:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices  
        self.answer = answer.lower()

    def preview(self):
        print("\nPreview:")
        print(self.question)
        for option in ['a', 'b', 'c', 'd']:
            print(f"{option}) {self.choices.get(option)}")
        print(f"Correct Answer: {self.answer.upper()}")
    
    def to_text(self): 
        output = [f"Question: {self.question}"]
        for option in ['a', 'b', 'c', 'd']:
            output.append(f"{option}) {self.choices[option]}")
        output.append(f"Answer: {self.answer.upper()}")
        output.append("################\n")
        return '\n'.join(output)
    
class Quiz:
    def __init__(self, category, filename):
        self.category = category
        self.filename = filename
        self.questions = []
        self.file_path = self._create_path()

    def _create_path(self):
        folder = os.path.join("Quizzes", self.category)
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, self.filename + ".txt")

    def save_question(self, question):
        try:
            with open(self.file_path, 'a', encoding="utf-8") as text:
                text.write(question.to_text())
            print("Question saved successfully.\n")
        except Exception as e:
            print(f"Error saving question: {e}")

class Creator:
    def __init__(self):
        self.quiz = None

    def create_question(self):
        question = input("\nEnter your question: ")
        choices = {}
        for option in ['a', 'b', 'c', 'd']:
            choices[option] = input(f"Choice {option}: ")

        while True:
            answer = input("Enter correct answer (a/b/c/d): ").lower()
            if answer in ['a', 'b', 'c', 'd']:
                break
            else:
                print("Invalid input. Please enter a, b, c, or d only.")
        
        return Question(question, choices, answer)
    
    def start(self):
        category = input("Enter quiz category: ")
        filename = input("Enter quiz filename (without .txt): ")
        self.quiz = Quiz(category, filename)

        while True:
            question = self.create_question()
            question.preview()

            save = input("Save this question? (y/n): ").lower()
            if save == 'y':
                self.quiz.save_question(question)
                self.quiz.questions.append(question)
            else:
                print("Question not saved.")

            another = input("Would you like to add another question? (y/n): ").lower()
            if another != 'y':
                break