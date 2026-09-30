
#booking.py - Module for pricing, ticket reservation, and cancellation logic.


import random
from datetime import datetime
import storage
import display

TAX_RATE = 0.05  # 5% entertainment tax


def get_total_price(ticket_price, seat_count):
    """Calculate base price, tax, and total bill."""
    subtotal = ticket_price * seat_count
    tax = subtotal * TAX_RATE
    total = subtotal + tax
    return round(subtotal, 2), round(tax, 2), round(total, 2)


def issue_booking_id():
    """Generate a unique 6-character booking code."""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return "TKT-" + "".join(random.choice(chars) for _ in range(6))


def reserve_seats(data):
    """Handle seat booking, validation, and payment confirmation."""
    movies = data["movies"]
    display.show_now_playing(movies)

    choice = input("\nEnter Movie ID to book (or '0' to return): ").strip()
    if choice == "0":
        return
    if choice not in movies:
        print("[!] Invalid Movie ID. Returning to main menu.")
        return

    movie = movies[choice]
    print(f"\nSelected: {movie['title']} (₹{movie['price']:.2f} per ticket)")
    display.render_seats(movie)

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

    # Check boundaries and availability
    valid_rows = [chr(ord('A') + r) for r in range(movie["rows"])]
    valid_cols = list(range(1, movie["cols"] + 1))
    booked_set = set(movie["booked_seats"])

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

    # Bill calculation
    subtotal, tax, total = get_total_price(movie["price"], len(requested_seats))
    booking_id = issue_booking_id()

    print("\n" + "=" * 45)
    print("           BOOKING CONFIRMATION")
    print("=" * 45)
    print(f"Booking ID   : {booking_id}")
    print(f"Customer     : {customer_name} ({customer_phone})")
    print(f"Movie        : {movie['title']}")
    print(f"Seats        : {', '.join(requested_seats)} (Count: {len(requested_seats)})")
    print(f"Subtotal     : ₹{subtotal:.2f}")
    print(f"Tax (5%)     : ₹{tax:.2f}")
    print(f"Total Amount : ₹{total:.2f}")
    print(f"Date & Time  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 45)

    confirm = input("Confirm and complete payment? (y/n): ").strip().lower()
    if confirm == "y":
        movie["booked_seats"].extend(requested_seats)
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
        storage.save_data(data)
        print("\n[✔] Tickets booked successfully! Save your Booking ID.")
    else:
        print("\n[x] Booking cancelled by user.")


def cancel_booking(data):
    """Handle booking cancellation and release reserved seats."""
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
    print(f"Refund Amount : ₹{booking['total_paid']:.2f}")
    print("-" * 40)

    confirm = input("Are you sure you want to cancel this booking? (y/n): ").strip().lower()
    if confirm == "y":
        movie_id = booking["movie_id"]
        if movie_id in data["movies"]:
            current_seats = data["movies"][movie_id]["booked_seats"]
            for s in booking["seats"]:
                if s in current_seats:
                    current_seats.remove(s)

        del data["bookings"][booking_id]
        storage.save_data(data)
        print(f"\n[✔] Booking {booking_id} cancelled successfully.")
        print(f"[✔] Refund of ₹{booking['total_paid']:.2f} initiated.")
    else:
        print("\n[x] Cancellation aborted.")


def view_ticket_details(data):
    """Look up ticket receipt by Booking ID."""
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
    print(f"Total Paid   : ₹{b['total_paid']:.2f}")
    print(f"Booked On    : {b['timestamp']}")
    print("=" * 40)