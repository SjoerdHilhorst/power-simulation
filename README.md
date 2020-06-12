# Power-simulation
Simulation of battery for [Greener Power Solutions](https://www.gogreener.eu/) with a modbus server.
A software engineering project for Rijksuniversiteit Groningen.

## Prerequisites
The software requires Python 3.5
To use this project you need to clone the repo:
```
git clone https://github.com/SjoerdHilhorst/power-simulation.git
```

Install the required python packages in requirements.txt with pip

```pip install -r requirements.txt```


## Running
first determine your enviromnent in a json file in config
and set filename as your json filename in main.py 

Now you're all setup, run
```
python3 main.py
```
To set up a new simulation you can alter the ```configuration/env.py``` to specify your own configuration and in ```simulations/simulation.py``` you can override and/or define any field declared in ```env.py``` with your own functions

## Authors
* [Mariya](https://github.com/m-ariya)
* [Victor](https://github.com/vicimikul)
* [Chris](https://github.com/chrisw889)
* [Sjoerd](https://github.com/SjoerdHilhorst)

## Acknowledgements
Huge thanks to Jasper Clarijs from Greener Power Solutions for setting us up with the project and answering questions
and [Alex Tutea](https://github.com/alextutea) our TA For guiding us through the software engineering course.
