from campusflow.tickets import create_ticket, find_ticket, list_tickets
from campusflow.storage import load_tickets, save_tickets
from campusflow.workflow import assign_ticket, update_status
from campusflow.queue import get_open_tickets, sort_by_priority
from campusflow.reports import generate_report

def main():
    tickets = load_tickets()
    print("=== CampusFlow Helpdesk ===")
    
    while True:
        print("\n1. Create ticket (F1)")
        print("2. List tickets (F2)")
        print("3. View ticket (F2)")
        print("4. Assign ticket (F3)")
        print("5. Update status (F4)")
        print("6. Show priority queue (F5)")
        print("7. Reports (F6)")
        print("8. Save & Exit")
        
        choice = input("Choice: ").strip()
        
        if choice == "1":
            title = input("Title: ")
            category = input("Category (network/software/hardware/access/other): ")
            urgency = input("Urgency (low/medium/high): ")
            try:
                affected = int(input("Affected users: "))
                t = create_ticket(tickets, title, category, urgency, affected)
                print(f"Created {t['id']} priority={t['priority']}")
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "2":
            for t in list_tickets(tickets):
                print(f"{t['id']} | {t['title']} | {t['priority']} | {t['status']} | {t['assigned_to']}")
                
        elif choice == "3":
            tid = input("Ticket ID: ")
            t = find_ticket(tickets, tid)
            print(t if t else "Not found")
            
        elif choice == "4":
            tid = input("Ticket ID: ")
            staff = input("Assign to: ")
            try:
                assign_ticket(tickets, tid, staff)
                print("Assigned")
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "5":
            tid = input("Ticket ID: ")
            status = input("New status (open/in_progress/resolved): ")
            try:
                update_status(tickets, tid, status)
                print("Status updated")
            except Exception as e:
                print(f"Error: {e}")
                
        elif choice == "6":
            open_t = get_open_tickets(tickets)
            sorted_t = sort_by_priority(open_t)
            for t in sorted_t:
                print(f"{t['priority'].upper():8} | {t['id']} | {t['title']} | {t['affected_users']} users")
                
        elif choice == "7":
            report = generate_report(tickets)
            print(report)
            
        elif choice == "8":
            save_tickets(tickets)
            print(f"Saved {len(tickets)} tickets. Bye!")
            break

if __name__ == "__main__":
    main()
