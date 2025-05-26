import os
import random
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from colorama import Fore, Style, init

init(autoreset=True)
console = Console()

ascii_art = """
 ██████╗ ██╗   ██╗██╗███████╗
██╔═══██╗██║   ██║██║╚══███╔╝
██║   ██║██║   ██║██║  ███╔╝ 
██║▄▄ ██║██║   ██║██║ ███╔╝  
╚██████╔╝╚██████╔╝██║███████╗
 ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝"""

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

    def ask_question(self, number):
        question_text = f"[bold yellow]Question {number}:[/bold yellow] {self.question}\n"
        for option in sorted(self.choices):
            question_text += f"[cyan]{option})[/cyan] {self.choices[option]}\n"

        console.print(Panel.fit(Text.from_markup(question_text.strip()), border_style="magenta"))

        while True:
            user_input = input(Fore.GREEN + "👉 Your answer (a/b/c/d): " + Style.RESET_ALL).lower()
            if user_input in self.choices:
                return user_input == self.answer
            else:
                print(Fore.RED + "❌ Invalid input. Please enter a, b, c, or d.")

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
            console.print(f"[bold red]❌ Error loading questions: {e}[/bold red]")
            return []

class QuizRunner:
    def __init__(self, questions):
        self.questions = questions

    def start(self):
        random.shuffle(self.questions)
        score = 0
        for i, question in enumerate(self.questions, 1):
            if question.ask_question(i):
                score += 1
        console.print(f"\n[bold cyan]🏁 Quiz Complete![/bold cyan]")
        console.print(f"[bold green]🎯 Your score: {score} / {len(self.questions)}[/bold green]")

class QuizPlayer:
    def __init__(self):
        self.loader = QuizLoader()

    def run(self):
        console.print(Panel.fit(ascii_art.strip(), border_style="bright_red"))
        loading("Booting Quiz Creator")
        typewriter("Welcome to Quiz Player!\n")

        if not os.path.exists(self.loader.base_path):
            console.print("[bold red]❌ No quizzes available. Make sure the 'Quizzes' folder exists.[/bold red]")
            return

        categories = self.loader.list_categories()
        if not categories:
            console.print("[bold red]❌ No quiz categories found.[/bold red]")
            return

        print("\nAvailable Categories:")
        for i, category in enumerate(categories, 1):
            print(Fore.YELLOW + f"{i}. {category}")

        try:
            category_index = int(input(Fore.CYAN + "\n🎯 Select a category by number: " + Style.RESET_ALL)) - 1
            selected_category = categories[category_index]
        except (ValueError, IndexError):
            print(Fore.RED + "❌ Invalid category selection.")
            return

        quizzes = self.loader.list_quizzes(selected_category)
        if not quizzes:
            print(Fore.RED + "❌ No quiz files in this category.")
            return

        print(Fore.BLUE + f"\n📚 Quizzes in '{selected_category}':")
        for i, quiz in enumerate(quizzes, 1):
            print(Fore.GREEN + f"{i}. {quiz}")

        try:
            quiz_index = int(input(Fore.CYAN + "\n🗂️  Select a quiz file by number: " + Style.RESET_ALL)) - 1
            selected_quiz = quizzes[quiz_index]
        except (ValueError, IndexError):
            print(Fore.RED + "❌ Invalid quiz file selection.")
            return

        quiz_path = os.path.join(self.loader.base_path, selected_category, selected_quiz)
        questions = self.loader.load_questions(quiz_path)

        if questions:
            runner = QuizRunner(questions)
            runner.start()
        else:
            print(Fore.RED + "❌ No valid questions found.")

if __name__ == "__main__":
    player = QuizPlayer()
    player.run()
