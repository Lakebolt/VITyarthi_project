"""
main.py - Main application launcher.
Imports and coordinates the 3 modules: storage, display, and booking.
"""

import sys
import storage
import display
import booking


def main():
    data = storage.load_data()

    while True:
        print("\n" + "#" * 45)
        print("    🎬 MOVIE TICKET BOOKING SYSTEM 🎬")
        print("#" * 45)
        print("1. View Movies & Showtimes")
        print("2. Check Seat Availability Map")11
        print("3. Book Movie Ticket(s)")
        print("4. Cancel a Booking")
        print("5. Search Ticket by Booking ID")
        print("6. Exit")
        print("#" * 45)

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            display.show_now_playing(data["movies"])
        elif choice == "2":
            display.show_now_playing(data["movies"])
            m_id = input("\nEnter Movie ID to view seat map: ").strip()
            if m_id in data["movies"]:
                print(f"\n--- {data['movies'][m_id]['title']} Seat Map ---")
                display.render_seats(data["movies"][m_id])
            else:
                print("[!] Invalid Movie ID.")
        elif choice == "3":
            booking.reserve_seats(data)
        elif choice == "4":
            booking.cancel_booking(data)
        elif choice == "5":
            booking.view_ticket_details(data)
        elif choice == "6":
            print("\nThank you for using the Movie Ticket Booking System! Goodbye.\n")
            sys.exit(0)
        else:
            print("[!] Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()