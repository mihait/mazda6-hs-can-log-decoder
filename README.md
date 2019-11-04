# Mazda 6 GJ HS-CAN ids decoder

Mazda 6 GJ (3rd gen) 2013(Europe)/2014(US), manual gearbox, decoded can bus ids + candump decoder

### Disclaimer
Use this at your own risk! I'm not responsible for any damage, risks, accidents, injuries and so on that you may provoke to you or others.
The HS-CAN is a critical network of your car. Do not attempt to write messages on the bus unless you really really really know what you're doing.
Test the interface on the bench before using it in your car.

### Description

This is a small project and tutorial on how to:
   - get a working OBD2 to USB SocketCan interface
   - dump CAN bus traffic to a text file
   - interpret the candump data for a mazda 6 gj (in this case) with the guessed can ids
   - the definitions.txt json file can be modified to replay other cars logs

### Instructions - socketcan interface

Hardware:  OBD2 dev kit from: https://docs.longan-labs.cc/1030003/

Firmware: https://github.com/kahiroka/slcanuino ( modified defaults.h pins for arduino leonardo)

Software: linux can-utils

Interface setup for can dump

```sh
$ sudo slcan_attach -f -s6 -o /dev/ttyACM0  
$ sudo slcand -S 1000000 ttyACM0 can0  
$ sudo ifconfig can0 up  
```

Dump log:

```sh
$ candump -l can0
```

Stop slcan:

```sh
$ sudo ifconfig can0 down  
$ sudo killall slcand  
```

Parse results:

   - python3 


```sh
$ ./dumb_log_parser.py candumo-<date>-<time>.log
```

Output demo:

[![asciicast](https://asciinema.org/a/279110.svg)](https://asciinema.org/a/279110)



