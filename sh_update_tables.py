#!/usr/bin/env python
# -*- encoding:utf-8 -*-
"""
Updating tables file in Gasmit10.x by this py-shell
更改链接规则
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
        Usage: ./sh_update_tables.py -link n -grid <y/n> -version <v>
                -year <year> -out <path>
            -link    link the downloading files in tables, this need to root
            -grid    download grids [default is n]
            -version the version of gamit, fomat of some tables file is different between
                     under 10.6 and 10.6 [default is 10.6]
            -out     on which download tables [default is current]
        Example: ./sh_update_tables.py -link y -grid n -version 10.6 -year 2017 
        ''')
    sys.exit()
Link=False
Grid = False
Version = 10.6
year = 2017
Out = os.path.join(os.getcwd(),'tables')
Path=os.getenv('HELP_DIR')
if Path== None:
    print 'Gamit has some errors!'
    sys.exit()
Path=os.path.dirname(os.path.dirname(Path))
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
tables = {'pole.usno': 'pole.',
          'ut1.usno': 'ut1.',
          'luntab.{0}.J2000'.format(year): 'luntab.',
          'soltab.{0}.J2000'.format(year): 'soltab.',
          'nutabl.{0}'.format(year): 'nutabl.',
          'leap.sec': None,
          'gdetic.dat': None,
          'antmod.dat': None,
          'rcvan.dat': None,
          'svnav.dat.gnss': 'svnav.dat',
          'svnav.dat.gps': 'svnav.dat',
          'dcb.dat.gnss': 'dcb.dat',
          'dcb.dat.gps': 'dcb.dat', }
grids = {'otl_FES2004.grid':'otl.grid',
         'vmf1grd.{0}'.format(year): 'vmf1.grid.{0}'.format(year),
         'atmdisp_cm.{0}'.format(year): 'atml.grid.{0}'.format(year), }

# download tables
# ftp://garner.ucsd.edu/
print 'Updating tables'
if (Out == None or not os.path.exists(Out)):
    print 'path not exist, we will create this path: %s' % Out
    os.mkdir(Out)
ftp = connect('132.239.152.183')
ftp.cwd('/pub/gamit/tables')
files = ftp.nlst()
for key, val in tables.items():
    print 'updating {0} to {1}'.format(key, Out)
    download(ftp, Out, key)
ftp.quit()

# download grids
# ftp://everest.mit.edu
if Grid:
    print 'Updating Grids'
    ftp = connect('18.83.0.21')
    ftp.cwd('/pub/GRIDS')
    files = ftp.nlst()
    for key, val in grids.items():
        print 'updating {0} to {1}'.format(key, Out)
        download(ftp, Out, key, 5 * 1024)
    ftp.quit()

if Version < 10.6:
    os.remove(os.path.join(Out, 'svnav.dat.gnss'))
else:
    os.remove(os.path.join(Out, 'svnav.dat.gps'))
# link tables files
if Link:
    for key, val in tables.items():
        if os.path.exists(os.path.join(Out, key)) and val != None:
            cps='sudo cp -f {0} {1}'.format(os.path.join(Out,key),os.path.join(Path,'tables',key))
            lnk = 'sudo ln -sf {0} {1}'.format(os.path.join(Path,'tables', key), os.path.join(Path,'tables',val))
            print cps
            os.system(cps)
            print lnk
            os.system(lnk)
    for key, val in grids.items():
        if os.path.exists(os.path.join(Out,key)) and val != None:
            cps = 'sudo cp -f {0} {1}'.format(os.path.join(Out, key), os.path.join(Path, 'tables', key))
            lnk = 'sudo ln -sf {0} {1}'.format(os.path.join(Path,'tables',key), os.path.join(Path,'tables',val))
            print cps
            os.system(cps)
            print lnk
            os.system(lnk)