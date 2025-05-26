import os
import time
import sys
from colorama import Fore, Style, init
from rich.console import Console
from rich.panel import Panel

init(autoreset=True)
console = Console()

# ASCII Art Logo
ascii_art = """
 ██████╗ ██╗   ██╗██╗███████╗     ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗ 
██╔═══██╗██║   ██║██║╚══███╔╝    ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██║   ██║██║   ██║██║  ███╔╝     ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝
██║▄▄ ██║██║   ██║██║ ███╔╝      ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
╚██████╔╝╚██████╔╝██║███████╗    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
 ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
"""

def typewriter(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading(message="Loading", delay=2):
    with console.status(f"[bold green]{message}..."):
        time.sleep(delay)

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
    
    def add_question(self, question):
        self.questions.append(question)

    def save_question(self, question):
        try:
            with open(self.file_path, 'a', encoding="utf-8") as text:
                text.write(question.to_text())
            print(Fore.GREEN + "Question saved successfully.\n")
        except Exception as e:
            print(Fore.RED + f"Error saving question: {e}")

class Creator:
    def __init__(self):
        self.quiz = None

    def create_question(self):
        question = input(Fore.YELLOW + "\nEnter your question: " + Style.RESET_ALL)
        choices = {}
        for option in ['a', 'b', 'c', 'd']:
            choices[option] = input(Fore.CYAN + f"Choice {option}: " + Style.RESET_ALL)

        while True:
            answer = input(Fore.GREEN + "Enter correct answer (a/b/c/d): " + Style.RESET_ALL).lower()
            if answer in ['a', 'b', 'c', 'd']:
                break
            else:
                print(Fore.RED + "Invalid input. Please enter a, b, c, or d only.")
        
        return Question(question, choices, answer)
    
    def start(self):
        console.print(Panel.fit(ascii_art, border_style="cyan"))
        loading("Booting Quiz Creator")
        typewriter("🎉 Welcome to the Quiz Creator!\n")

        category = input(Fore.MAGENTA + "Enter quiz category: " + Style.RESET_ALL)
        filename = input(Fore.MAGENTA + "Enter quiz filename (without .txt): " + Style.RESET_ALL)
        self.quiz = Quiz(category, filename)

        while True:
            question = self.create_question()
            question.preview()

            save = input(Fore.YELLOW + "Save this question? (y/n): " + Style.RESET_ALL).lower()
            if save == 'y':
                self.quiz.save_question(question)
                self.quiz.add_question(question)
            else:
                print(Fore.RED + "Question not saved.")
            another = input(Fore.CYAN + "Would you like to add another question? (y/n): " + Style.RESET_ALL).lower()
            if another != 'y':
                print(Fore.GREEN + "Quiz creation finished.")
                break

if __name__ == "__main__":
    creator = Creator()
    creator.start()