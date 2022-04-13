import os
from time import time, sleep
import datetime
from subprocess import Popen, PIPE, STDOUT


def print_info(stream_url):
    cmd = "ffprobe -hide_banner -i " + stream_url
    p = Popen(cmd, stdout=PIPE)
    p.wait()


def get_record(stream_url):
    cmd = (
        "ffmpeg -y -hide_banner -timeout 50000 -loglevel quiet -i "
        + stream_url
        + " -c copy "
        + "抖音自动录播/"
        + datetime.datetime.now().strftime("%F")
        + "-"
        + datetime.datetime.now().strftime("%T").replace(":", "-")
        + ".mp4"
    )
    return Popen(cmd, stdin=PIPE, stderr=STDOUT)


flv = input("请输入flv源,回车开始录制,Ctrl+C结束录制\n")
print_info(flv)

if not os.path.exists("抖音自动录播"):
    os.mkdir("抖音自动录播")

flag = True
count = 0
while flag:
    try:
        while count < 30:
            pre_time = int(time())
            ff = get_record(flv)
            ff.wait()
            sleep(1)
            if int(time()) - pre_time > 3:
                count = 0
            count += 1
            print("尝试重连%d次" % count)
            if count == 30:
                flag = False
    except:
        ff.communicate(b"q")
        flag = False
print("录制结束")
