import time


def write_txt(filename, str):
    txt = open(filename, mode="w", encoding="utf-8")
    txt.write(str)
    txt.close()

def read_txt(filename):
    txt = open(filename, mode="r", encoding="utf-8")
    t = txt.read()
    txt.close()
    return t

if __name__ == '__main__':
    for i in range(0, 20):
        write_txt(filename="../const/hour_last_time", str=str(time.time()))
        s = read_txt(filename="../const/hour_last_time")
        print(s)
        time.sleep(1)