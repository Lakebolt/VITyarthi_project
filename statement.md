# Project Statement: Movie Ticket Booking System (CLI)

----

1. Problem Overview
Small cinema organizations often rely on physical labor for ticketing. This leads to various human mistakes, for example, duplicate seat reservations, incorrect bill composing, and so on. The purpose of this task is to create a command-line interface-based program that performs every action related to ticketing, starting with presenting the showtimes and completing with issuing the bill and cancellation.

----

2. Project Scope
The project includes the following:
-    Command line interface - the system must be usable via terminal only.
-    Movie catalog - the movie that is currently shown must be available in the system with such parameters as genre, length, date, cost, etc.
-    Display seat allocation - the 2D map of the auditorium with free and busy seats must be displayed with the ability to book the seats.
-    Ability to book tickets - the system allows booking of needed number of tickets taking into account the conditions of no duplicates.
-    Automatic billing - subtract amounts based on the tickets booked and entertainment tax.
-    Cancellation with releasing of booked seat - tickets can be cancelled via booking ID, and seats are released automatically.
-    Data persistence - all data about cinema and booking is saved at a JSON file

----

# Out-of-Scope:
- Online payment processing via the gateway (payment is simulated via terminal confirmation only).
- Graphical User Interface (GUI), as only CLI is expected for the automatic evaluation.
- Multi-threaded cloud synchronization.

----

 3. Target Users
- Box Office Operators / Cinema Staff: The clerks at the ticket counter use a fast keyboard interface to book and cancel tickets for customers.
- Cinema Customers: Customers coming to the cinema and using the self-service terminal for checking the available shows and booking their seats.
- Independent Cinémas Owners: Independent manages assisting theatre owners with a zero-maintenance reservation system not relying on external databases.

----

4. High-Level Features
- Real-Time Movie Catalog: Information regarding movie screening times, genres, running time, and original ticket price.
- 2D Visual Seat Layout: A terminal grid showing the row letters (A–E) and seat numbers.
- Smart Booking Engine: Seat code validation, prohibits booking already occupied seats, and the availability of multiple-seat booking using commas.
- Invoice & Receipt Generation: Structured invoice with customer’s details, movie name, seat numbers, taxes, and Booking ID ('TKT-XXXXXX').
- Cancellation & Instant Refund Calculation: Booking tracking by an ID.

Project Overview: Ticket Booking System for Cinema