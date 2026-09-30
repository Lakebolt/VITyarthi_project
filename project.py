"""
Movie Ticket Booking System (CLI)
Features:
- View Available Movies & Showtimes
- Visual Seat Layout Map (Available vs. Booked)
- Multi-seat Booking with Input Validation
- Automated Pricing Calculation with Taxes & Itemized Bill
- Booking Cancellation & Seat Release
- Ticket Lookup by Booking ID
- Persistent Storage via Local JSON File
"""

import json
import os
import random
import sys
from datetime import datetime

DATA_FILE ="theatre_data.json"
TAX_RATE = 0.05 # 5% convenience / entertainment tax

# Initial mock data for movies and 5x8 seat layouts
DEFAULT_MOVIES = {
    "1": {
        "title": "MARVEL: IRON MAN ",
        "genre": "Sci-Fi/Action",
        "duration": " 2h 6m",
        "price": 300.00,
        "rows": 6,
        "cols": 7,
        "booked_seats": ["A1", "A2", "C4"]
    },
    "2": {
        "title": "FORD V FERRARI",
        "genre": "Sport/Action",
        "duration": "2h 32m",
        "price": 290.00,
        "rows": 8,
        "cols": 5,
        "booked_seats": ["E1", "E2", "E3"]
    },
    "3": {
        "title": "MISSION IMPOSSIBLE",
        "genre": "Action/Thriller",
        "duration": "1h 50m",
        "price": 250.00,
        "rows": 4,
        "cols": 7,
        "booked_seats": ["C1", "C4", "C7"]
    },
    "4": {
        "title": "THE PURSUIT OF HAPPYNESS",
        "genre": "Melodrama/Drama",
        "duration": "1h 57m",
        "price": 225.00,
        "rows": 7,
        "cols": 6,
        "booked_seats": ["B3", "D5"]
    }
}


def load_data(): 
    
    #Load movie and booking data from a JSON file.
    
    if not os.path.exists(DATA_FILE):
        data = {
            "movies": DEFAULT_MOVIES,
            "bookings": {}
        }
        save_data(data)
        return data

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("[!] Error loading data file. Resetting to defaults.")
        data = {"movies": DEFAULT_MOVIES, "bookings": {}}
        save_data(data)
        return data


def save_data(data): 
    
    #Save current state to the JSON file.
    
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def show_now_playing(movies):
    
    #Display all currently playing movies.
    
    print("\n" + "=" * 65)
    print(f"{'ID':<4} {'Movie Title':<20} {'Genre':<18} {'Duration':<12} {'Price'}")
    print("=" * 65)
    for movie_id, info in movies.items():
        print(f"[{movie_id}]  {info['title']:<20} {info['genre']:<18} {info['duration']:<12}  ₹{info['price']:.2f}")
    print("=" * 65)


def render_seats(movie_info):
    
    #Print an interactive 2D grid representation of seats.
    
    rows = movie_info["rows"]
    cols = movie_info["cols"]
    booked = set(movie_info["booked_seats"])

    print("\n" + " " * 12 + "------ SCREEN THIS WAY ------")
    print(" " * 6 + " ".join([f" {c} " for c in range(1, cols + 1)]))

    for r in range(rows):
        row_letter = chr(ord('A') + r)
        row_display = []
        for c in range(1, cols + 1):
            seat_code = f"{row_letter}{c}"
            if seat_code in booked:
                row_display.append("[X]")  # Booked
            else:
                row_display.append("[O]")  # Available
        print(f"  {row_letter}   " + " ".join(row_display))

    print("\nLegend:  [O] = Available    [X] = Booked")
    total_seats = rows * cols
    available_seats = total_seats - len(booked)
    print(f"Available Seats: {available_seats}/{total_seats}")


def get_total_price(ticket_price, seat_count):
    
    #Compute base cost, taxes, and total amount.
    
    subtotal = ticket_price * seat_count
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    return round(subtotal, 2), round(tax, 2), round(total, 2)


def issue_booking_id():
    
    #Generate a random 6-character booking reference code.
    
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "TKT-" + "".join(random.choice(chars) for _ in range(6))


def reserve_seats(data):
    
    #Handle seat reservation and bill generation.
    
    movies = data["movies"]
    show_now_playing(movies)

    choice = input("\nEnter Movie ID to book (or '0' to return): ").strip()
    if choice == "0":
        return
    if choice not in movies:
        print("[!] Invalid Movie ID. Returning to main menu.")
        return

    movie = movies[choice]
    print(f"\nSelected: {movie['title']} (${movie['price']:.2f} per ticket)")
    show_now_playing(movie)

    customer_name = input("\nEnter Customer Name: ").strip()
    if not customer_name:
        print("[!] Customer name cannot be empty.")
        return

    customer_phone = input("Enter Contact Number: ").strip()
    if not customer_phone.isdigit() or len(customer_phone) < 7:
        print("[!] Please enter a valid phone number (at least 7 digits).")
        return

    seats_input = input("Enter seat code(s) separated by commas (e.g. A3, A4): ").strip().upper()
    requested_seats = [s.strip() for s in seats_input.split(",") if s.strip()]

    if not requested_seats:
        print("[!] No seats selected.")
        return

    # Validate seat bounds and availability
    
    valid_rows = [chr(ord('A') + r) for r in range(movie["rows"])]
    valid_cols = list(range(1, movie["cols"] + 1))
    booked_set = set(movie["reserve_seats"])

    invalid_seats = []
    already_booked = []

    for s in requested_seats:
        if len(s) < 2 or s[0] not in valid_rows or not s[1:].isdigit() or int(s[1:]) not in valid_cols:
            invalid_seats.append(s)
        elif s in booked_set:
            already_booked.append(s)

    if invalid_seats:
        print(f"[!] Invalid seat format/out of bounds: {', '.join(invalid_seats)}")
        return
    if already_booked:
        print(f"[!] Seat(s) already occupied: {', '.join(already_booked)}")
        return
    if len(requested_seats) != len(set(requested_seats)):
        print("[!] Duplicate seats detected in input.")
        return

    # Calculate pricing 
    
    subtotal, tax, total = get_total_price(movie["price"], len(requested_seats))

    # Print Invoice / Receipt
    booking_id =issue_booking_id()
    print("\n" + "=" * 45)
    print("           BOOKING CONFIRMATION")
    print("=" * 45)
    print(f"Booking ID   : {booking_id}")
    print(f"Customer     : {customer_name} ({customer_phone})")
    print(f"Movie        : {movie['title']}")
    print(f"Seats        : {', '.join(requested_seats)} (Count: {len(requested_seats)})")
    print(f"Subtotal     :  ₹{subtotal:.2f}")
    print(f"Tax (8%)     :  ₹{tax:.2f}")
    print(f"Total Amount :  ₹{total:.2f}")
    print(f"Date & Time  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 45)

    confirm = input("Confirm and complete payment? (y/n): ").strip().lower()
    if confirm == "y":
        
        # Update movie booked seats
        movie["reserve_seats"].extend(requested_seats)

        # Store booking record
        
        data["bookings"][booking_id] = {
            "booking_id": booking_id,
            "movie_id": choice,
            "movie_title": movie["title"],
            "customer_name": customer_name,
            "phone": customer_phone,
            "seats": requested_seats,
            "subtotal": subtotal,
            "tax": tax,
            "total_paid": total,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_data(data)
        print("\n[✔] Tickets booked successfully! Save your Booking ID.")
    else:
        print("\n[x] Booking cancelled by user.")


def cancel_booking(data):
    #Handle booking cancellation and release reserved seats.
    
    booking_id = input("\nEnter Booking ID to cancel (e.g. TKT-XXXXXX): ").strip().upper()

    if booking_id not in data["bookings"]:
        print("[!] Booking ID not found. Please verify and try again.")
        return

    booking = data["bookings"][booking_id]
    print("\n" + "-" * 40)
    print(f"Found Booking : {booking_id}")
    print(f"Customer      : {booking['customer_name']}")
    print(f"Movie         : {booking['movie_title']}")
    print(f"Seats         : {', '.join(booking['seats'])}")
    print(f"Refund Amount :  ₹{booking['total_paid']:.2f}")
    print("-" * 40)

    confirm = input("Are you sure you want to cancel this booking? (y/n): ").strip().lower()
    if confirm == "y":
 
        # Free up the seats from the movie
 
        movie_id = booking["movie_id"]
        if movie_id in data["movies"]:
            current_seats = data["movies"][movie_id]["booked_seats"]
            for s in booking["seats"]:
                if s in current_seats:
                    current_seats.remove(s)

        # Remove from active bookings
 
        del data["bookings"][booking_id]
        save_data(data)
        print(f"\n[✔] Booking {booking_id} cancelled successfully.")
        print(f"[✔] Refund of  ₹{booking['total_paid']:.2f} initiated.")
    else:
        print("\n[x] Cancellation aborted.")


def view_ticket_details(data):
    #Look up a booking by ID.
    
    booking_id = input("\nEnter Booking ID to look up: ").strip().upper()
    if booking_id not in data["bookings"]:
        print("[!] No records found for this Booking ID.")
        return

    b = data["bookings"][booking_id]
    print("\n" + "=" * 40)
    print("             TICKET DETAILS")
    print("=" * 40)
    print(f"Booking ID   : {b['booking_id']}")
    print(f"Customer     : {b['customer_name']}")
    print(f"Phone        : {b['phone']}")
    print(f"Movie        : {b['movie_title']}")
    print(f"Seats        : {', '.join(b['seats'])}")
    print(f"Total Paid   :  ₹{b['total_paid']:.2f}")
    print(f"Booked On    : {b['timestamp']}")
    print("=" * 40)


def main():
    #Main CLI driver menu.
    
    data = load_data()

    while True:
        print("\n" + "#" * 45)
        print("    🎬 MOVIE TICKET BOOKING SYSTEM 🎬")
        print("#" * 45)
        print("1. View Movies & Showtimes")
        print("2. Check Seat Availability Map")
        print("3. Book Movie Ticket(s)")
        print("4. Cancel a Booking")
        print("5. Search Ticket by Booking ID")
        print("6. Exit")
        print("#" * 45)

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            show_now_playing(data["movies"])
        elif choice == "2":
            show_now_playing(data["movies"])
            m_id = input("\nEnter Movie ID to view seat map: ").strip()
            if m_id in data["movies"]:
                print(f"\n--- {data['movies'][m_id]['title']} Seat Map ---")
                render_seats(data["movies"][m_id])
            else:
                print("[!] Invalid Movie ID.")
        elif choice == "3":
            reserve_seats(data)
        elif choice == "4":
            cancel_booking(data)
        elif choice == "5":
            view_ticket_details(data)
        elif choice == "6":
            print("\nThank you for using the Movie Ticket Booking System! Goodbye.\n")
            sys.exit(0)
        else:
            print("[!] Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()