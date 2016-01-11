# SenseHatLogger
A Raspberry Pi Sense Hat sensor logger with LED and text file output.

##Usage
####logger.py [-h] [-t START END] [-r ROTATION] [-b]

####-h, --help
show help message and exit

####-t START END, --timerange START END
Optional argument to change hours the LED matrix should be off. Time range is a start and an end hour, where the start is inclusive and the end is exclusive. Both times are 0 indexed 24 hour times, so valid hours are 0-23.

####-r ROTATION, --rotation ROTATION
Optional argument to change the LED matrix rotation in degrees. The screen will be rotated to the nearest 90 degree that was entered.

####-b, --bright
Optional argument to turn the LED matrix to full brightness instead of low.
