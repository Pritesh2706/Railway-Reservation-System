# Railway-Reservation-System

Overview
This is a Python-based Railway Reservation System that manages train schedules and ticket bookings using a MySQL database. The application provides a command-line interface for performing CRUD operations on trains and booking tickets, with features to view train details and ticket reports.
Features

Train Management:
Add new trains with details (train number, name, source, destination, total seats).
Update train information.
Delete trains.
List all trains in a formatted table.


Ticket Booking:
Book tickets for passengers with specified seat counts.
Automatically update available seats.
Generate unique ticket IDs using UUID.


Reporting:
View all booked tickets with train and passenger details.


Database:
Uses MySQL for persistent storage.
Automatically creates RailwayDB database and required tables (Trains, Tickets).



Prerequisites

Python 3.6+
MySQL Server installed and running
Required Python packages:
mysql-connector-python
tabulate
uuid (included in Python standard library)



Installation

Clone the Repository:
git clone <repository-url>
cd railway-reservation-system


Install Dependencies:
pip install mysql-connector-python tabulate


Configure MySQL:

Ensure MySQL is running.
Update the database connection settings in the script (if needed):host='localhost',
user='root',
password='Create Your Password',
database='RailwayDB'

Replace password with your MySQL root password.


Run the Application:
python railway_reservation.py



Usage

Launch the script to access the interactive menu.
Choose options (1-7) to perform operations:
Add Train: Input train details to add a new train.
Update Train: Provide train ID and new values to update.
Delete Train: Enter train ID to remove a train.
List Trains: View all trains in a tabular format.
Book Ticket: Provide train ID, passenger name, and seat count.
View All Tickets: Display all booked tickets.
Exit: Close the application.



Database Schema

Trains Table:
TrainID: Auto-incremented primary key.
TrainNumber: Unique train identifier.
TrainName: Name of the train.
Source: Starting station.
Destination: End station.
TotalSeats: Total seat capacity.
AvailableSeats: Remaining seats.


Tickets Table:
TicketID: UUID-based primary key.
TrainID: Foreign key referencing Trains.
PassengerName: Name of the passenger.
SeatCount: Number of seats booked.
BookingDate: Timestamp of booking.



Error Handling

The application includes error handling for database connections, queries, and invalid inputs.
Connection issues or SQL errors are caught and displayed to the user.

Notes

Ensure the MySQL server is running before starting the application.
The tabulate library is used to display data in a formatted table.
The database and tables are created automatically on first run.
Passwords in the code should be secured in a production environment (e.g., using environment variables).

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Contributions are welcome! Please submit a pull request or open an issue for suggestions or bug reports.
