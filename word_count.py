import os 
import time

path = os.path.join('examples','hp_full_book.txt')


n = 0
with open(path, 'r') as file:
    list = file.read().split()
    print(len(list))

time.sleep(10)
print("it has been 10 seconds")