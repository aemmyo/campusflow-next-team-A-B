from campusflow.tickets import create_ticket, find_ticket
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import assign_ticket, update_ticket_status

from campusflow.queue import (
    get_open_tickets,
    sort_tickets_by_priority,
)

from campusflow.reports import (
    get_ticket_summary,
    count_tickets_by_status,
    count_tickets_by_priority,
    count_tickets_by_category,
    count_assignment_status,
)


DATA_FILE = "data/tickets.json"


def load_saved_tickets():
    """Load tickets safely when the application starts."""
    try:
        tickets = load_tickets(DATA_FILE)
        print(f"Loaded {len(tickets)} saved tickets.")
        return tickets

    except FileNotFoundError:
        print("No saved tickets found. Starting with an empty collection.")
        return []

    except (ValueError, OSError) as error:
        print(f"Could not load tickets: {error}")
        return None


def create_new_ticket(tickets):
    """Collect information and create a new ticket."""
    title = input("Title: ").strip()

    category = input(
        "Category (Network/Hardware/Software/Other): "
    ).strip()

    urgency = input("Urgency (low/medium/high): ").strip()

    try:
        affected_users = int(input("Affected users: "))

        ticket = create_ticket(
            tickets,
            title,
            category,
            urgency,
            affected_users,
        )

        print(
            f"Created {ticket['id']} "
            f"with priority {ticket['priority']}."
        )

    except (ValueError, TypeError) as error:
        print(f"Error: {error}")


def list_tickets(tickets):
    """Display all tickets."""
    if not tickets:
        print("No tickets found.")
        return

    print("\n=== ALL TICKETS ===")

    for ticket in tickets:
        print(
            f"{ticket['id']} | "
            f"{ticket['title']} | "
            f"{ticket['priority']} | "
            f"{ticket['status']} | "
            f"assigned={ticket.get('assigned_to')}"
        )


def view_ticket(tickets):
    """Display details for one ticket."""
    ticket_id = input("Ticket ID: ").strip()

    try:
        ticket = find_ticket(tickets, ticket_id)

        if ticket:
            print("\n=== TICKET DETAILS ===")

            for key, value in ticket.items():
                print(f"{key}: {value}")
        else:
            print("Ticket not found.")

    except (ValueError, TypeError, KeyError) as error:
        print(f"Error: {error}")


def assign_existing_ticket(tickets):
    """Assign a ticket to a staff member."""
    ticket_id = input("Ticket ID: ").strip()
    staff = input("Assign to: ").strip()

    try:
        assign_ticket(tickets, ticket_id, staff)
        print(f"Ticket {ticket_id} assigned to {staff}.")

    except (ValueError, TypeError, KeyError) as error:
        print(f"Error: {error}")


def change_ticket_status(tickets):
    """Update the status of a ticket."""
    ticket_id = input("Ticket ID: ").strip()

    status = input(
        "New status (open/in_progress/resolved): "
    ).strip()

    try:
        update_ticket_status(tickets, ticket_id, status)
        print(f"Ticket {ticket_id} status updated.")

    except (ValueError, TypeError, KeyError) as error:
        print(f"Error: {error}")


def show_priority_queue(tickets):
    """Display open tickets sorted by priority."""
    try:
        open_tickets = get_open_tickets(tickets)
        sorted_tickets = sort_tickets_by_priority(open_tickets)

        print(
            f"\n=== OPEN PRIORITY QUEUE "
            f"({len(sorted_tickets)} tickets) ==="
        )

        if not sorted_tickets:
            print("No open tickets.")
            return

        for ticket in sorted_tickets:
            print(
                f"{ticket['priority'].upper():8} | "
                f"{ticket['id']} | "
                f"{ticket['title']} | "
                f"{ticket['affected_users']} users"
            )

    except (ValueError, TypeError, KeyError) as error:
        print(f"Could not display queue: {error}")


def show_reports(tickets):
    """Display ticket statistics and reports."""
    try:
        print("\n=== CAMPUSFLOW REPORTS ===")
        print(f"Total tickets: {len(tickets)}")

        print(
            "By Status:",
            count_tickets_by_status(tickets),
        )

        print(
            "By Priority:",
            count_tickets_by_priority(tickets),
        )

        print(
            "By Category:",
            count_tickets_by_category(tickets),
        )

        print(
            "Assignment:",
            count_assignment_status(tickets),
        )

        print("\n=== SUMMARY ===")
        print(get_ticket_summary(tickets))

    except (ValueError, TypeError, KeyError) as error:
        print(f"Could not generate reports: {error}")


def save_and_exit(tickets):
    """Save tickets and report whether saving succeeded."""
    try:
        save_tickets(tickets, DATA_FILE)
        print(f"Saved {len(tickets)} tickets to {DATA_FILE}.")
        print("Goodbye!")
        return True

    except (OSError, ValueError, TypeError) as error:
        print(f"Could not save tickets: {error}")
        print("Your application is still running.")
        return False


def display_menu():
    """Display the main menu."""
    print("\n=== CAMPUSFLOW HELPDESK ===")
    print("1. Create ticket (F1)")
    print("2. List tickets (F2)")
    print("3. View ticket (F2)")
    print("4. Assign ticket (F3)")
    print("5. Update status (F4)")
    print("6. Show priority queue (F5)")
    print("7. Reports (F6)")
    print("8. Save & Exit (F7)")


def main():
    """Run the CampusFlow application."""
    tickets = load_saved_tickets()

    # Stop if the existing ticket file could not be loaded safely.
    if tickets is None:
        return

    while True:
        display_menu()
        choice = input("Choice: ").strip()

        if choice == "1":
            create_new_ticket(tickets)

        elif choice == "2":
            list_tickets(tickets)

        elif choice == "3":
            view_ticket(tickets)

        elif choice == "4":
            assign_existing_ticket(tickets)

        elif choice == "5":
            change_ticket_status(tickets)

        elif choice == "6":
            show_priority_queue(tickets)

        elif choice == "7":
            show_reports(tickets)

        elif choice == "8":
            if save_and_exit(tickets):
                break

        else:
            print("Invalid choice. Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()