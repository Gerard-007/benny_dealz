import datetime
from typing import List

MANUFACTURERS = (
    ("Abarth", "Abarth"),
    ("Alfa Romeo", "Alfa Romeo"),
    ("Aston Martin", "Aston Martin"),
    ("Audi", "Audi"),
    ("Bentley", "Bentley"),
    ("BMW", "BMW"),
    ("Bugatti", "Bugatti"),
    ("Cadillac", "Cadillac"),
    ("Chevrolet", "Chevrolet"),
    ("Chrysler", "Chrysler"),
    ("Citroën", "Citroën"),
    ("Dacia", "Dacia"),
    ("Daewoo", "Daewoo"),
    ("Daihatsu", "Daihatsu"),
    ("Dodge", "Dodge"),
    ("Donkervoort", "Donkervoort"),
    ("DS", "DS"),
    ("Ferrari", "Ferrari"),
    ("Fiat", "Fiat"),
    ("Fisker", "Fisker"),
    ("Ford", "Ford"),
    ("Honda", "Honda"),
    ("Hummer", "Hummer"),
    ("Hyundai", "Hyundai"),
    ("Infiniti", "Infiniti"),
    ("Innoson", "Innoson"),
    ("Iveco", "Iveco"),
    ("Jaguar", "Jaguar"),
    ("Jeep", "Jeep"),
    ("Kia", "Kia"),
    ("KTM", "KTM"),
    ("Lada", "Lada"),
    ("Lamborghini", "Lamborghini"),
    ("Lancia", "Lancia"),
    ("Land Rover", "Land Rover"),
    ("Landwind", "Landwind"),
    ("Lexus", "Lexus"),
    ("Lotus", "Lotus"),
    ("Maserati", "Maserati"),
    ("Maybach", "Maybach"),
    ("Mazda", "Mazda"),
    ("McLaren", "McLaren"),
    ("Mercedes-Benz", "Mercedes-Benz"),
    ("MG", "MG"),
    ("Mini", "Mini"),
    ("Mitsubishi", "Mitsubishi"),
    ("Morgan", "Morgan"),
    ("Nissan", "Nissan"),
    ("Opel", "Opel"),
    ("Peugeot", "Peugeot"),
    ("Porsche", "Porsche"),
    ("Renault", "Renault"),
    ("Rolls-Royce", "Rolls-Royce"),
    ("Rover", "Rover"),
    ("Saab", "Saab"),
    ("Seat", "Seat"),
    ("Skoda", "Skoda"),
    ("Smart", "Smart"),
    ("SsangYong", "SsangYong"),
    ("Subaru", "Subaru"),
    ("Suzuki", "Suzuki"),
    ("Tesla", "Tesla"),
    ("Toyota", "Toyota"),
    ("Volkswagen", "Volkswagen"),
    ("Volvo", "Volvo")
)


CATEGORY = (
    ('New', 'New'),
    ('Foreign Used', 'Foreign Used'),
    ('Nigerian Used', 'Nigerian Used')
)

YEAR_CHOICES = [(r, r) for r in range(1995, datetime.date.today().year)]

TRANSMISSION = (
    ('Manual', 'Manual'),
    ('Automatic', 'Automatic'),
    ('Duplex', 'Duplex')
)

FUEL_TYPE = (
    ('Diesel', 'Diesel'),
    ('PetroleumGas', 'PetroleumGas'),
    ('Petrol', 'Petrol'),
    ('Hybrid', 'Hybrid')
)

BODY_TYPE = (
    ('Bus', 'Bus'),
    ('Coupe', 'Coupe'),
    ('Hatchback', 'Hatchback'),
    ('Pickup', 'Pickup'),
    ('Suv', 'Suv'),
    ('Convertible', 'Convertible'),
    ('Crossover', 'Crossover'),
    ('Mpv', 'Mpv'),
    ('Sedan', 'Sedan'),
    ('Truck', 'Truck')
)

STATUS = (
    ('Sold', 'Sold'),
    ('Available', 'Available'),
    ('Rented', 'Rented'),
    ('Swapped', 'Swapped'),
)

SWAP_STATUS = (
    ('Swap', 'Swap'),
    ('Sell', 'Sell'),
)

body_types = [
            'Bus',
            'Coupe',
            'Hatchback',
            'Pickup',
            'Suv',
            'Convertible',
            'Crossover',
            'Mpv',
            'Sedan',
            'Truck'
        ]
