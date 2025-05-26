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