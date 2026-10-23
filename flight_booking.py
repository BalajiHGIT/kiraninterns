
from abc import ABC, abstractmethod
from dataclasses import dataclass
from uuid import uuid4


class Passenger(ABC):
    def __init__(self, name, age):
        self._name = name
        self._age = age

    @property
    def name(self):
        return self._name

    @property
    def age(self):
        return self._age

    @abstractmethod
    def get_discount(self):
        pass


class RegularPassenger(Passenger):
    def get_discount(self):
        return 0


class StudentPassenger(Passenger):
    def get_discount(self):
        return 10


class Flight:
    def __init__(self, code, airline, source, destination, seats, fare):
        self.code = code
        self.airline = airline
        self.source = source
        self.destination = destination
        self._available_seats = seats
        self.base_fare = fare

    @property
    def available_seats(self):
        return self._available_seats

    def has_seats(self, count):
        return count > 0 and count <= self._available_seats

    def reserve_seats(self, count):
        if not self.has_seats(count):
            raise ValueError("Not enough available seats.")
        self._available_seats -= count


@dataclass
class Booking:
    booking_id: str
    passenger: Passenger
    flight: Flight
    tickets: int
    base_total: float
    discount_amount: float
    final_fare: float


class FlightBookingSystem:
    def __init__(self):
        self.flights = [
            Flight("AI101", "Air India", "Mumbai", "Delhi", 20, 4500),
            Flight("6E202", "IndiGo", "Pune", "Bengaluru", 15, 3500),
            Flight("UK303", "Vistara", "Delhi", "Mumbai", 10, 5000),
        ]
        self.bookings = []
        self.last_booking = None

    def display_flights(self):
        print("\n" + "=" * 85)
        print("AVAILABLE FLIGHTS")
        print("=" * 85)
        print(
            f"{'Code':<10}{'Airline':<15}{'Source':<15}"
            f"{'Destination':<15}{'Seats':<10}{'Fare':>10}"
        )
        print("-" * 85)

        for flight in self.flights:
            print(
                f"{flight.code:<10}{flight.airline:<15}"
                f"{flight.source:<15}{flight.destination:<15}"
                f"{flight.available_seats:<10}Rs.{flight.base_fare:,.2f}"
            )
        print("=" * 85)

    def find_flight(self, code):
        for flight in self.flights:
            if flight.code.lower() == code.strip().lower():
                return flight
        return None

    def validate_booking(self, flight, name, age, tickets, category):
        if flight is None:
            raise ValueError("Invalid flight code.")

        if not name.strip():
            raise ValueError("Passenger name cannot be empty.")

        if not age.isdigit() or not 1 <= int(age) <= 120:
            raise ValueError("Enter a valid age between 1 and 120.")

        if not tickets.isdigit() or int(tickets) < 1:
            raise ValueError("Ticket count must be a positive number.")

        if category not in ("1", "2"):
            raise ValueError("Select a valid passenger category.")

        if int(tickets) > flight.available_seats:
            raise ValueError(
                f"Only {flight.available_seats} seats are available."
            )

        return True

    def calculate_fare(self, flight, passenger, tickets):
        base_total = flight.base_fare * tickets
        discount_amount = base_total * passenger.get_discount() / 100
        final_fare = base_total - discount_amount

        return base_total, discount_amount, final_fare

    def confirm_booking(self, flight, passenger, tickets):
        base, discount, final = self.calculate_fare(
            flight, passenger, tickets
        )

        flight.reserve_seats(tickets)

        booking = Booking(
            booking_id="FB" + uuid4().hex[:8].upper(),
            passenger=passenger,
            flight=flight,
            tickets=tickets,
            base_total=base,
            discount_amount=discount,
            final_fare=final,
        )

        self.bookings.append(booking)
        self.last_booking = booking
        return booking

    def display_summary(self, booking):
        print("\n" + "=" * 45)
        print("         BOOKING CONFIRMED")
        print("=" * 45)
        print("Booking ID       :", booking.booking_id)
        print("Passenger Name   :", booking.passenger.name)
        print("Passenger Age    :", booking.passenger.age)
        print("Passenger Type   :", type(booking.passenger).__name__)
        print("Flight Code      :", booking.flight.code)
        print("Airline          :", booking.flight.airline)
        print("Route            :", booking.flight.source,
              "to", booking.flight.destination)
        print("Number of Tickets:", booking.tickets)
        print("Fare per Ticket  : Rs.", f"{booking.flight.base_fare:,.2f}")
        print("Base Total       : Rs.", f"{booking.base_total:,.2f}")
        print("Discount         : Rs.", f"{booking.discount_amount:,.2f}")
        print("Final Amount     : Rs.", f"{booking.final_fare:,.2f}")
        print("Remaining Seats  :", booking.flight.available_seats)
        print("=" * 45)

    def book_flight(self):
        self.display_flights()

        code = input("Enter flight code: ")
        flight = self.find_flight(code)

        name = input("Enter passenger name: ")
        age = input("Enter passenger age: ")
        tickets = input("Enter number of tickets: ")

        print("\n1. Regular Passenger (0% discount)")
        print("2. Student Passenger (10% discount)")
        category = input("Select passenger category: ")

        try:
            self.validate_booking(
                flight, name, age, tickets, category
            )

            age_value = int(age)
            ticket_count = int(tickets)

            if category == "1":
                passenger = RegularPassenger(name.strip(), age_value)
            else:
                passenger = StudentPassenger(name.strip(), age_value)

            booking = self.confirm_booking(
                flight, passenger, ticket_count
            )
            self.display_summary(booking)

        except ValueError as error:
            print("\nBooking Error:", error)
            print("No booking was created.")

    def view_booking(self):
        if self.last_booking is None:
            print("\nNo confirmed booking found.")
        else:
            self.display_summary(self.last_booking)

    def run(self):
        while True:
            print("\n===== FLIGHT BOOKING SYSTEM =====")
            print("1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.display_flights()
            elif choice == "2":
                self.book_flight()
            elif choice == "3":
                self.view_booking()
            elif choice == "4":
                print("Thank you for using Flight Booking System. Goodbye!")
                break
            else:
                print("Invalid choice! Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    system = FlightBookingSystem()
    system.run()
