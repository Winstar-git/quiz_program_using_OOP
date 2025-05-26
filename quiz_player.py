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