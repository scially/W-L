import os,sys
import subprocess as pro
import easygui as gui

def code_smooth_process(infile):
    cname = 'C:\\Users\\dell\\Desktop\\python-小程序\\批量转换3.x到2.11并载波相位平滑伪距\\code_smooth.exe'
    source ='--dt 30 --inputfile '+infile+' --forceCA --smooth --RinexFile '+infile+'_smooth'
    os.system(cname+' '+source)
def convbin_process(infile):
    pname='C:\\Users\\dell\\Desktop\\python-小程序\\批量转换3.x到2.11并载波相位平滑伪距\\convbin.exe'
    source = infile+' -r rinex -y R -y J -y S -f 5 -ho liuqi/liuqi -hc liuqi_edit'
    # p=pro.Popen(pname,stdin=pro.PIPE,stdout=pro.PIPE)
    # result = p.communicate(input=source)
    # res=result[0].decode()
    # print(res)
    # print(pname+' '+source)
    os.system(pname+' '+source)
def walk_dir(dir,topdown=True):
    for root, dirs, files in os.walk(dir, topdown):
        for name in files:
            infile = os.path.join(root , name)
            file_type = infile.split('.')
            if file_type[-1][-1] == 'o':
                convbin_process(infile)
            elif file_type[-1]=='obs':
                code_smooth_process(infile)



path=str(gui.diropenbox('选择文件夹','浏览文件夹','E:\日常记录'))
walk_dir(path)
gui.msgbox('ok')