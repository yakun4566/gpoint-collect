import schedule
import time
import arrow

def test1():
    print("test1:" + str(arrow.now().format("YYYY-MM-DD HH:mm:ss")))
    time.sleep(120)

if __name__ == '__main__':
    schedule.every(1).minute.do(test1)

    while True:
        schedule.run_pending()
        time.sleep(1)