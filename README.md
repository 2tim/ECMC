# ECMC Coding Challenge

## Task
Task 1 was chosen. The problem statement can be found in ./byte-reader/README.md

Solution
--------

The solution is coded in Python. It assumes little when dealing wth the floating point debits and credits. For financial transactions this detail would need to be worked out in the business rules.

Running the code
----------------

Ensure you have python3 installed:

On a Mac you can install it with Homebrew:

`brew install python3`

Then you can run with:

`git clone https://github.com/2tim/ECMC.git`

`cd ECMC`

`python3 data_reader.py`

Results will be printed to the screen.

Recommendations for dealing with floating point currency input would be to use the python-money package:
https://github.com/carlospalol/money

The code would be adapted to use the library to convert the raw float64 item to a python money object. The project is mature, follows industry standards and is easy to use.
