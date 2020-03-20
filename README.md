# E-Ink Display

This project is for the interface that displays information from the iglü
system on the e-ink display.

## About our the driver

Due to the structure of our iglü case and physical limitations, the e-ink
display (manufactured by Waveshare) has to be displayed upside-down. To display
things the right-side up, we had to modify the Python driver to flip the
buffer.

Link to the original source of the driver and fonts: <https://github.com/waveshare/e-Paper>
