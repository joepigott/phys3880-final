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

Level 3 data contains the spectrum of a level 2 dataset with a spectral average
subtracted off. For example, an average spectrum of the datasets between 
3/24/24 and 4/09/24 can be calculated, and this will be subtracted from each
dataset's spectrum to highlight spectral differences from the average.

### Level 4

Level 4 data contains the spectral peaks in the relevant frequency range (~0.1
to 0.033 cycles/minute) of each dataset chunk. This is what is used in the
final analysis: if we find a spectral peak that is well above average, we can
do some testing on it to find out whether that peak is statistically 
significant.

### Analysis

Unfortunately, I was unable to come up with a mathematically rigorous method of
determining statistical significance. In the end, the final analysis was to
take the level 4 data and check for values that are more than three standard
deviations above the average. This checks for any strong outliers that could be
wave detections, but also idealizes many things about the data (such that it is
Gaussian, which it is not). This seems to be good enough, but it does bug me
that I couldn't come up with something more solid.
