QUESTIONS = [
    {
        "question": "Can an unassigned open ticket move directly to in_progress?",
        "options": {
            "A": "Yes, every open ticket can move directly",
            "B": "No, the ticket must be assigned first",
            "C": "Only if its priority is low",
            "D": "Only if it has a note",
        },
        "answer": "B",
        "explanation": (
            "The workflow requires a ticket to be assigned before it "
            "can move into in_progress."
        ),
    },
    {
        "question": "What should the resolution percentage be when there are no tickets?",
        "options": {
            "A": "100%",
            "B": "An error caused by division by zero",
            "C": "0%",
            "D": "50%",
        },
        "answer": "C",
        "explanation": (
            "An empty ticket collection should be handled safely and "
            "should not cause division by zero."
        ),
    },
    {
        "question": "When searching by category and status, how are the filters combined?",
        "options": {
            "A": "OR: either filter must match",
            "B": "AND: both filters must match",
            "C": "Only the category is used",
            "D": "Only the status is used",
        },
        "answer": "B",
        "explanation": (
            "Combining category and status with AND returns tickets "
            "that match both selected filters."
        ),
    },
    {
        "question": "Can a resolved ticket receive a note immediately?",
        "options": {
            "A": "Yes, without any restrictions",
            "B": "Only if the ticket is critical",
            "C": "No, it must be reopened first",
            "D": "Only if it has no assigned staff member",
        },
        "answer": "C",
        "explanation": (
            "The workflow requires a resolved ticket to be reopened "
            "before a new note can be added."
        ),
    },
    {
        "question": "What should happen if a JSON file contains a duplicate ticket ID?",
        "options": {
            "A": "Silently delete the older ticket",
            "B": "Change the duplicate ID automatically",
            "C": "Reject the invalid data without modifying the in-memory tickets",
            "D": "Ignore all validation",
        },
        "answer": "C",
        "explanation": (
            "Duplicate IDs should be rejected so ticket identity remains "
            "consistent and existing in-memory data is not changed."
        ),
    },
    {
        "question": "A pull request changes validation rules but has no negative tests. What is the main concern?",
        "options": {
            "A": "The program will always run more slowly",
            "B": "Invalid inputs may not be properly rejected",
            "C": "The README will be deleted",
            "D": "Git will refuse to merge the branch",
        },
        "answer": "B",
        "explanation": (
            "Negative tests check that invalid input is rejected and "
            "help prevent validation regressions."
        ),
    },
]
