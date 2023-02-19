# Test
## How to use
### First clone repo to your PC:
```
git clone https://github.com/L1mple/test.git
```
### First install requirements with terminal command:
```
pip install -r requirements.txt
```
### Create object of VahicleManager class:
```python
manager = VehicleManger(url="https://test.tspb.su/test-task")
```
### Feel free to play with commands:
```python
manager.get_vehicles()
manager.get_vehicle(id={id})
manager.add_vehicle(vehicle=Vehicle(...)
manager.update_vehicle(vehicle=Vehicle(id={id}, ...)
manager.delete_vehicle(id={id})
manager.get_distance(id1={id_of_first_vehicle}, id2={id_of_second_vehicle})
manager.get_nearest_vehicle(id={id}) # vehicle nearest to vehicle with id={id}
```
