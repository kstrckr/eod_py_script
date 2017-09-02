import time
import sys
import random

num = 1

for num in range(1,11):
    time.sleep(random.randint(0, 2))
    print('{} Beep!'.format(num))
    num+=1
    sys.stdout.flush()
