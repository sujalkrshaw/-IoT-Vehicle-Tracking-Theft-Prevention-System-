import random

class VehicleSimulator:
    def __init__(self):
        self.latitude = 22.5726
        self.longitude = 88.3639

    def move(self):
        self.latitude += random.uniform(-0.0015, 0.0015)
        self.longitude += random.uniform(-0.0015, 0.0015)

        return {
            "latitude": round(self.latitude, 6),
            "longitude": round(self.longitude, 6)
        }