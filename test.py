def length_of_period(period):
    if period < 5:
        return 12 * 60
    else:
        return 5 * 60

def calculate_time_at_period(period):
    if period > 5:
        return (720 * 4 + (period - 5) * (5 * 60))
    else:
        return (720 * (period - 1))

def convert_time_to_seconds(row):
    period = row['PERIOD']
    time_str = row['PCTIMESTRING']
    mins, sec = time_str.split(':')
    time_at_start = calculate_time_at_period(period)
    len_of_period = length_of_period(period)
    min_int = int(mins) * 60
    sec_int = int(sec)
    time_elapsed = len_of_period - (min_int + sec_int)
    return time_at_start + time_elapsed


row1 = {'PERIOD': 3, 'PCTIMESTRING': '12:00'} # 2*720
row2 = {'PERIOD': 3, 'PCTIMESTRING': '00:00'} # 3*720
row3 = {'PERIOD': 5, 'PCTIMESTRING': '4:22'} # 4 * 720 + 38


print(convert_time_to_seconds(row1))
print(720*2)
print('\n\n')

print(convert_time_to_seconds(row2))
print(720*3)
print('\n\n')


print(convert_time_to_seconds(row3))
print((720*4)+38)




