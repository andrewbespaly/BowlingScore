import os
from tabulate import tabulate
import keyboard
import time

def main():

    while(True):
        #keyboard.wait("a")
        os.system('cls')
        print(keyboard.read_key())
        time.sleep(0.5)
    


if __name__ == "__main__":
    main()