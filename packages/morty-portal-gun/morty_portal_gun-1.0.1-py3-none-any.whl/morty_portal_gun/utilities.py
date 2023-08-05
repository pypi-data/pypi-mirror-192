import datetime


def time():
    result = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return str(result)

def sha256():
    return "hi"