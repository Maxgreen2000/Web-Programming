class Flight():
    def __init__(self, capacity):
        self.capacity = capacity
        self.passengers = []
    
    def add_passengers(self, name):
        if not self.open_seats():  ## this effectively says if open_seats() == 0
            return False
        self.passengers.append(name)
        return True
        
    def open_seats(self):
        return self.capacity - len(self.passengers)

        
flight = Flight(3)

people = ["Harry", "Ron", "Hermione", "Ginny"]
for person in people:
    if flight.add_passengers(person):
        print(f"Added {person} to flight succesfully.")
    else:
        print(f"No available seats for {person}")
        
    
