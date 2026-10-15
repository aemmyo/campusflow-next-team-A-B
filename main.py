from campusflow.tickets import create_ticket, find_ticket
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import assign_ticket, update_ticket_status
from campusflow.queue import (
    get_open_tickets,
    get_assigned_tickets,
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


def main():
    # Load saved tickets when the application starts.
    try:
        tickets = load_tickets(DATA_FILE)
    except FileNotFoundError:
        tickets = []
        print("No saved tickets found. Starting with an empty collection.")
    except (ValueError, OSError) as error:
        print(f"Could not load tickets: {error}")
        return

    print("=== CampusFlow Helpdesk - Final Project F1-F7 ===")

    while True:
        print("\n1. Create ticket (F1)")
        print("2. List tickets (F2)")
        print("3. View ticket (F2)")
        print("4. Assign ticket (F3)")
        print("5. Update status (F4)")
        print("6. Show priority queue (F5)")
        print("7. Reports (F6)")
        print("8. Save & Exit (F7)")

        choice = input("Choice: ").strip()

        # F1: Create a ticket.
        if choice == "1":
            title = input("Title: ").strip()
            category = input(
                "Category (Network/Hardware/Software/Other): "
            ).strip()
            urgency = input("Urgency (low/medium/high): ").strip()

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

            except Exception as error:
                print(f"Could not create ticket: {error}")

        # F2: List all tickets.
        elif choice == "2":
            if not tickets:
                print("No tickets found.")
            else:
                print("\n=== ALL TICKETS ===")

                for ticket in tickets:
                    print(
                        f"{ticket['id']} | "
                        f"{ticket['title']} | "
                        f"{ticket['priority']} | "
                        f"{ticket['status']} | "
                        f"assigned={ticket.get('assigned_to')}"
                    )

        # F2: View one ticket.
        elif choice == "3":
            ticket_id = input("Ticket ID: ").strip()

            try:
                ticket = find_ticket(tickets, ticket_id)

                if ticket:
                    print("\n=== TICKET DETAILS ===")

                    for key, value in ticket.items():
                        print(f"{key}: {value}")
                else:
                    print("Ticket not found.")

            except (ValueError, TypeError) as error:
                print(f"Error: {error}")

        # F3: Assign a ticket.
        elif choice == "4":
            ticket_id = input("Ticket ID: ").strip()
            staff = input("Assign to: ").strip()

            try:
                assign_ticket(tickets, ticket_id, staff)
                print(f"Ticket {ticket_id} assigned to {staff}.")

            except (ValueError, TypeError, KeyError) as error:
                print(f"Error: {error}")

            except Exception as error:
                print(f"Could not assign ticket: {error}")

        # F4: Update ticket status.
        elif choice == "5":
            ticket_id = input("Ticket ID: ").strip()
            status = input(
                "New status (open/in_progress/resolved): "
            ).strip()

            try:
                update_ticket_status(tickets, ticket_id, status)
                print(f"Ticket {ticket_id} status updated.")

            except (ValueError, TypeError, KeyError) as error:
                print(f"Error: {error}")

            except Exception as error:
                print(f"Could not update status: {error}")

        # F5: Show the open priority queue.
        elif choice == "6":
            try:
                open_tickets = get_open_tickets(tickets)
                sorted_tickets = sort_tickets_by_priority(open_tickets)

                print(
                    f"\n--- OPEN QUEUE "
                    f"({len(sorted_tickets)} tickets) ---"
                )

                if not sorted_tickets:
                    print("No open tickets.")
                else:
                    for ticket in sorted_tickets:
                        print(
                            f"{ticket['priority'].upper():8} | "
                            f"{ticket['id']} | "
                            f"{ticket['title']} | "
                            f"{ticket['affected_users']} users"
                        )

            except (ValueError, TypeError, KeyError) as error:
                print(f"Could not display queue: {error}")

        # F6: Display reports.
        elif choice == "7":
            try:
                print("\n=== REPORTS (F6) ===")
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

                print("\nSummary:")
                print(get_ticket_summary(tickets))

            except (ValueError, TypeError, KeyError) as error:
                print(f"Could not generate reports: {error}")

        # F7: Save tickets and exit.
        elif choice == "8":
            try:
                save_tickets(tickets, DATA_FILE)
                print(
                    f"Saved {len(tickets)} tickets "
                    f"to {DATA_FILE}. Goodbye!"
                )
                break

            except (OSError, ValueError, TypeError) as error:
                print(f"Could not save tickets: {error}")
                print("Your application is still running.")

        # Handle invalid menu choices.
        else:
            print("Invalid choice. Enter a number from 1 to 8.")


if __name__ == "__main__":
    main()