#!/usr/bin/env python3

import csv
import json
import sys
import os
import signal
import codecs
import curses
from candump_processor.decoder import decoder

#check args
if len(sys.argv) != 2:
    print("Usage: %s candump_file" % sys.argv[0])
    sys.exit(1)

#load defs 
data_decoder = decoder('./definitions.txt')
#candump file
data_log = sys.argv[1]
#can log data
data = []

def restore_term():
    #curses end
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


#handle sigterm, siginit so curses doesn't break the term
def sigterm_handler(_signo, _stack_frame):
    restore_term()
    #exit
    sys.exit(0)

#register signals handlers
signal.signal(signal.SIGTERM, sigterm_handler)
signal.signal(signal.SIGINT, sigterm_handler)

#load data from candump
with open(data_log) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=' ')
    lc = 0
    for r in csv_reader:
        data.append(r[2])

#init curses screen
stdscr = curses.initscr()
curses.noecho()

#refresh data on screen
def redraw(mapp):
    j = 2
    l = 2
    stdscr.addstr(0, 0, " State: 0 = Off, 1 = On")
    for i in mapp:
        for k in mapp[str(i)]:
            if type(k["result"]) == str:
                stdscr.addstr(j, l, "{:<24}: {:<8} {}".format(k["name"], k["result"], k["unit"]))
            else:
                stdscr.addstr(j, l, "{:<24}: {:<8.0f} {}".format(k["name"], k["result"], k["unit"]))
            j+=1
            if j == 20:
                l = 55
                j = 2


#loop through the candump data
try:
    for i in data:
        #optionall - slow down the data processing
        #sleep(0.02)
        temp = i.split('#')
        msgid = temp[0]
        msgdata = codecs.decode(temp[1], 'hex')
        data_decoder.update_map(msgid, msgdata)
        redraw(data_decoder.output())
        stdscr.refresh()

except Exception as e:
    restore_term()
    raise


restore_term()

