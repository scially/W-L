## Gamit脚本补充
===
##### by 王会
##### Email:wzxwhd@126.com
##### 2017-6-12
#### update by wanghui 2018-1-3
----
### sh_update_stnfo
解决了在sh_upd_stnfo -files \*.\*o 中提示word too long的问题<br />
但是，脚本是一个一个o文件遍历，速度有点慢，sh_upd_stnfo每<br />
次执行完毕也会sleep 3s，所以导致速度很慢。<br />
### sh_lfile
封装了sh_rx2apr脚本，在rinex目录下运行sh_lfile,将会批量调<br />
用sh_rx2apr，最终生成lfile.apr(新版Gamit的lfile.和Globk的<br />
的apr文件)。<br />
但是没有考虑IGS站，对于IGS站仍然进行单点定位或双差定位得<br />
到先验坐标。<br />
### sh_update_tables
更新Gamit10.x表文件，如果需要进行链接操作，需要你输入root<br />
密码。更新时间在1分钟左右（不包括Grid文件）。<br />
otl.grid是600MB左右，不进行更新。如有需要，请前往mit的<br />
ftp <ftp://everest.mit.edu/pub/GRIDS> 自行下载。<br />
### sh_merge.sh
使用teqc将指定时间段的Rinex文件合并，并根据list文件生成track.cmd<br />
配置文件。<br />
##### 更新说明
本次更改了输出路径，可以在-out后指定输出路径，同时修复了生成
track.cmd的BUG
```shell
./sh_merge.sh -year <year> -doy <doy> -regx <regx> -file <list>
&emsp;&emsp;-out <file>
regx 为bash的正则表达式，这里由使用者提供。
```
##### 要求：
		Rinex文件要符合 SITE[DOY]\*.16[Oo]格式
		list如下：
		|YALD F
		|KATA
		|SITE
		|....
**注：不在只输出GPS卫星数据！会保留所有卫星数据！**

### sh_track_plot.py
使用python3的matplotlib绘制Gamit的track模块的解算结果。<br />
如果你未安装matplotlib，在终端输入：<br />
```shell
sudo pip install matplotlib
```
在其他版本的Linux中，可以前往<http://matplotlib.org/>下载安装<br />
#### 示例
>将该脚本复制到track_res中，在终端中运行
>```shell
>ls *.LC > list
>python3 sh_track_plot.py -out res.png -file <list>
>```
### sh_teqc.sh
对Teqc的封装，可用使用该脚本对指定目录下的指定Rinex文件进行批量Edit
>```shell
>./sh_teqc.sh -file <list> -out <out> -cmd <cmd>
>```
>&emsp;&emsp;-cmd teqc命令
>&emsp;&emsp;-file  待处理的Rinex文件列表，每个文件名占一行，可用ls和重定向生成