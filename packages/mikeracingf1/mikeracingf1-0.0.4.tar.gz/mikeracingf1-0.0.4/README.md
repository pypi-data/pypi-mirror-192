# MikeRacingF1 Package

The `MikeRacingF1` package is a Python package that provides a simple and easy-to-use interface to the F1Stats API. The F1Stats API provides data about Formula 1 races, circuits, constructors, drivers, and more.

## Installation

```python
pip install mikeracingf1

```
# Usage
To use the MikeRacingF1 package, you first need to import the MikeRacingF1 class:

```python
from MikeRacingF1 import MikeRacingF1
```

You can then create a new instance of the MikeRacingF1 class, which provides methods for accessing the F1Stats API:

```python
f1stats = MikeRacingF1()
```
The MikeRacingF1 class provides the following methods:

`get_circuits(year):` Returns information about F1 circuits for the given year.

`get_constructor_results(year):` Returns results for F1 constructors for the given year.

`get_constructor_list():` Returns a list of F1 constructors.

`get_constructorstandings():` Returns standings for F1 constructors.

`get_driversinfo(year):` Returns information about F1 drivers for the given year.

`get_driverstandings(year):` Returns standings for F1 drivers for the given year.

`get_races(year):` Returns information about F1 races for the given year.

`get_results(year, round):` Returns results for an F1 race for the given year and round.

Each method sends a GET request to the corresponding endpoint of the F1Stats API, and returns the JSON response as a Python object.

Here's an example of how to use the MikeRacingF1 class to retrieve information about F1 races and circuits:

```python
from MikeRacingF1 import MikeRacingF1

f1stats = MikeRacingF1()

# Retrieve information about F1 circuits for the year 2023
circuits = f1stats.get_circuits(2023)
print("Circuits:")
print(circuits)
print()

# Retrieve information about F1 races for the year 2023
races = f1stats.get_races(2023)
print("Races:")
print(races)
print()
    
 ```
This code creates a new instance of the MikeRacingF1 class, and calls its get_circuits and get_races methods with the year 2023. It then prints the JSON responses from the F1Stats API.

License
This package is licensed under the MIT License. See the LICENSE file for details.


This `long_description` field provides a brief overview of the `MikeRacingF1` package, and includes an example of how to use it to retrieve data from the F1Stats API. It also includes a section on how to install the package, and a note about the license.



