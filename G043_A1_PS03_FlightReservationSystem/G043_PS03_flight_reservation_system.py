import pathlib
import re


def write_output(string):
    output_file_path = pathlib.Path(__file__).parent / "outputPS03.txt"
    if not re.match(r"^.*$\n", string):
        string = string + '\n'
    with open(output_file_path, "a") as output:
        output.write(string)


class Flight:
    def __init__(self, flight_id, flight_description, status, next=None):
        self.flight_id = flight_id
        self.flight_description = flight_description
        self.status = status
        self.next = next


class FlightReservation:
    def __init__(self):
        self.head = None
        self.flight_counter = 1001

    def addFlight(self, flight_string=""):
        """
        Creates a flight along with a unique Flight-ID and adds it to the reservation system.
        Input: Flight string (e.g., flight destination, details).
        Output: "ADDED:<Unique Flight-ID> - <Flight String>"
        """
        is_booked = "AVAILABLE"
        flight_id = f"FL{self.flight_counter}"
        next = None
        newflight = Flight(flight_id, flight_string.strip(), is_booked, next)
        self.flight_counter = self.flight_counter + 1
        if not self.head:
            self.head = newflight
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = newflight
        write_output(f"ADDED:{newflight.flight_id}-{newflight.flight_description}")

    def removeFlight(self, flight_string="", flight_id=""):
        """
        Removes a flight along with a unique Flight-ID from the reservation system.
        Input: Flight string or Flight-ID.
        Output: "REMOVED:<Unique Flight-ID> - <Flight String>"
        """
        prev = None
        current = self.head

        while current:
            if (flight_id and current.flight_id == flight_id) or (
                    flight_string and flight_string in current.flight_description):
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next

                removed_flight = f"REMOVED:{current.flight_id} - {current.flight_description}"
                del current
                write_output(removed_flight)
                return
            prev = current
            current = current.next
        write_output("ERROR: Flight not found for removal.")
        return

    def searchFlight(self, search_string=""):
        """
        Searches for a flight and returns the associated Flight-ID.
        Input: Flight string or Flight-ID.
        Output: "SEARCHED:<Search String> \n----------------------------------------\n<Flight-ID> - <Flight String>"
        """
        current = self.head
        result = []
        while current:
            if search_string in current.flight_id or search_string in current.flight_description:
                result.append(f"{current.flight_id}-{current.flight_description}")
            current = current.next

        if result:
            write_output(f"SEARCHED:{search_string}\n----------------------------------------\n" + "\n".join(result))
        else:
            write_output(f"SEARCHED:{search_string}\n----------------------------------------\nNo matching flights found.")


    def bookFlight(self, flight_string="", flight_id=""):
        """
        Marks a flight as booked and returns a confirmation.
        Input: Flight string or Flight-ID.
        Output: "BOOKED:<Unique Flight-ID> - <Flight String>"
        """
        write_output(f"BOOKED:{flight_string or flight_id}")

    def unbookFlight(self, flight_string="", flight_id=""):
        """
        Marks a flight as available (unbooked).
        Input: Flight string or Flight-ID.
        Output: "UNBOOKED:<Unique Flight-ID> - <Flight String>"
        """
        current = self.head
        while current:
            if current.flight_id == flight_id or current.flight_description == flight_string.strip():
                if current.status == "Booked":
                    current.status = "Available"
                    write_output(f"UNBOOKED:{current.flight_id}-{current.flight_description}")
                    return
                else:
                    write_output(f"ERROR: Flight is already available: {current.flight_id}-{current.flight_description}")
                    return
            current = current.next

        write_output("ERROR: Flight not found for unbooking.")

    def statusFlight(self):
        """
        Displays the status of all flights (Booked and Available).
        Input: None.
        Output: "FLIGHT STATUS:\n--------------------------------------------------\n<Flight-ID> -<Flight String> - <Status (Booked/Available)>"
        """
        if not self.head:
            write_output("FLIGHT STATUS:\n--------------------------------------------------\nNo flights available.")
            return

        result = ["FLIGHT STATUS:\n--------------------------------------------------"]
        current = self.head
        while current:
            result.append(f"{current.flight_id} {current.flight_description} - {current.status}")
            current = current.next
        result.append("--------------------------------------------------")
        write_output("\n".join(result))


def initiateFlightSystem(read_input_file):
    """
    Reads the input file and creates a flight reservation system and all associated data structures,
    calling the necessary functions as mentioned in the input file.
        Input: Input file name with path.
        Output: None.
    """
    # Check if the provide input file exists and exit with error
    if not pathlib.Path.exists(read_input_file):
        raise Exception(f"Input file {read_input_file} does not exist")
    flight_reservation_system = FlightReservation()
    with open(read_input_file, 'r') as flight_input:
        for command in flight_input:
            operation, flights_data = command.split(":")
            flight_string = flights_data if re.match(r"^[A-Za-z\s]+ to [A-Za-z\s]+$", flights_data) else ""
            flight_id = flights_data if re.match(r"^[A-Z]{2}\d{4}$", flights_data) else ""
            if re.match(r"(?i)^add.*flight$", operation):
                flight_reservation_system.addFlight(flight_string)
            elif re.match(r"(?i)^remove.*flight$", operation):
                flight_reservation_system.removeFlight(flight_string, flight_id)
            elif re.match(r"(?i)^mark.*booked$", operation):
                flight_reservation_system.bookFlight(flight_string, flight_id)
            elif re.match(r"(?i)^mark.*available$", operation):
                flight_reservation_system.unbookFlight(flight_string, flight_id)
            elif re.match(r"(?i)^flight.*status$", operation):
                flight_reservation_system.statusFlight()
            elif re.match(r"(?i)^search.*flight$", operation):
                flight_reservation_system.searchFlight(flight_string or flight_id)


if __name__ == "__main__":
    read_input_file = pathlib.Path(__file__).parent / "inputPS03.txt"
    initiateFlightSystem(read_input_file)
