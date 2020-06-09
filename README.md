# Power-simulation
Simulation of battery for [Greener Power Solutions](https://www.gogreener.eu/) with a modbus server.
A software engineering project for Rijksuniversiteit Groningen.

## Prerequisites
To use this project you need to clone the repo:
```
git clone https://github.com/SjoerdHilhorst/power-simulation.git
```

Install the required python packages in requirements.txt with pip

```pip install -r requirements.txt```


## Usage
### Setting up a simulation
1. Navigate to ```config/env.py```
2. Input the device information, and simulation parameters 
3. Update the fields dictionary to match your own battery setup
  - ```reg_type``` to the type of modbus registry
  - ```address``` to the address in the modbus server
  - ```encode``` to the type of encoding used for the field (see encoding for more details)
  - ```init``` (optional) to fill a register with a initial value
  


### Changing the input of a field
The simulation has predefined relations for every relational field. 
| Field                    | Relation                                                                                                  |
|--------------------------|-----------------------------------------------------------------------------------------------------------|
| active_power_converter   | active_power_in - active_power_out                                                                        |
| reactive_power_converter | reactive_power_in - reactive_power_out                                                                    |
| soc                      | previous SoC + [(active_power_converter) / (Some configurable max battery capacity, say 330 kWh)] * 3600. |
| voltage_l1_l2_in         | Gaussian distribution centered around 400, deviation 3                                                    |
| voltage_l2_l3_in         | Gaussian distribution centered around 400, deviation 3                                                    |
| voltage_l3_l1_in         | Gaussian distribution centered around 400, deviation 3                                                    |
| current_l1_in            | active_power_in / (sqrt(3) * voltage_l1_l2_in * power_factor_in)                                          |
| current_l2_in            | active_power_in / (sqrt(3) * voltage_l2_l3_in * power_factor_in)                                          |
| current_l3_in            | active_power_in / (sqrt(3) * voltage_l3_l1_in * power_factor_in)                                          |
| frequency_in             | Gaussian distribution centered around 50, deviation 0.01                                                  |
| voltage_l1_l2_out        | Gaussian distribution centered around 400, deviation 3                                                    |
| voltage_l2_l3_out        | Gaussian distribution centered around 400, deviation 3                                                    |
| voltage_l3_l1_out        | Gaussian distribution centered around 400, deviation 3                                                    |
| current_l1_out           | active_power_out / (sqrt(3) * voltage_l1_l2_out * power_factor_out)                                       |
| current_l2_out           | active_power_out / (sqrt(3) * voltage_l2_l3_out * power_factor_out)                                       |
| current_l3_out           | active_power_out / (sqrt(3) * voltage_l3_l1_out * power_factor_out)                                       |
| frequency_out            | Gaussian distribution centered around 50, deviation 0.01                                                  |

Active power in, active power out, reactive power in, and reactive power out are fields from input and have to be provided by the user. For every depended field (see table), it also is possible change the relations. 

The user can define or redefine the input in the following 2 ways:

#### CSV
Suppose we want ```current_l2_out``` from ```historic_battery_data.csv``` instead of the predefined relation.

1.  in ```config/env.py``` update ```from_csv``` with the line ```current_l2_out: 'historic_battery_data'``` dictionary. Note that the key, in this case ```current_l2_out``` refers to a column in the csv table and not the simulation field.
2. in ```simulations/simulation.py``` add a method which overrides the method in the ```simulation_super``` class:
```python
def get_current_l2_out(self):
  current_l2_out = self.csv_reader.get_from_csv('current_l2_out')
  return current_l2_out
```
Note that the method name ```get_current_l2_out``` has to be the same as in the ```simulation_super``` class


#### Mathematical function
Suppose now we want ```active_power_converter``` to be ```(active_power_in - active_power_out) * 0.1)``` instead of the predefined relation.
1. in ```simulations/simulation.py``` add a method which overrides the method in the ```simulation_super``` class:
```python
def get_activer_power_converter(self):
  apc = self.battery.get_value(self.fields['active_power_in']) - self.battery.get_value(self.fields['active_power_out'])
  return apc * 0.1
```
Note that the method name ```get_active_power_converter``` has to be the same as in the ```simulation_super``` class

## Adding a new field
Suppose now we want to add a new field ```custom``` to our simulation
1. in ```config/env.py``` update  ```fields``` with your new field. If we want the field to be constant we can make use of the ```init``` to provide a constant value.
2. To provide a relation we can add a new method to ```simulations/simulations``` like for example the sine of the time elapsed:
```python
    def get_custom(self):
        return sin(self.time_elapsed)
```
3. Add the method to the ```update_custom``` function method, so that ```custom``` field will get updated every iteration
```python
    def update_custom(self):
        self.battery.set_value(self.fields['custom'], self.get_custom())
```

### Graph
To enable/disable the graph and/or add new fields to the plot, update ```graph``` in ```config/env.py```


### Database
To enable/disable the Database, update ```database``` in ```config/env.py```. Note that enabling the database will hinder performance of the program.


Now you're all setup, run
```
python3 main.py
```
## Authors
* [Mariya](https://github.com/m-ariya)
* [Victor](https://github.com/vicimikul)
* [Chris](https://github.com/chrisw889)
* [Sjoerd](https://github.com/SjoerdHilhorst)

## Acknowledgements
Huge thanks to Jasper Clarijs from Greener Power Solutions for setting us up with the project and answering questions
and [Alex Tutea](https://github.com/alextutea) our TA For guiding us through the software engineering course.
