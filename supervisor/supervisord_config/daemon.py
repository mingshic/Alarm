#!/usr/bin/env python3
  
import flask

import time  
import os  
def run():
    while True:  
        time.sleep(1)  
        f=open("log",'a')  
        t=time.time()  
        f.write(str(t))  
        f.write("\n")  
        f.close() 

if __name__ == "__main__":
    run()
