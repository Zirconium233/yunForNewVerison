from main import Yun_For_New
import time
import schedule
def run():
    print("\n\n开始跑步")
    Yun = Yun_For_New(auto_generate_task=False)
    Yun.start()
    Yun.do_by_points_map(random_choose=True)
    Yun.finish_by_points_map()
if __name__ == "__main__":
    # schedule.every(10).minutes.do(run)               # 每隔 10 分钟运行一次 run 函数
    # schedule.every().hour.do(run)                    # 每隔 1 小时运行一次 run 函数
    # schedule.every().day.at("07:30").do(run)         # 每天在 7:30 时间点运行 run 函数
    # schedule.every().monday.do(run)                  # 每周一 运行一次 run 函数
    # schedule.every().wednesday.at("13:15").do(run)   # 每周三 13：15 时间点运行 run 函数
    # schedule.every().minute.at(":17").do(run)        # 每分钟的 17 秒时间点运行 run 函数
    s = input("运行时间：[07:30]")
    if s == "":
        s = "07:30"
    schedule.every().day.at(s).do(run)
    i = 0
    ch = "/"
    while True:
        if i % 4 == 0:
            ch = "/"
        elif i % 4 == 1:
            ch = "-"
        elif i % 4 == 2:
            ch = "\\"
        elif i % 4 == 3:
            ch = "|"
        print(f"第{i}次检查，3秒后下一次检查: {ch}", end="\t")
        print(schedule.get_jobs(), end="\r")
        schedule.run_pending()
        time.sleep(3)
        i += 1
        