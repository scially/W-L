#!/usr/bin/env python
# -*- coding:utf-8 -*-
from matplotlib import pyplot as plt
import numpy as np
import re
import os
import sys


def plots(resfile, offset=0, col=6, **kwargs):
    """
    offset can be use to set the y offset
    resfile is the result of track modle.
    The kwargs can be uesd to set label ,legend location,
    start_time and offset_time
    where:
        label and location is required
        start_time and end_time can be ignore.
        offset_time is start_time offset.
    """
    North = []
    dNorth = []
    with open(resfile, 'r') as f:
        for line in f.readlines():
            if line[0] == '*' or len(line) == 0:
                continue
            lines=re.split('\s+',line[1:-1])
            North.append(lines[col])
            dNorth.append(lines[col+1])
    start_time = int(kwargs.pop('start_time', 0))
    offset_time = len(North) if kwargs['offset_time'] == None else int(kwargs['offset_time'])
    end_time = start_time + offset_time
    North = np.array(North).astype('float')[start_time:end_time]
    dNorth = np.array(dNorth).astype('float')[start_time:end_time]
    plt.plot(range(0, North.shape[0]), 100 * (North-North[0]) + offset,
             label=os.path.basename(resfile)[-7:-3].upper())
    plt.errorbar(range(0,North.shape[0]), 100 * (North-North[0]) + offset,
                 yerr=dNorth*100, ecolor='pink', errorevery=10,alpha=0.1)
    plt.ylabel(kwargs['label'])
    plt.xlabel('Seconds')
    plt.legend(loc=kwargs.pop('loc', 'upper right'))


def getfiles(filelist):
    with open(filelist, 'r') as f:
        return [line.strip() for line in f.readlines()]


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('''
        This py can be used to draw the result file of track in Gamit.
        Usage:
            ./sh_track_plot.py -file <list> -out <out> -start <start> -offset <offset>
                -file is the list of track result [Required]
                -out is the result picture, and the format of picture specified
                     by the file name suffix.(For example, .png , .ps) [Required]
                -start is the drawing start time [Ignored]
                -offset is start time and end time deviation(s) 
        ''')
        sys.exit(1)
    infiles = ''
    out = ''
    start = 0
    offset = None
    for i in range(0,len(sys.argv)):
        if sys.argv[i] == '-file':
            infiles = sys.argv[i+1]
        elif sys.argv[i] == '-out':
            out = sys.argv[i+1]
        elif sys.argv[i] == '-start':
            start=sys.argv[i+1]
        elif sys.argv[i] == '-offset':
            offset = sys.argv[i+1]
    axes = plt.subplot(211)
    i = 1
    for file in getfiles(infiles):
        plots(os.path.join(os.getcwd(), file), i * 100, loc='lower right', label='North(mm)',
              start_time=start, offset_time=offset)
        i = -1 * (abs(i)+1)
    plt.savefig(out)
    plt.show()
