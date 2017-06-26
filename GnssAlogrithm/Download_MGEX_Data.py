import ftplib
import sys
import os
import easygui as gui

def connect(host):
    try:
        ftp = ftplib.FTP(host, user='anonymous', passwd='anonymous')
        ftp.connect()
        ftp.login()
        return ftp
    except:
        gui.msgbox('FTP is unavailable, pleace check you internet!')
        sys.exit(0)
def Hour2alpha(Hour):
    return chr(ord('a')+Hour)
def Year2short(Year):
    return str(int(Year)%100)

def Download_data(Out_file = 'E:\\',data_type='f',Update_Frequency = 'hourly',Version = 'rinex3',Station = 'ebre',Year = '2017',DOY = '175'):
    year = Year2short(Year)
    try:
        if Update_Frequency=='hourly':
            for Hour in range(0, 24):
                hour = Hour2alpha(Hour)
                if (Hour < 10):
                    Url = Url_or + '/' + Update_Frequency + '/' + Version + '/' + Year + '/' + DOY + '/' + '0' + str(Hour)
                else:
                    Url = Url_or + '/' + Version + '/' + Year + '/' + DOY + '/' + str(Hour)
                ftp = connect(ip)
                ftp.cwd(Url)
                # +'/'+Station+DOY+hour+'.'+year+'o'
                filename = Station + DOY + hour + '.' + year + data_type+'.Z'
                files = ftp.nlst()
                if not os.path.exists(os.path.join(Out_file, filename)) and filename in files:  # 这里的not应该不要吧  不在本地文件 同时存在ftp上 才下载
                    with open(os.path.join(Out_file, filename), 'wb') as f:
                        ftp.retrbinary('RETR ' + filename, f.write)
                ftp.quit()
                Url = ''
        elif Update_Frequency=='daily':
            Url=''
    except:
        gui.exceptionbox()
ip='198.118.242.40'
# ip='2001:4d0:241a:442::52'
Url_or='/pub/gps/data/campaign/mgex'

Values=gui.multenterbox(msg='Fill in values for the fields.', title=' ', fields=('DataType','UpdateFrequency','Version','Station','Year','DOY'), values=())


out_path=gui.diropenbox()
Download_data(out_path,Values)