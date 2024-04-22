import datetime

now = datetime.datetime.now()
f = open('time.txt', 'a')
f.write(f'The current time is: {now}\n')
f.close()