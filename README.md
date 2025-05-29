## Problem Set 3
This project contains implementations of two algorithmic problems in Python:

    - The Goodstein sequence
    - The Hackenbush game

These problems were developed and tested as part of Discrete Mathematics course.


## Installation
Make sure you have Python 3.10+ installed. Then, clone the repository and install the project in editable mode with:

```bash 
pip install -e .
```

This allows you to make changes in the source code without reinstalling the package.


## Requirements
To install the packages, you can run:
```bash
pip install -r requirements.txt
```


## Usage
To run the test scenarios for each problem:

```bash
python tests/tests_Goodstein.py
```
Runs tests on the Goodstein sequence with an exemple of m and n, demonstrating the surprising termination of this rapidly growing sequence.

```bash
python tests/tests_Hackenbush.py
```
Allows you to play Hackenbush Game


## Author
This project was developed as part of the second problem set in a Discrete Mathematics course by Louis Bonnecaze (Louis641214).