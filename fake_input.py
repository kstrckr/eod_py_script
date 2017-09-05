import time
import sys
import random

num = 1

for num in range(1,16):
    time.sleep(random.randint(1, 4)/3)
    print('{} Beep!'.format(num))
    num+=1
    sys.stdout.flush()
