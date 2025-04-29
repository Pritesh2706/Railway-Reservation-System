import mysql.connector
from mysql.connector import Error
from tabulate import tabulate # type: ignore
import uuid

# Database and table setup
def create_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pritesh@27'
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS RailwayDB")
    except Error as e:
        print(f"Error creating database: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pritesh@27',
            database='RailwayDB'
        )
        cursor = conn.cursor()
        # Trains table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Trains (
                TrainID INT AUTO_INCREMENT PRIMARY KEY,
                TrainNumber VARCHAR(20) NOT NULL UNIQUE,
                TrainName VARCHAR(100) NOT NULL,
                Source VARCHAR(50) NOT NULL,
                Destination VARCHAR(50) NOT NULL,
                TotalSeats INT NOT NULL DEFAULT 0,
                AvailableSeats INT NOT NULL DEFAULT 0
            );
        """)
        # Tickets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Tickets (
                TicketID VARCHAR(36) PRIMARY KEY,
                TrainID INT,
                PassengerName VARCHAR(100) NOT NULL,
                SeatCount INT NOT NULL,
                BookingDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (TrainID) REFERENCES Trains(TrainID)
            );
        """)
    except Error as e:
        print(f"Error creating tables: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Utility: connect
def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Pritesh@27',
            database='RailwayDB'
        )
        return conn
    except Error as e:
        print(f"Connection error: {e}")
        return None

# CRUD for trains
def add_train(train_number, train_name, source, destination, total_seats):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Trains (TrainNumber, TrainName, Source, Destination, TotalSeats, AvailableSeats) VALUES (%s, %s, %s, %s, %s, %s)",
                (train_number, train_name, source, destination, total_seats, total_seats)
            )
            conn.commit()
            print(f"Added train '{train_name}' ({train_number}) successfully.")
        except Error as e:
            print(f"Error adding train: {e}")
        finally:
            cursor.close()
            conn.close()

def update_train(train_id, **kwargs):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            fields = []
            values = []
            for key, value in kwargs.items():
                fields.append(f"{key} = %s")
                values.append(value)
            values.append(train_id)
            sql = f"UPDATE Trains SET {', '.join(fields)} WHERE TrainID = %s"
            cursor.execute(sql, tuple(values))
            conn.commit()
            print(f"Updated train {train_id}.")
        except Error as e:
            print(f"Error updating train: {e}")
        finally:
            cursor.close()
            conn.close()

def delete_train(train_id):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Trains WHERE TrainID = %s", (train_id,))
            conn.commit()
            print(f"Deleted train {train_id}.")
        except Error as e:
            print(f"Error deleting train: {e}")
        finally:
            cursor.close()
            conn.close()

def list_trains():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT TrainID, TrainNumber, TrainName, Source, Destination, TotalSeats, AvailableSeats FROM Trains")
            rows = cursor.fetchall()
            if rows:
                headers = [desc[0] for desc in cursor.description]
                print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
            else:
                print("No trains found.")
        except Error as e:
            print(f"Error fetching trains: {e}")
        finally:
            cursor.close()
            conn.close()

# Ticket booking
def book_ticket(train_id, passenger_name, seat_count):
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Check available seats
            cursor.execute("SELECT AvailableSeats FROM Trains WHERE TrainID = %s", (train_id,))
            result = cursor.fetchone()
            if result and result[0] >= seat_count:
                ticket_id = str(uuid.uuid4())
                cursor.execute(
                    "INSERT INTO Tickets (TicketID, TrainID, PassengerName, SeatCount) VALUES (%s, %s, %s, %s)",
                    (ticket_id, train_id, passenger_name, seat_count)
                )
                cursor.execute(
                    "UPDATE Trains SET AvailableSeats = AvailableSeats - %s WHERE TrainID = %s",
                    (seat_count, train_id)
                )
                conn.commit()
                print(f"Ticket booked: ID {ticket_id} for {passenger_name}, {seat_count} seat(s).")
            else:
                print("Insufficient seats or invalid train.")
        except Error as e:
            print(f"Error booking ticket: {e}")
        finally:
            cursor.close()
            conn.close()

# Reporting
def view_all_tickets():
    conn = get_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT t.TicketID, tr.TrainNumber, tr.TrainName, t.PassengerName, t.SeatCount, t.BookingDate "
                "FROM Tickets t JOIN Trains tr ON t.TrainID = tr.TrainID"
            )
            rows = cursor.fetchall()
            if rows:
                headers = [desc[0] for desc in cursor.description]
                print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))
            else:
                print("No tickets booked yet.")
        except Error as e:
            print(f"Error fetching tickets: {e}")
        finally:
            cursor.close()
            conn.close()

# Main interactive menu
def main():
    create_database()
    while True:
        print("\n--- RAILWAY RESERVATION SYSTEM ---")
        print("1. Add Train")
        print("2. Update Train")
        print("3. Delete Train")
        print("4. List Trains")
        print("5. Book Ticket")
        print("6. View All Tickets")
        print("7. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            train_number = input("Train number: ")
            train_name = input("Train name: ")
            source = input("Source station: ")
            destination = input("Destination station: ")
            total_seats = int(input("Total seats: "))
            add_train(train_number, train_name, source, destination, total_seats)
        elif choice == '2':
            train_id = int(input("Train ID to update: "))
            print("Enter new values (leave blank to skip):")
            new_train_number = input("New train number: ")
            new_train_name = input("New train name: ")
            new_source = input("New source: ")
            new_destination = input("New destination: ")
            new_total_seats = input("New total seats: ")
            new_available_seats = input("New available seats: ")
            updates = {}
            if new_train_number: updates['TrainNumber'] = new_train_number
            if new_train_name: updates['TrainName'] = new_train_name
            if new_source: updates['Source'] = new_source
            if new_destination: updates['Destination'] = new_destination
            if new_total_seats: updates['TotalSeats'] = int(new_total_seats)
            if new_available_seats: updates['AvailableSeats'] = int(new_available_seats)
            update_train(train_id, **updates)
        elif choice == '3':
            train_id = int(input("Train ID to delete: "))
            delete_train(train_id)
        elif choice == '4':
            list_trains()
        elif choice == '5':
            train_id = int(input("Train ID to book: "))
            passenger_name = input("Passenger name: ")
            seat_count = int(input("Number of seats: "))
            book_ticket(train_id, passenger_name, seat_count)
        elif choice == '6':
            view_all_tickets()
        elif choice == '7':
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()