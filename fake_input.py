import time
import sys
import random

num = 1

for num in range(1,251):
    time.sleep(0.1)
    print('{} Beep!'.format(num))
    num+=1
    sys.stdout.flush()
