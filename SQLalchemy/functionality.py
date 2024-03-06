from database import Session, Car, Invoice

#INSERT FUNCTIONALITY
def addOneCar():
    with Session() as session:
        session.add(Car(
            manufacturer = "Tesla",
            model = "Model 3"
        ))
        session.commit()

def addMultipleCars():
    with Session() as session:
        session.add_all([
            Car(manufacturer = "Porche", model = "Cayenne"),
            Car(manufacturer = "Wolkswagen", model = "ID.3")
        ])
        session.commit()

#PRINT FUNCTIONALITY
        
def printAllCars():
    with Session() as session:
        allCars = session.query(Car)
        if allCars is None: return

        for car in allCars:
            print(car.manufacturer, car.model)

def printSingleCar():
    with Session() as session:
        car = session.query(Car).filter( Car.manufacturer == "Tesla" ).first()
        if car is None:
            print("Car was not found")
        else:
            print("We found this single car:")
            print(car.manufacturer, car.model)

def printFilters():
    with Session() as session:
        # > print first car with ID larger than 1
        print("### PRINT FILTERS:")
        car = session.query(Car).filter( Car.carId > 1 ).first()
        print(car.carId, car.manufacturer)

        # > print all cars with ID less than 3
        print("### NEXT FILTERS:")
        car_all = session.query(Car).filter( Car.carId < 3 ).all()
        for car in car_all:
            print(car.carId, car.manufacturer)

        # AND: print car that has model "Model 3" and manufacturer "Tesla"
        car = session.query(Car).filter( Car.model == "Model Y", Car.manufacturer == 'Tesla').first()
        print("### AND Filters")
        print(car.manufacturer)

        # LIKE: print car that has manufacturer like 'wagen'
        car = session.query(Car).filter( Car.manufacturer.like("%wagen%") ).first()
        print('### Like FIlters')
        print(car.manufacturer)

        # IN: print car that has manufaturer Wolkswagen or Ford
        lst = [ "Wolkswagen", "Tesla" ]
        cars = session.query(Car).filter( Car.manufacturer.in_( lst ))
        print("### IN Filters")
        for car in cars:
            print(car.model)
        
        # OR: print car that have manufacturer Wolkswagen or Ford
        cars = session.query(Car).filter( (Car.manufacturer == "Wolkswagen") | (Car.manufacturer == "Tesla") )
        print("### OR Filter")
        for car in cars:
            print(car.manufacturer, car.model)

        # OR & AND: print cars that have model "ID.3" OR model "Golf" AND manufacturer is "Wolkswagen"
        cars = session.query(Car).filter(
            (Car.model == "ID.3") | (Car.model == "Golf"),
            Car.manufacturer == "Wolkswagen"
        )
        print("### OR & AND:")
        for car in cars:
            print(car.manufacturer, car.model)
        # SORT BY: Find all cars with ID over 1, sorted by manufacturer in ascending order
        # Note: IMPORT desc for descending order
        from sqlalchemy import asc, desc
        cars = session.query(Car).filter( Car.carId > 1 ).order_by( asc( Car.manufacturer ) )
        print("### ORDER BY:")
        for car in cars:
            print(car.manufacturer)

        # LIMIT: Find all cars with ID over 1, order by carId asc, limit to 2 entries
        print("### LIMIT")
        cars = session.query(Car).filter( Car.carId > 1 ).order_by( asc( Car.carId ) ).limit(2)
        for car in cars:
            print(car.carId)
# REMOVE FUNCTIONALITY 
            
def removeAllCars(): #CLEAR UP
    # Automatic way
    with Session() as session:
        session.query(Car).delete()
        session.commit()
    
    # Manual way
    '''with Session() as session:
        allCars = session.query(Car).filter().delete()
        for car in allCars:
            session.delete(car)
        session.commit()'''

def removeCar():
    with Session() as session:
        tesla = session.query(Car).filter( Car.manufacturer == "Tesla").first()
        if tesla is None: return
        session.delete(tesla)
        session.commit() 

# EDIT FUNCTIONALITY

def editCar():
    with Session() as session:
        tesla = session.query(Car).filter(  Car.model == "Model 3"  ).first()
        if tesla is None: return

        tesla.model = "Model Y"
        session.commit()