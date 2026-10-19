from campusflow.quiz_questions import QUESTIONS


def calculate_score(answers):
    """Return the number of correct answers."""
    score = 0

    for question, answer in zip(QUESTIONS, answers):
        if answer.upper() == question["answer"]:
            score += 1

    return score


def run_quiz():
    """Collect all answers, then display results and learning notes."""
    answers = []
    learning_notes = []

    print("\n=== ENGINEERING UNDERSTANDING CHECK ===")
    print("Choose A, B, C, or D for each question.")
    print("Your results will be displayed after all six questions.\n")

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\nQuestion {number}: {question['question']}")

        for letter, option in question["options"].items():
            print(f"  {letter}. {option}")

        while True:
            answer = input("Your answer (A/B/C/D): ").strip().upper()

            if answer in question["options"]:
                answers.append(answer)
                break

            print("Invalid choice. Please enter A, B, C, or D.")

        if number in (2, 5):
            explanation = input(
                "Explain in your own words why your answer is correct: "
            ).strip()

            while not explanation:
                print("Please provide an explanation.")
                explanation = input("Your explanation: ").strip()

            learning_notes.append(
                {
                    "question": number,
                    "explanation": explanation,
                }
            )

    score = calculate_score(answers)

    print("\n=== QUIZ RESULTS ===")
    print(f"Your score: {score}/{len(QUESTIONS)}")

    for number, (question, answer) in enumerate(
        zip(QUESTIONS, answers), start=1
    ):
        print(f"\nQuestion {number}")
        print(f"Your answer: {answer}")
        print(f"Correct answer: {question['answer']}")
        print(f"Explanation: {question['explanation']}")

        if answer == question["answer"]:
            print("Result: Correct")
        else:
            print("Result: Incorrect")

    print("\n=== YOUR LEARNING NOTES ===")

    for note in learning_notes:
        print(f"Question {note['question']}: {note['explanation']}")

    print("\nUse these learning notes in your AI learning log.")
