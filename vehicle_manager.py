from math import asin, cos, radians, sin, sqrt

from requests import delete, get, post, put


class Vehicle:
    """Class for store and represent info about vehicles."""

    def __init__(
        self,
        name: str,
        model: str,
        year: int,
        color: str,
        price: float,
        latitude: float,
        longitude: float,
        id: int | None = None,
    ):
        self.id = id
        self.name = name
        self.model = model
        self.year = year
        self.color = color
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return (
            f"<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>"
        )


class VehicleManager:
    """Class for work with API (https://****.****.**/*********)."""

    def __init__(self, url: str):
        self.url = url

    def get_vehicles(self) -> list[Vehicle]:
        """Method for get all vehicles from DB.

        Gets the list of vehicles from the API, transforms it into Vehicles and returns.
        """
        result = get(self.url + "/vehicles")
        return [Vehicle(**result.json()[i]) for i in range(len(result.json()))]

    def filter_vehicles(self, params: dict[str, str | float | int]):
        """Method for get specific vehicles by params."""
        vehicle_list = get(self.url + "/vehicles").json()
        filtered_vehicles = []
        for vehicle in vehicle_list:
            suitable = True
            for key in params.keys():
                if vehicle[key] != params[key]:
                    suitable = False
            if suitable is True:
                filtered_vehicles.append(Vehicle(**vehicle))
        return filtered_vehicles

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        """Method for get vehicle by uid."""
        result: Vehicle = Vehicle(**get(self.url + f"/vehicles/{vehicle_id}").json())
        return result

    def add_vehicle(self, vehicle: Vehicle) -> Vehicle:
        """Method for add vehicle to DB."""
        result: Vehicle = Vehicle(
            **post(self.url + f"/vehicles", data=vehicle.__dict__).json()
        )
        return result

    def update_vehicle(self, vehicle: Vehicle) -> Vehicle:
        """Method for update info about vehicle."""
        result: Vehicle = Vehicle(
            **put(self.url + f"/vehicles/{vehicle.id}", data=vehicle.__dict__).json()
        )
        return result

    def delete_vehicle(self, id: int):
        """Method for delete info about vehicle by uid."""
        result = delete(self.url + f"/vehicles/{id}")
        return result

    def get_distance(self, id1: int, id2: int) -> float:
        """Method for get distance between two vehicles (in meters)."""
        first_vehicle = self.get_vehicle(id1)
        second_vehicle = self.get_vehicle(id2)
        result_distance = self.calculate_distance(
            vehicle1=first_vehicle, vehicle2=second_vehicle
        )
        return result_distance

    def get_nearest_vehicle(self, id: int) -> Vehicle:
        """Method for get the nearest vehicle to vehicle with uid = id.

        As our set of vehicles is not big we can iterate through all cars and calculate distance between each pair.
        And then we can choose vehicle with min distance.
        So time complexity of algo is O({number vehicles} * {complexity of calculating distance between 2 vehicles}).
        As a result time complexity is O(n*logn)
        """
        vehicle_list = self.get_vehicles()
        first_vehicle = self.get_vehicle(vehicle_id=id)
        min_distance = 10000000000000000000000
        suitable_vehicle = None
        for vehicle in vehicle_list:
            if vehicle.id != id:
                curr_dist = self.calculate_distance(first_vehicle, vehicle)
                if curr_dist < min_distance:
                    min_distance = curr_dist
                    suitable_vehicle = vehicle
        return suitable_vehicle

    @staticmethod
    def calculate_distance(vehicle1: Vehicle, vehicle2: Vehicle) -> float:
        """Method for calculate distance between two points on Earth.

        Formula from https://www.geeksforgeeks.org/program-distance-two-points-earth/
        """
        lon1 = radians(vehicle1.longitude)
        lon2 = radians(vehicle2.longitude)
        lat1 = radians(vehicle1.latitude)
        lat2 = radians(vehicle2.latitude)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        r = 6371000  # Earth radius (in meters)

        return c * r
