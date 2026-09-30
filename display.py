
#display.py - Module for printing tables, menus, and 2D seating grids.


def show_now_playing(movies):
    """Display all currently screening movies in a formatted table."""
    print("\n" + "=" * 65)
    print(f"{'ID':<4} {'Movie Title':<26} {'Genre':<16} {'Duration':<10} {'Price'}")
    print("=" * 65)
    for movie_id, info in movies.items():
        print(f"[{movie_id}]  {info['title']:<26} {info['genre']:<16} {info['duration']:<10} ₹{info['price']:.2f}")
    print("=" * 65)


def render_seats(movie_info):
    """Print an interactive 2D seating layout showing available vs. booked seats."""
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
                row_display.append("[X]")  # Occupied
            else:
                row_display.append("[O]")  # Vacant
        print(f"  {row_letter}   " + " ".join(row_display))

    print("\nLegend:  [O] = Available    [X] = Booked")
    total_seats = rows * cols
    available_seats = total_seats - len(booked)
    print(f"Available Seats: {available_seats}/{total_seats}")