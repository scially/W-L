#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
Updating tables file in Gasmit10.x by this py-shell
"""
import ftplib
import sys
import os

def connect(host):
    try:
        ftp = ftplib.FTP(host, user='anonymous', passwd='anonymous')
        ftp.connect()
        ftp.login()
        return ftp
    except:
        print 'FTP is unavailable, pleace check you internet'
        sys.exit(0)


def download(ftp, out, filename, blocksize=2048):
    if key in files:
        with open(os.path.join(out, filename), 'wb') as f:
            ftp.retrbinary('RETR ' + key, f.write, blocksize=blocksize)


if len(sys.argv) == 1:
    print(
        '''
        Updating tables file in Gamit10.x by this py-shell
        Usage: ./sh_update_tables.py -update <y/n> -grid <y/n> -path <gamit> -version <v>
                -year <year> -out <path>
            -link  links updating files to gamit tables [default is n]
                     if -update y ,you should run this py on root
            -grid    download grids [default is n]
            -path    the install path of gamit 
                     if -update n,-path don't need
            -version the version of gamit, fomat of some tables file is different between
                     under 10.6 and 10.6 [default is 10.6]
            -out     on which download tables
        Example: ./sh_update_tables.py -link y -grid n -path /opt/gamit10.6 -version 10.6
                 -year 2017 -out /home/wanghui/Desktop/tables
        ''')
    sys.exit()
Link = False
Grid = False
Path = None
Version = 10.6
year = None
Out = None
for index in range(0, len(sys.argv)):
    if sys.argv[index] == '-link':
        Link = True if sys.argv[index + 1] == 'y' else False
    elif sys.argv[index] == '-grid':
        Grid = True if sys.argv[index + 1] == 'y' else False
    elif sys.argv[index] == '-path':
        Path = sys.argv[index + 1]
    elif sys.argv[index] == '-version':
        Version = float(sys.argv[index + 1])
    elif sys.argv[index] == '-year':
        year = sys.argv[index + 1]
    elif sys.argv[index] == '-out':
        Out = sys.argv[index + 1]
tables = {'pole.usno': 'pole.',
          'ut1.usno': 'ut1.',
          'luntab.%s.J2000' % (year): 'luntab.',
          'soltab.%s.J2000' % (year): 'soltab.',
          'nultab.%s' % (year): 'nultab.',
          'leap.sec': None,
          'gdetic.dat': None,
          'antmod.dat': None,
          'rcvan.dat': None,
          'svnav.dat.gnss': 'svnav.dat',
          'svnav.dat.gps': 'svnav.dat',
          'dcb.dat.gnss': 'dcb.dat',
          'dcb.dat.gps': 'dcb.dat', }
grids = {'otl_FES2004.grid':'otl.grid',
         'vmf1grd.{}'.format(year): 'map.grid',
         'atmdisp_cm.{}'.format(year): 'atml.grid', }

# download tables
# ftp://garner.ucsd.edu/
print '\033[1;31;40mUpdating tables\033[0m'
if (Out == None or not os.path.exists(Out)):
    print 'path not exist, we will create this path: %s' % Out
    os.mkdir(Out)
ftp = connect('132.239.152.183')
ftp.cwd('/pub/gamit/tables')
files = ftp.nlst()
for key, val in tables.items():
    print 'updating %s to %s' % (key, Out)
    download(ftp, Out, key)
ftp.quit()

# download grids
# ftp://everest.mit.edu
if Grid:
    print '\033[1;31;Updating Grids\033[0m'
    ftp = connect('18.83.0.21')
    ftp.cwd('/pub/GRIDS')
    files = ftp.nlst()
    for key, val in grids.items():
        print 'updating %s to %s' % (key, Out)
        download(ftp, Out, key, 5 * 1024)
    ftp.quit()

# link tables files
if Link and Path != None:
    if Version < 10.6:
        os.remove(os.path.join(Out, 'svnav.dat.gnss'))
    else:
        os.remove(os.path.join(Out, 'svnav.dat.gps'))
    for files in os.listdir(Out):
        if os.path.isfile(files):
            cp = 'cp {} {}'.format(os.path.join(Out, files), os.path.join(Path, 'tables', files))
            print cp
            os.system(cp)
    for key, val in tables.items():
        if os.path.exists(os.path.join(Path, 'tables', key)) and val != None:
            lnk = 'ln -sf {} {}'.format(os.path.join(Path, 'tables', key), os.path.join(Path, 'tables', val))
            print lnk
            os.system(lnk)
    for key, val in grids.items():
        if os.path.exists(os.path.join(Path, 'tables', key)) and val != None:
            lnk = 'ln -sf {} {}'.format(os.path.join(Path, 'tables', key), os.path.join(Path, 'tables', val))
            print lnk
            os.system(lnk)
