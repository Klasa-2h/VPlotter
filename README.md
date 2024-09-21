
# VPlotter

This Arduino-based plotter uses two motors to control a pen suspended by strings, allowing it to draw on large surfaces.

It’s a simple, affordable solution for automated, large-scale drawings.


## Installation
    1. Clone this repository or dowload the latest release

## Latest release
No releases yet. 


## Getting started
This project's software is divided into 2 parts:

  1. Arduino code that performs drawing
  2. Windows GUI app that enables users to read an image they want to draw and set right parameters.
    Based on the selected image this app generates a file with information for the Arduino. 
---
1. In the project's ```arduino``` folder you'll find the code that you need to paste in your Arduino (using Aduino IDE)

2. In ```src``` folder there is a ```main.py``` file that opens up the main window of the application.

### Usage

1. Select image you want to draw

2. Select the destination of the steps file. 
This should be an empty SD card that later you insert into the Arduino.

3. Set all the parameters

4. Choose the drawing style

5. Generate the steps file and preview the simulation

6. Tweek the parameters until you're happy with the result

7. set the starting marker position on the plotter according to the calculated values

8. Insert the SD card with previously generated steps file into the the Arduino

9. Run the Arduino script and wait for it to finish your drawing

## License
[Mit License](https://opensource.org/licenses/MIT)


Copyright 2024 LO 1 Rumia Klasa 3h

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
