from campusflow.tickets import (
    create_ticket,
    find_ticket,
    PRIORITY_ORDER,
)

from campusflow.validation import ALLOWED_CATEGORIES
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import assign_ticket, update_ticket_status
from campusflow.notes import add_note, get_notes
from campusflow.quiz import run_quiz
from campusflow.queue import (
    get_open_tickets,
    get_assigned_tickets,
    sort_tickets_by_priority,
)
from campusflow.search import (
    search_tickets,
    sort_search_results_by_priority,
)
from campusflow.reports import (
    get_ticket_summary,
    count_tickets_by_status,
    count_tickets_by_priority,
    count_tickets_by_category,
    count_assignment_status,
)

DATA_FILE = "data/tickets.json"


ALLOWED_STATUSES = ["open", "in_progress", "resolved"]


def ask_filter(prompt, allowed_values):
    """Ask for an optional filter and retry invalid choices."""

    while True:
        value = input(prompt).strip().lower()

        # An empty answer means this filter is ignored.
        if not value:
            return ""

        if value in allowed_values:
            return value

        print(
            f"Invalid choice. Allowed values: "
            f"{', '.join(allowed_values)}"
        )
        print("Please try again, or press Enter to skip.")


def display_search_results(results):
    """Display the required ticket information."""

    if not results:
        print("No matching tickets found.")
        return

    print(f"\n--- SEARCH RESULTS ({len(results)} tickets) ---")

    for ticket in results:
        print(
            f"{ticket['id']} | "
            f"{ticket['title']} | "
            f"{ticket['category']} | "
            f"{ticket['priority']} | "
            f"{ticket['status']} | "
            f"assigned_to={ticket.get('assigned_to')}"
        )


def search_menu(tickets):
    """Collect search filters and display matching tickets."""

    print("\n=== SEARCH TICKETS ===")
    print("Leave a filter blank to ignore it.")

    title = input("Title contains: ").strip()

    category = ask_filter(
        f"Category ({'/'.join(ALLOWED_CATEGORIES)}): ",
        ALLOWED_CATEGORIES,
    )

    status = ask_filter(
        f"Status ({'/'.join(ALLOWED_STATUSES)}): ",
        ALLOWED_STATUSES,
    )

    priority = ask_filter(
        f"Priority ({'/'.join(PRIORITY_ORDER)}): ",
        list(PRIORITY_ORDER),
    )

    try:
        results = search_tickets(
            tickets,
            title=title,
            category=category,
            status=status,
            priority=priority,
        )

        if results:
            while True:
                choice = input(
                    "Sort results by priority? (yes/no): "
                ).strip().lower()

                if choice in ("yes", "y"):
                    results = sort_search_results_by_priority(results)
                    break

                if choice in ("no", "n"):
                    break

                print("Please enter yes or no.")

        display_search_results(results)

    except ValueError as error:
        print(f"Search error: {error}")


def add_note_menu(tickets):
    """Prompt the user to add a note to a ticket."""

    ticket_id = input("Enter ticket ID: ").strip()
    author = input("Enter your name: ")
    message = input("Enter your note (5–300 characters): ")

    try:
        note = add_note(tickets, ticket_id, author, message)
        print(f"Note {note['note_id']} added successfully.")

    except ValueError as error:
        print(f"Error: {error}")


def view_notes_menu(tickets):
    """Display notes belonging to a ticket."""

    ticket_id = input("Enter ticket ID: ").strip()

    try:
        notes = get_notes(tickets, ticket_id)

        if not notes:
            print("This ticket has no notes.")
            return

        print(f"\nNotes for ticket {ticket_id}:")

        for note in notes:
            print(f"\nNote ID: {note['note_id']}")
            print(f"Author: {note['author']}")
            print(f"Message: {note['message']}")

    except ValueError as error:
        print(f"Error: {error}")

        
def main():
    try:
        tickets = load_tickets(DATA_FILE)
    except FileNotFoundError:
        tickets = []

        print("=== CampusFlow Helpdesk ===")

    while True:
        print("\n1. Create ticket")
        print("2. List tickets")
        print("3. View ticket")
        print("4. Assign ticket")
        print("5. Update status")
        print("6. Show priority queue")
        print("7. Reports")
        print("8. Search tickets")
        print("9. Add a note")
        print("10. View ticket notes")
        print("11. Engineering Understanding Check")
        print("12. Save & Exit")

        choice = input("Choice: ").strip()

        if choice == "1":
            title = input("Title: ")
            category = input(
                "Category (network/software/hardware/other): "
            )
            urgency = input("Urgency (low/medium/high): ")

            try:
                affected = int(input("Affected users: "))

                ticket = create_ticket(
                    tickets,
                    title,
                    category,
                    urgency,
                    affected,
                )

                print(
                    f"Created {ticket['id']} "
                    f"priority={ticket['priority']}"
                )

            except (ValueError, TypeError) as error:
                print(f"Error: {error}")

        elif choice == "2":
            if not tickets:
                print("No tickets.")
            else:
                for ticket in tickets:
                    print(
                        f"{ticket['id']} | "
                        f"{ticket['title']} | "
                        f"{ticket['priority']} | "
                        f"{ticket['status']} | "
                        f"assigned={ticket.get('assigned_to')}"
                    )

        elif choice == "3":
            ticket_id = input("Ticket ID: ").strip()

            try:
                ticket = find_ticket(tickets, ticket_id)
                print(ticket if ticket else "Not found.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "4":
            ticket_id = input("Ticket ID: ").strip()
            staff = input("Assign to: ").strip()

            try:
                assign_ticket(tickets, ticket_id, staff)
                print("Ticket assigned successfully.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "5":
            ticket_id = input("Ticket ID: ").strip()
            status = input(
                "New status (open/in_progress/resolved): "
            ).strip()

            try:
                update_ticket_status(tickets, ticket_id, status)
                print("Status updated successfully.")
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "6":
            open_tickets = get_open_tickets(tickets)
            sorted_tickets = sort_tickets_by_priority(open_tickets)

            print(
                f"--- OPEN QUEUE ({len(sorted_tickets)} tickets) ---"
            )

            for ticket in sorted_tickets:
                print(
                    f"{ticket['priority'].upper():8} | "
                    f"{ticket['id']} | "
                    f"{ticket['title']} | "
                    f"{ticket['affected_users']} users"
                )

        elif choice == "7":
            print("\n=== REPORTS ===")
            print(f"Total: {len(tickets)}")
            print("By Status:", count_tickets_by_status(tickets))
            print("By Priority:", count_tickets_by_priority(tickets))
            print("By Category:", count_tickets_by_category(tickets))
            print("Assignment:", count_assignment_status(tickets))
            print("\nSummary:")
            print(get_ticket_summary(tickets))

        elif choice == "8":
            search_menu(tickets)

        elif choice == "9":
            add_note_menu(tickets)

        elif choice == "10":
            view_notes_menu(tickets)

        elif choice == "11":
            run_quiz()

        elif choice == "12":
            save_tickets(tickets, DATA_FILE)
            print(
                f"Saved {len(tickets)} tickets to "
                "data/tickets.json. Bye!"
            )
            break

        else:
            print(
                "Invalid menu choice. "
                "Please enter a number from 1 to 12."
            )


if __name__ == "__main__":
    main()