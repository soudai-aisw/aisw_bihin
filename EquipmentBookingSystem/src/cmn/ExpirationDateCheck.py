import datetime
import dev.display.Console as Console

def ExpirationDateCheck(inputdate, maxday):
    try:
        UserIn = datetime.datetime.strptime(inputdate, '%Y/%m/%d')
    except ValueError:
        Console.puts(inputdate + "は無効な日付です。")
        return False

    MinDate = datetime.date.today()
    InputDay = datetime.date(UserIn.year, UserIn.month, UserIn.day)
    LongDay = MinDate + datetime.timedelta(days=maxday)

    if MinDate <= InputDay <= LongDay:
        return True
    else:
        return False

# -----------------------------------------------------------------------------


def __debug_this_module(self):
    str = input('Input Return Day:')
    result = ExpirationDateCheck(str, 90)
    print(result)


if __name__ == "__main__":
    __debug_this_module()