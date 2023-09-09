"""
This is a simple Python project using builtin libraries that generates a flash card application.
It has two game modes, each with two options "Type" and "Click":
 - Flashcards (Specific Dialogue AND Event Order)
 - Multiple Choice (Just Event Order)

If you check the Jesus lines box, all lines for Jesus will be included as potential questions.
NOTE: This does not affect Multiple Choice.

User Notes:
You can update the knowledge base in a text editor like Notepad.


Code Notes:
 - Mode1 is "Flashcards"
 - Mode2 is "Multiple Choice"

"""
import tkinter as tk
from tkinter import *

import random


class MarkDramaFlashcards:
    def __init__(self, root, _dialogue, _events):
        self.questions = dict()
        self.dialogue = _dialogue
        self.random_question = None
        self.random_part = None
        self.events = _events
        self.root = root
        self.root.title("Mark Drama Game")
        self.root.geometry("800x600")  # Set default window size
        self.parts_to_include = []
        self.create_title_screen()
        self.load_mode2_correct_answers()  # Load correct answers for Mode 2
        self.score = dict()
        self.reset_score()

        # Initialize everything else as per PEP-8 style guide (well, almost everything)
        self.feedback_text_frame = None
        self.mode2_answer_buttons = None
        self.mode2_question_number = None
        self.mode2_correct_answer = None
        self.score_label = None

        self.mode2_window = None
        self.mode2_question_label = None
        self.next_question_button = None
        self.correct_button = None
        self.wrong_button = None
        self.mode1_feedback_text = None
        self.mode1_entry = None
        self.mode1_question_label = None
        self.mode1_window = None
        self.mode1_correct_answer = None
        self.mode1_user_answer = None
        self.mode1_question = None
        self.mode1_next_button = None
        self.selected_dialogue = None
        self.selected_parts = None

    def reset_score(self):
        self.score = {"correct": 0, "total": 0}  # Initialize score

    def update_score_label(self):
        self.score_label.config(text=f"Score for this Session: {self.score['correct']}/{self.score['total']} correct")

    # ---------------------------------------------------------------------------------------------------------------- #
    # Title Screen Starts Here

    def create_title_screen(self):
        title_label = tk.Label(self.root, text="Mark Drama Learning", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)  # Add padding for separation

        mode_frame = tk.Frame(self.root)
        mode_frame.pack()

        mode1_button = tk.Button(mode_frame, text="Flashcards", font=("Helvetica", 16), command=self.start_mode1)
        mode1_button.pack(side=tk.LEFT, padx=20)  # Add side and padding for separation

        mode2_button = tk.Button(mode_frame, text="Multiple Choice", font=("Helvetica", 16), command=self.start_mode2)
        mode2_button.pack(side=tk.LEFT, padx=20)  # Add side and padding for separation

        # Create a frame for the checkboxes
        checkboxes_frame = tk.Frame(self.root)
        checkboxes_frame.pack()

        # Checkbox for "Jesus Dialogue" in italics
        jesus_mode_var = tk.IntVar()
        jesus_mode_checkbox = tk.Checkbutton(checkboxes_frame, text="Jesus Dialogue", font=("Helvetica", 12, "italic"),
                                             variable=jesus_mode_var)
        jesus_mode_checkbox.grid(row=0, column=0, padx=10)  # Grid layout for the first checkbox

        # Checkbox for "Pharisee Dialogue" in italics
        pharisee_mode = tk.IntVar()
        pharisee_mode_checkbox = tk.Checkbutton(checkboxes_frame, text="Pharisee Dialogue",
                                                font=("Helvetica", 12, "italic"), variable=pharisee_mode)
        pharisee_mode_checkbox.grid(row=0, column=1, padx=10)  # Grid layout for the second checkbox

        divider = tk.Frame(self.root, height=2, bg="black")
        divider.pack(fill=tk.X, padx=20, pady=10)  # Divider below the buttons

        # Create a frame for checkboxes
        # Create a LabelFrame to enclose the checkbox frame
        checkbox_label_frame = tk.LabelFrame(self.root, text="Parts to Include", font=("Helvetica", 14, "bold"))
        checkbox_label_frame.pack(padx=20, pady=10)

        # Place the checkboxes inside the LabelFrame
        for i in range(1, 4):
            checkbox = tk.Checkbutton(checkbox_label_frame, text=f"Part {i}", font=("Helvetica", 12, "bold"),
                                      command=lambda part=i: self.toggle_part(part))
            checkbox.grid(row=0, column=i - 1, padx=20, pady=5)  # Grid layout for the first row

        for i in range(4, 7):
            checkbox = tk.Checkbutton(checkbox_label_frame, text=f"Part {i}", font=("Helvetica", 12, "bold"),
                                      command=lambda part=i: self.toggle_part(part))
            checkbox.grid(row=1, column=i - 4, padx=20, pady=5)  # Grid layout for the second row

    def toggle_part(self, part_number):
        if part_number in self.parts_to_include:
            self.parts_to_include.remove(part_number)
        else:
            self.parts_to_include.append(part_number)

    def get_questions(self, mode=1):
        questions = dict()
        if not self.parts_to_include:
            print("No parts given, defaulting to the first 3 of them")
            self.parts_to_include = [1, 2, 3]
        mode_name = "Flashcards" if mode == 1 else "Multichoice"
        print(f"Launching {mode_name} with parts: {self.parts_to_include}")

        if mode == 1:
            for k in self.dialogue.keys():
                part_num = NUMBER_MAP[k]
                if part_num in self.parts_to_include:
                    questions[k] = self.dialogue[k]
        if mode == 2:
            for k in self.events.keys():
                part_num = NUMBER_MAP[k]
                if part_num in self.parts_to_include:
                    questions[k] = self.events[k]

        return questions

    # ---------------------------------------------------------------------------------------------------------------- #
    # Mode 1 Starts Here

    def reset_mode1(self):
        self.mode1_question = "This is a question."
        self.mode1_user_answer = tk.StringVar()
        self.mode1_user_answer.set("")
        self.mode1_correct_answer = "The correct answer has appeared."

    def start_mode1(self):
        self.questions = self.get_questions()
        self.reset_score()
        self.reset_mode1()
        self.create_mode1_window()

    def create_mode1_window(self):
        self.reset_score()
        self.mode1_window = Toplevel(self.root)
        self.mode1_window.title("Mark Drama Flashcards")
        self.mode1_window.geometry("800x800")  # Set default window size

        # Create a frame to hold widgets that use grid
        grid_frame = Frame(self.mode1_window)
        grid_frame.pack()

        # Add an empty column on the left for padding
        grid_frame.grid_columnconfigure(0, weight=1)

        self.mode1_question_label = Label(grid_frame, text="This is a question.", font=("Helvetica", 14))
        self.mode1_question_label.grid(row=0, column=1, pady=(10, 0), columnspan=2)

        self.mode1_entry = Text(grid_frame, font=("Helvetica", 12), wrap=WORD, height=6, width=60)
        self.mode1_entry.grid(row=1, column=1, pady=10, columnspan=2)

        self.reveal_answer_button = Button(grid_frame, text="Reveal Answer", font=("Helvetica", 12),
                                      command=self.reveal_mode1_answer)
        self.reveal_answer_button.grid(row=2, column=1, pady=10, columnspan=2)

        self.mode1_feedback_text = Text(grid_frame, font=("Helvetica", 12), wrap=WORD, height=16, width=60)
        self.mode1_feedback_text.grid(row=4, column=1, pady=10, columnspan=2)

        # Create a scrollbar for the feedback text widget
        scrollbar = Scrollbar(grid_frame, command=self.mode1_feedback_text.yview)
        scrollbar.grid(row=4, column=3, sticky='ns')  # Place scrollbar next to text widget
        self.mode1_feedback_text.config(yscrollcommand=scrollbar.set)

        self.correct_button = Button(grid_frame, text="I got it right", font=("Helvetica", 12),
                                     command=self.correct_mode1_answer)
        self.correct_button.grid(row=5, column=1, padx=10)

        self.wrong_button = Button(grid_frame, text="I got it wrong", font=("Helvetica", 12),
                                   command=self.wrong_mode1_answer)
        self.wrong_button.grid(row=5, column=2, padx=10)

        self.mode1_next_button = Button(grid_frame, text="Next Question", font=("Helvetica", 12),
                                        command=self.update_mode1_question)
        self.mode1_next_button.grid(row=6, column=1, pady=10, columnspan=2)
        self.mode1_next_button.config(state=DISABLED)  # Initially disabled

        self.score_label = tk.Label(grid_frame, text="Score for this Session: 0/0 correct", font=("Helvetica", 14))
        self.score_label.grid(row=7, column=0, columnspan=2, pady=10)

        self.update_mode1_question()

    def reveal_mode1_answer(self):
        # Get the correct answer
        if self.random_question:
            answers = self.questions[self.random_part][self.random_question]
            correct_answer = ""
            for i in answers:
                correct_answer += f"{i}\n"
            if correct_answer[0].strip() == "":
                correct_answer = ["Entry is blank, Jesus probably has no dialogue in this scene."]
        else:
            correct_answer = ["(Entry is Blank, does nothing happen?)"]

        # Clear the feedback field and set the correct answer
        self.mode1_feedback_text.config(state=tk.NORMAL)
        self.mode1_feedback_text.delete(1.0, tk.END)
        self.mode1_feedback_text.insert(tk.END, correct_answer)
        self.mode1_feedback_text.config(state=tk.DISABLED)

        # Enable "Right/Wrong" button after revealing the answer
        self.correct_button.config(state=tk.NORMAL)
        self.wrong_button.config(state=tk.NORMAL)
        self.reveal_answer_button.config(state=tk.DISABLED)

    def update_mode1_question(self):
        # Pick a Part
        self.random_part = random.choice(list(self.questions.keys()))
        # Generate a Question Based on Events in that Part
        the_question = self.questions[self.random_part]
        try:
            self.random_question = random.choice(list(the_question.keys()))
        except IndexError:
            print("This is causing trouble: ", the_question)
            exit()
        new_question = f"[{self.random_question}]" + \
                       "\n What does Jesus do here?"

        # Clear the user's input field and update the question
        self.mode1_entry.delete(1.0, tk.END)
        self.mode1_question_label.config(text=new_question)

        # Clear the feedback field
        self.mode1_feedback_text.config(state=tk.NORMAL)
        self.mode1_feedback_text.delete(1.0, tk.END)
        self.mode1_feedback_text.config(state=tk.DISABLED)

        # Disable "Next Question" button until a new answer is given
        self.mode1_next_button.config(state=tk.DISABLED)
        self.correct_button.config(state=tk.DISABLED)
        self.wrong_button.config(state=tk.DISABLED)
        self.reveal_answer_button.config(state=tk.NORMAL)

    def correct_mode1_answer(self):
        self.score["correct"] += 1
        self.score["total"] += 1
        self.mode1_next_button.config(state=tk.NORMAL)
        self.correct_button.config(state=tk.DISABLED)
        self.wrong_button.config(state=tk.DISABLED)
        self.update_score_label()

    def wrong_mode1_answer(self):
        self.score["total"] += 1
        self.mode1_next_button.config(state=tk.NORMAL)
        self.update_score_label()
        self.correct_button.config(state=tk.DISABLED)
        self.wrong_button.config(state=tk.DISABLED)

    # ---------------------------------------------------------------------------------------------------------------- #
    # Mode 2 Starts Here

    def load_mode2_correct_answers(self):
        self.mode2_correct_answers = {
            "1": "A",
            "2": "B",
            "3": "C",
            "4": "D",
            "5": "E",
            "6": "F",
            "7": "G",
            "8": "H",
        }

    def start_mode2(self):
        # Select a random question from the dictionary
        self.mode2_question_number = random.choice(list(self.mode2_correct_answers.keys()))
        self.mode2_correct_answer = self.mode2_correct_answers[self.mode2_question_number]
        self.questions = self.get_questions(mode=2)
        self.create_mode2_window()

    def create_mode2_window(self):
        self.mode2_window = tk.Toplevel(self.root)
        self.reset_score()
        self.mode2_window.title("Mark Drama Multi-Choice")
        self.mode2_window.geometry("800x480")  # Adjusted window size

        self.mode2_question_label = tk.Label(self.mode2_window,
                                             text=f"What comes after ERROR / BROKEN?",
                                             font=("Helvetica", 16))
        self.mode2_question_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Generate new answer options
        answer_options = list(self.mode2_correct_answers.values())
        random.shuffle(answer_options)

        # Ensure the correct answer is in the answer options
        if self.mode2_correct_answer not in answer_options:
            # Replace one of the random answers with the correct answer
            random_index = random.randint(0, 3)
            answer_options[random_index] = self.mode2_correct_answer

        self.mode2_answer_buttons = []

        for i in range(4):
            answer_button = tk.Button(self.mode2_window, text=answer_options[i], font=("Helvetica", 14),
                                      command=lambda ans=answer_options[i]: self.check_mode2_answer(ans), padx=80)
            answer_button.grid(row=i // 2 + 1, column=i % 2, padx=20, pady=10)
            self.mode2_answer_buttons.append(answer_button)

        # Text frame for answer feedback
        self.feedback_text_frame = tk.Text(self.mode2_window, font=("Helvetica", 8), wrap=tk.WORD, height=16, width=47)
        self.feedback_text_frame.grid(row=1, column=2, rowspan=3, padx=20, pady=10)

        # Create "Next Question" button
        self.next_question_button = tk.Button(self.mode2_window, text="Next Question", font=("Helvetica", 16),
                                              command=self.next_mode2_question)
        self.next_question_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.next_question_button.config(state=tk.DISABLED)  # Initially disabled

        # Create the Score Label
        self.score_label = tk.Label(self.mode2_window, text="Score for this Session: 0/0 correct",
                                    font=("Helvetica", 14))
        self.score_label.grid(row=5, column=0, columnspan=2, pady=10)
        self.update_mode2_question()

    def check_mode2_answer(self, user_answer):
        self.feedback_text_frame.config(state=tk.NORMAL)
        self.feedback_text_frame.delete(1.0, tk.END)  # Clear previous content

        if user_answer == self.mode2_correct_answer:
            feedback = random.choice(["You got it!", "Correct!"] * 3 +
                                     ["10 points to Gryffindor!", "Yay!", "Woo-hoo!"])
            self.feedback_text_frame.insert(tk.END, feedback, "green")
            self.score["correct"] += 1  # Increment correct score
        else:
            feedback_wrong = random.choice(["Don't stop, you can do it!\n", "Don't give up!\n",
                                            "Time for a cookie?\n"] + [""]*10)
            feedback_correct = self.mode2_correct_answer
            self.feedback_text_frame.insert(tk.END, f"'{user_answer}' is incorrect.\n", "red")
            self.feedback_text_frame.insert(tk.END, f'{feedback_wrong}', "red")
            self.feedback_text_frame.insert(tk.END, f"'{feedback_correct}' is the correct answer.", "green")

        # Update the performance record below the "Next Question" button
        self.score["total"] += 1  # Increment total questions
        self.update_score_label()

        self.feedback_text_frame.config(state=tk.DISABLED)
        self.feedback_text_frame.tag_configure("red", foreground="red")
        self.feedback_text_frame.tag_configure("green", foreground="green")

        # Enable "Next Question" button after an answer is given
        self.next_question_button.config(state=tk.NORMAL)

        # Disable these buttons
        for button in self.mode2_answer_buttons:
            button.config(state=tk.DISABLED)

    def next_mode2_question(self):
        # Select a new random question from the dictionary
        self.mode2_question_number = random.choice(list(self.mode2_correct_answers.keys()))
        self.mode2_correct_answer = self.mode2_correct_answers[self.mode2_question_number]

        # Enable answer buttons
        for button in self.mode2_answer_buttons:
            button.config(state=tk.NORMAL)
        self.update_mode2_question()

    def update_mode2_question(self):
        print(self.questions)
        # Pick a Part
        self.random_part = random.choice(list(self.questions.keys()))
        # Generate a Question Based on Events in that Part
        the_question = self.questions[self.random_part]
        self.random_question = random.choice(the_question)

        self.mode2_question_label.config(text=f"What comes after {self.random_question}?", fg="black")

        # Generate new answer options
        answer_options = list(self.mode2_correct_answers.values())[:4]
        #answer_options = the_question[:4]
        random.shuffle(answer_options)

        # Ensure the correct answer is in the answer options
        if self.mode2_correct_answer not in answer_options:
            # Replace one of the random answers with the correct answer
            random_index = random.randint(0, 3)
            answer_options[random_index] = self.mode2_correct_answer

        for i in range(4):
            self.mode2_answer_buttons[i].config(text=answer_options[i],
                                                command=lambda ans=answer_options[i]: self.check_mode2_answer(ans))

        self.feedback_text_frame.config(state=tk.NORMAL)
        self.feedback_text_frame.delete(1.0, tk.END)  # Clear previous content
        self.feedback_text_frame.config(state=tk.DISABLED)
        self.next_question_button.config(state=tk.DISABLED)  # Disable "Next Question" button for the new question


def parse_event_order_to_dict():
    # Take my event order notes and turn them into a dict.
    # Initialize an empty dictionary to store the entries
    entries = {}
    current_part = None  # Initialize a variable to keep track of the current part

    # Open the file for reading
    with open('mark_learning_event_order.txt', 'r') as file:
        for line in file:
            # Check if the line starts with "="
            if line.startswith('=') or not line.strip():
                # Ignore lines starting with "="
                continue
            # Check if the line starts with " -"
            elif line.startswith(' -'):
                # If it starts with " -", add it to the current part
                entries[current_part].append(line.strip()[2:])
            else:
                # If it doesn't start with " -", it's a new part
                current_part = line.replace(":", "").strip()
                entries[current_part] = []
    return entries


def parse_dialogue_to_dict():
    # Take my dialogue notes for Jesus and turn them into a dict.
    # Initialize an empty dictionary to store the entries
    entries = {}
    current_part = None
    current_event = None

    # Open the file for reading
    with open('mark_learning_dialogue.txt', 'r') as file:
        for line in file:
            # Check if the line starts with "=" or "#"
            if line.startswith('=') or not line.strip() or line.startswith("#"):
                # Ignore lines starting with "="
                continue
            # Check if the line starts with " -"
            elif line.startswith('['):
                # If it doesn't start with " -", it's a new part
                current_part = line.replace('[', "").replace(']', "").strip()
                entries[current_part] = {}
            elif line.startswith(' -') or line.startswith('-'):
                current_event = line.replace("-", "").strip()
                entries[current_part][current_event] = []
            else:
                # Its dialogue or event notes.
                if not line.startswith("*") and not line.startswith("'"):
                    # JC is Jesus Christ
                    line = "JC: " + line
                entries[current_part][current_event].append(line.strip())
    return entries


if __name__ == "__main__":
    NUMBER_MAP = {
        1: "Part One",
        2: "Part Two",
        3: "Part Three",
        4: "Part Four",
        5: "Part Five",
        6: "Part Six"
    }
    INVERTED_NUMBER_MAP = {v: k for k, v in NUMBER_MAP.items()}
    NUMBER_MAP = {**NUMBER_MAP, **INVERTED_NUMBER_MAP}

    events = parse_event_order_to_dict()
    dialogue = parse_dialogue_to_dict()
    _root = tk.Tk()
    game = MarkDramaFlashcards(_root, _dialogue=dialogue, _events=events)
    _root.mainloop()
