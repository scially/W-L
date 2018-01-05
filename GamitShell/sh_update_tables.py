#!/usr/bin/env python3
# -*- encoding:utf-8 -*-
"""
Updating tables file in Gasmit10.x by this pyhon script
authors: wanghui
emails : wzxwhd@126.com
"""
import ftplib
import sys
import os
import time
import functools

if len(sys.argv) == 1:
    print(
        '''
        Updating tables file in Gamit10.x by this py-shell
        Usage: [sudo] python3 sh_update_tables.py -link n -grid <y/n> -version <v> -path <p> -year <year> -out <path>
            -link    link the downloading files in tables, this need to root[y/n]
            -tables  downlaod tables[y/n] [default is y]
            -grid    download grids[y/n] [default is n]
            -path    the path of gamit[default is ~/gamit10.6]
            -version the version of gamit[default is 10.6]
            -out     on which download tables [default is current path]
        Example: [sudo] python3 sh_update_tables.py -link y -grid n -version 10.6 -year 2018 
        ''')
    sys.exit(1)

# global configure
# modify these parametes according to your system
Link=False
Grid = False
Tables = True
Version = 10.6
year = 2018
Out = os.path.join(os.getcwd(),'tables')
Path='~/gamit10.6'
__current_size = 0

# get parameters
for index in range(0, len(sys.argv)):
    if sys.argv[index] == '-link':
        Link = True if sys.argv[index + 1] == 'y' else False
    elif sys.argv[index] == '-grid':
        Grid = True if sys.argv[index + 1] == 'y' else False
    elif sys.argv[index] == '-version':
        Version = float(sys.argv[index + 1])
    elif sys.argv[index] == '-year':
        year = sys.argv[index + 1]
    elif sys.argv[index] == '-out':
        Out = sys.argv[index + 1]
    elif sys.argv[index]=='-path':
        Path = sys.argv[index + 1]
    elif sys.argv[index]=='-tables':
        Tables = True if sys.argv[index+1] == 'y' else False

tables = {'pole.usno': 'pole.',
          'ut1.usno': 'ut1.',
          'luntab.{0}.J2000'.format(year): 'luntab.',
          'soltab.{0}.J2000'.format(year): 'soltab.',
          'nutabl.{0}'.format(year): 'nutabl.',
          'leap.sec': None,
          'gedtic.dat': None,
          'antmod.dat': None,
          'rcvant.dat': None,
          'guess_rcvant.dat':None,
          'svnav.dat.gnss': 'svnav.dat',
          'svnav.dat.gps': 'svnav.dat',
          'dcb.dat.gnss': 'dcb.dat',
          'dcb.dat.gps': 'dcb.dat',
          }
grids = {'vmf1grd.{0}'.format(year): 'map.grid.{0}'.format(year),
        'atmdisp_cm.{0}'.format(year): 'atml.grid.{0}'.format(year),
        }


# construct ftp object
def connect(host):
    try:
        ftp = ftplib.FTP(host, user='anonymous', passwd='anonymous')
        ftp.connect()
        ftp.login()
        return ftp
    except:
        print('FTP is unavailable, please check you system')
        sys.exit(1)

def write_callback(totalsize, fileobjct, blocks):
    global __current_size
    __current_size += len(blocks)
    fileobjct.write(blocks)
    #print('总大小{}，当前大小{}, 百分比{}'.format(totalsize, __current_size, __current_size/totalsize*100))
    progressbar(__current_size, totalsize)

def download(ftp, out, filename, blocksize=8192):   
    global __current_size    
    if key in files:
        filesize = ftp.size(filename)
        with open(os.path.join(out, filename), 'wb') as f:   
            callback = functools.partial(write_callback,filesize, f)
            ftp.retrbinary('RETR ' + filename, callback, blocksize=blocksize)
        print('\n')
        __current_size = 0

def LnkTables(tables):
    for key, val in tables.items():
        cps = 'cp -f {0} {1}'.format(os.path.join(Out, key), os.path.join(Path, 'tables', key))
        print(cps)
        os.system(cps)
        if os.path.exists(os.path.join(Out, key)) and val != None:    
            lnk = 'ln -sf {0} {1}'.format(os.path.join(Path, 'tables', key), os.path.join(Path, 'tables', val))
            print(lnk)
            os.system(lnk)

def progressbar(cur, total, width=50):
    percent = cur / total
    sys.stdout.write('\r' + ' ' * (width + 10) + '\r')
    sys.stdout.write('\r')
    sys.stdout.write("{:>4.0%}[{}]".format(percent, 
                    '#'*int(width*percent) + '-'*(width - int(width*percent))))
    sys.stdout.flush()
    time.sleep(0.05)

# download tables
# ftp://garner.ucsd.edu/
if Tables:
    print('Updating tables')
    if (Out == None or not os.path.exists(Out)):
        print('path not exist, we will create this path: {0}'
              .format(Out))
        os.mkdir(Out)
    ftp = connect('132.239.152.183')
    ftp.cwd('/pub/gamit/tables')
    files = ftp.nlst()
    for key, val in tables.items():
        print('updating {0} to {1}'.format(key, Out))
        download(ftp, Out, key)
    if Version < 10.6:
        os.remove(os.path.join(Out, 'svnav.dat.gnss'))
    else:
        os.remove(os.path.join(Out, 'svnav.dat.gps'))
    if Link:
        LnkTables(tables)
    ftp.quit()

# download grids
# ftp://everest.mit.edu
if Grid:
    print('Updating Grids')
    ftp = connect('18.83.0.21')
    ftp.cwd('/pub/GRIDS')
    files = ftp.nlst()
    for key, val in grids.items():
        print('updating {0} to {1}'.format(key, Out))
        download(ftp, Out, key, 5 * 1024)
    ftp.quit()
    # link grids files
    if Link:
        LnkTables(grids)
