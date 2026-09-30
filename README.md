# VITyarthi_project
Movie Ticket Booking System

 # Movie Ticket Booking System (CLI)

This project is a modular command-line-based Python program executed for the cinema reservation management. Users can browse their favorite movies and check live seating charts. Users are offered the option to book several seats with an auto-calculation of tax and may also cancel their reservation with the help of a unique Booking ID.

---

1. OVERVIEW OF THE PROJECT

*Movie Ticket Booking System* is created as an interactive terminal-based application. The project demonstrates Python-based concepts, such as modular programming (decoupling of the software into three modules), I/O (using JSON file format), data validation, and generating a bill.

---

2. FEATURES

- **Movie Catalog Displays**:    Displays the list of currently screened movies, genres, duration of the films, and ticket prices in INR (Indian Rupees).
- **Seating Chart Display**:     Dynamic matrix that shows a 2D terminal grid of available (marked as `[O]`) and booked seats (marked as `[X]`).
- **Seats Booking & Validation**:
  - Booking of several seats at once.
  - Prevention of double booking and wrong input of seat boundaries.
- **Automated Billing**:         The program performs the calculations of the total price of tickets, applies 5% of entertainment tax, and indicates the earnings.
- **Cancellation of Booking**:   Means of cancellation by unique Booking
-  **Search for the Ticket**:    Allows you to search for your reservation history with the use of the reference number.
- **Data Persistence**:          Saves the information in the `theatre_data.json` file. This way, the reservation status will remain saved after each execution of                                  the project.
---

3. TECNOLOGIES/ TOOLS USED

- **Programming Language Used**:
  - Python version 3.8 or later.
- **Custom Modular Structure (Architecture)**:
  - `main.py`: Driver of the application.
  - `storage.py`: Responsible for storing the data in the memory permanently using JSON's read and write methods.
  - `display.py`: Responsible for creating a user interface, formatting of the movie list, and creating the 2D seating grid.
  - `booking.py`: Responsible for the business logic of the application (seat reservation, tax calculation, invoice generation, and cancellation of bookings).
- **Built-in Python Libraries**:
  - `sys`: Used for exit and streaming operations.
  - `json`: Used for parsing data.
  - `os`: Used for validation of the file path.
  - `random`: Used for generating booking IDs.
  - `datetime`: Used for timestamp creation.
- **Software/Development Tools**:
  - **IDE**: Visual Studio Code (VS Code)
  - **Operating Environment**: Windows PowerShell / Command Line
  - **Version Control**: Git and GitHub
---
4. Steps to Install & Run the Project
### 1. Clone the Repository
```bash
git clone https://github.com/lakebolt/movie-ticket-booking.git
cd movie-ticket-booking
