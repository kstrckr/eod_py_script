import time
import sys

num = 0

for num in range(10):
    time.sleep(1)
    print('{} Beep!'.format(num))
    num+=1
    sys.stdout.flush()
