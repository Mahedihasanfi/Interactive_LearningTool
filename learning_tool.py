import json
import random
from datetime import datetime


class Question:
    def __init__(
        self,
        question_id,
        question_text,
        question_type,
        options=None,
        correct_answer=None,
        active=True,
        times_shown=0,
        times_correct=0,
    ):
        self.question_id = question_id
        self.question_text = question_text
        self.question_type = question_type
        self.options = options
        self.correct_answer = correct_answer
        self.active = active
        self.times_shown = times_shown
        self.times_correct = times_correct

    def check_answer(self, user_answer):
        if self.question_type == "quiz":
            return user_answer == self.correct_answer
        elif self.question_type == "free-form":
            return user_answer.lower() == self.correct_answer.lower()

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "active": self.active,
            "times_shown": self.times_shown,
            "times_correct": self.times_correct,
        }

    @staticmethod
    def from_dict(data):
        return Question(
            question_id=data["question_id"],
            question_text=data["question_text"],
            question_type=data["question_type"],
            options=data.get("options"),
            correct_answer=data.get("correct_answer"),
            active=data["active"],
            times_shown=data["times_shown"],
            times_correct=data["times_correct"],
        )


class LearningTool:
    def __init__(self):
        self.questions = []
        self.profiles = {}
        self.profile = ""

        self.load_questions()
        self.load_profiles()

    def load_questions(self):
        try:
            with open("questions.json", "r") as file:
                data = json.load(file)
                self.questions = [Question.from_dict(q) for q in data]
        except FileNotFoundError:
            # Creating an empty questions file incase not exist
            with open("questions.json", "w") as file:
                json.dump([], file)

    def save_questions(self):
        data = [q.to_dict() for q in self.questions]
        with open("questions.json", "w") as file:
            json.dump(data, file)

    def load_profiles(self):
        try:
            with open("profiles.json", "r") as file:
                self.profiles = json.load(file)
        except FileNotFoundError:
            # Creating an empty profiles file incase not exist
            with open("profiles.json", "w") as file:
                json.dump({}, file)

    def save_profiles(self):
        with open("profiles.json", "w") as file:
            json.dump(self.profiles, file)

    # Question Addition
    def add_question(self):
        print("Adding a question:")
        question_text = input("Enter the question text: ")
        question_type = input("Enter the question type (1 for quiz, 2 for free-form): ")

        if question_type == "1":  # Quiz question
            options = []
            num_options = int(input("Enter the number of answer options: "))
            for i in range(num_options):
                option = input(f"Enter option {i+1}: ")
                options.append(option)

            correct_answer = input("Enter the correct answer option number: ")
            question_id = len(self.questions) + 1
            self.questions.append(
                Question(question_id, question_text, "quiz", options, correct_answer)
            )

        elif question_type == "2":  # Free-form text question
            correct_answer = input("Enter the correct answer: ")
            question_id = len(self.questions) + 1
            self.questions.append(
                Question(
                    question_id,
                    question_text,
                    "free-form",
                    correct_answer=correct_answer,
                )
            )

        else:
            print("Invalid question type.")

        self.save_questions()

    # Defining Question as active or inactive
    def disable_enable_question(self):
        print(f"Avaiable Questions:")
        for questionid in self.questions:
            print(f"Question ID: {questionid.question_id}")
        question_id = int(
            input("Enter the ID of the question you want to disable/enable: ")
        )
        question = self.get_question_by_id(question_id)
        if question:
            print("Question Information:")
            print(f"ID: {question.question_id}")
            print(f"Question Text: {question.question_text}")
            print(f"Answer: {question.correct_answer}")
            action = input(
                "Enter 'disable' to disable the question or 'enable' to enable the question: "
            )
            if action == "disable":
                question.active = False
            elif action == "enable":
                question.active = True
            else:
                print("Invalid action.")
        else:
            print("Question not found.")

        self.save_questions()

    # Practise Mode Creation
    def practice_mode(self):
        if len(self.questions) < 5:
            print("Practice mode requires at least 5 questions.")
            return

        while True:
            practice_questions = [q for q in self.questions if q.active]

            if not practice_questions:
                print("No active questions available for practice.")
                return
            question = self.weighted_random_choice(practice_questions)
            print("\nwrite done to exit")
            print(f"Question: {question.question_text}")
            if question.question_type == "quiz":
                for i, option in enumerate(question.options, start=1):
                    print(f"{i}. {option}")
                user_answer = input("Select the correct option number: ")
            else:
                user_answer = input("Enter your answer: ")

            if question.check_answer(user_answer):
                print("Correct!")
                question.times_correct += 1
            if user_answer == "done":
                print("Bye from Practice Mode")
                return
            if not question.check_answer(user_answer):
                print("Incorrect.")
            question.times_shown += 1
            self.save_questions()

    def weighted_random_choice(self, questions):  
        # Questions: answered incorrectly will become more likely to appear
        weights = [1 / (q.times_correct + 1) for q in questions]
        return random.choices(questions, weights=weights)[0]

    # Test Mode Creation
    def test_mode(self):
        if len(self.questions) < 5:
            print("Test mode requires at least 5 questions.")
            return
        test_questions = [q for q in self.questions if q.active]
        if not test_questions:
            print("No active questions available for the test.")
            return
        num_questions = int(input("Enter the number of questions for the test: "))
        if num_questions > len(test_questions):
            print("Number of questions exceeds the available questions.")
            return

        random.shuffle(test_questions)
        test_questions = test_questions[:num_questions]

        score = 0
        for question in test_questions:
            print(f"\nQuestion ID: {question.question_id}")
            print(f"Question: {question.question_text}")
            if question.question_type == "quiz":
                for i, option in enumerate(question.options, start=1):
                    print(f"{i}. {option}")
                user_answer = input("Select the correct option number: ")
            else:
                user_answer = input("Enter your answer: ")

            if question.check_answer(user_answer):
                print("Correct!")
                score += 1
            else:
                print("Incorrect.")

        if self.profile in self.profiles:
            profile_stats = self.profiles[self.profile]
            profile_stats["Score"] = profile_stats.get("Score", 0) + score
            profile_stats["TotalQuestions"] = (
                profile_stats.get("TotalQuestions", 0) + num_questions
            )
            profile_stats["TimesCorrect"] = profile_stats.get("TimesCorrect", 0) + score
        else:
            self.profiles[self.profile] = {
                "Score": score,
                "TotalQuestions": num_questions,
                "TimesCorrect": score,
            }
        self.save_profiles()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = f"\nProfile: {self.profile}\nScore: {score}/{num_questions}\nTimestamp: {timestamp}"
        print(result)
        with open("results.txt", "a") as file:  # Creating test mode result file
            file.write(result + "\n")

    def get_question_by_id(self, question_id):
        for question in self.questions:
            if question.question_id == question_id:
                return question
        return None

    # Statistics Mode
    def view_statistics(self):
        print("Question Statistics:")
        for question in self.questions:
            print(f"Question ID: {question.question_id}")
            print(f"Question Text: {question.question_text}")
            print(f"Active: {question.active}")
            print(f"Times Shown (Practice): {question.times_shown}")
            if question.times_shown > 0:
                percentage = (question.times_correct / question.times_shown) * 100
                print(f"Percentage Correct: {percentage:.2f}%")
            else:
                print("Percentage Correct: 0%")
            print()

    # Profile selection
    def select_profile(self):
        profile = input("Enter profile name: ")
        if profile not in self.profiles:
            self.profiles[profile] = {}
        self.profile = profile
        self.save_profiles()

    # information based on individual profile
    def profile_statistics(self):
        if self.profile in self.profiles:
            profile_stats = self.profiles[self.profile]
            print("\nYour Personal Profile Statistics:")
            print(f"Profile: {self.profile}")
            print(f"Score: {profile_stats.get('Score', 0)}")
            print(f"Total Questions: {profile_stats.get('TotalQuestions', 0)}")
            print(f"Times Correct: {profile_stats.get('TimesCorrect', 0)}")

    # Tool play
    def start(self):
        print("Welcome to the Interactive Learning Tool!")
        self.select_profile()

        while True:
            print("\nMenu:")
            print("1. Adding questions")
            print("2. Disable/Enable questions")
            print("3. Practice Mode")
            print("4. Test Mode")
            print("5. Application Statistics viewing")
            print("6. Profile Select")
            print("7. Individual profile data")
            print("0. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.add_question()
            elif choice == "2":
                self.disable_enable_question()
            elif choice == "3":
                self.practice_mode()
            elif choice == "4":
                self.test_mode()
            elif choice == "5":
                self.view_statistics()
            elif choice == "6":
                self.select_profile()
            elif choice == "7":
                self.profile_statistics()
            elif choice == "0":
                print("Bye from this Learning Tool")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    learning_tool = LearningTool()
    learning_tool.start()
