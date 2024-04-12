# Physics 3880 Final Project

Disclaimer: Most of the programs in this project are going to be horribly
written and not portable at all. They are all pretty much written specifically
for my use case.

## Can AGWs be detected from ground-level pressure measurements?

The purpose of this project is to see if ground-level pressure measurements can
effectively detect the presence of an Atmospheric Gravity Wave (AGW). I have
always been more of a theory guy, so I decided to step out of my comfort zone
and choose a project that is almost entirely experimental and analysis-based.

## Experimental Setup

A simple Adafruit chipset equipped with a DPS310 sensor was placed outside of
my apartment and set to take pressure measurements once per minute.

## Data Levels

Each data file is prefixed with its corresponding data level: `l0` for level 0,
`l1` for level 1, etc.

### Level 0

Level 0 data is raw data obtained from the sensor. Files will usually include a
timestamp, and optionally an hour index if the dataset has been split. For 
example, the file
```
l0_pressure_2024-03-24_2024-04-09_4.csv
```
is fourth section of raw pressure data between 3/24/24 and 4/9/24. The hour
index may represent different chunks of time, depending on how analysis goes;
as of writing this, it's currently two hours per index.

Metadata of the starting and ending dates as well as the hour index are stored
in the file.

### Level 1

Level 1 data is the data relative to that set's average. In the process of 
converting level 0 to level 1, the average of the level 0 data is simply 
subtracted off, and this new dataset is stored as a level 1 dataset, along with
any metadata.

### Level 2a

Level 2a data contains the Fourier transform and corresponding frequency array 
of the level 1 data, along with any metadata.

### Level 2b

Level 2b data contains the Fourier transform and corresponding frequency array
of the *padded* level data, along with any metadata. A series of zeroes are
added to the end of the level 1 data to effectively interpolate between points
in frequency space.

### Level 3

Level 3 data contains the relative spectrum of level 2 as compared to an
average spectrum (that is yet to be defined).
