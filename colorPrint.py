#!/usr/bin/python

# minute period
#> python timeExe.py [yyyymmddhhMMss] [minute]m
#> python timeExe.py 20131017210000 120m

# second period
#> python timeExe.py [yyyymmddhhMMss] [second]
#> python timeExe.py 20131017210000 120


#ffmpeg -t 10 -i mmsh://bcr.media.hinet.net/RA000018 -acodec copy ~/Desktop/fm997_2.wma
# import modules used here -- sys is a very standard one
import sys
import datetime
import time
import os
import re

class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'

def deltaTime(userDT):
    nowDT = datetime.datetime.now()
    deltaDT = userDT - nowDT
    #print 'Start recording at : ' + str(userDT)
    #print '               Now : ' + str(nowDT)
    #print 'Start recording in : ' + str(deltaDT)
    #print (deltaDT).total_seconds()
    return deltaDT.total_seconds()

#20131017210000
def parseArg1(argStr):
    match =re.search(r'^20\d\d(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])([0-1][0-9]|2[0-4])([0-5][0-9])', argStr)
    if match != None:
        d = datetime.date(int(argStr[0:4]), int(argStr[4:6]), int(argStr[6:8]))
        #t = datetime.time(int(argStr[8:10]), int(argStr[10:12]), int(argStr[12:14]))
        t = datetime.time(int(argStr[8:10]), int(argStr[10:12]))
        userDT = datetime.datetime.combine(d, t)
        return userDT
    else:
        print 'Wrong date time format'
        exit(1)
        return None

def parseArg2(argStr):
    if argStr[-1] == 'm': #minute
        period = int(argStr[:-1]) * 60
    else:
        period = int(argStr)
    return period

# Gather our code in a main() function
def main():
    userDT = parseArg1(sys.argv[1])
    d_deltaTime = deltaTime(userDT)
    if d_deltaTime < 0:
        print 'Recording time has passed'
        exit(1)
    
    print bcolors.WARNING + 'Sleep for ' + str(d_deltaTime) + ' second' + bcolors.ENDC
    
    time.sleep( d_deltaTime )
    period = parseArg2(sys.argv[2])
    
    mmsURL = 'mmsh://bcr.media.hinet.net/RA000018'
    stationName = 'fm997'
    saveDir = '/Users/jacky/Music/fm997Record/original'

    #Prevent to sleep
    #commandStr2 = "caffeinate -u -t %d" % (period)
    #print bcolors.WARNING + commandStr2 + bcolors.ENDC
    #os.system(commandStr2)
    #Recording
    commandStr = "ffmpeg -t %d -i %s -acodec copy %s/%s_%s.wma" % \
                (period, mmsURL, saveDir, stationName, sys.argv[1])
    print bcolors.WARNING + commandStr + bcolors.ENDC
    os.system(commandStr)

    print bcolors.WARNING + commandStr + bcolors.ENDC + '\n'
    print bcolors.WARNING + 'Finish Recording \nOriginal file output path:\n%s/%s_%s.wma' % (saveDir, stationName,sys.argv[1])+ bcolors.ENDC

    #Convert to mp3  fm997_201310222137.wma
    commandStr = "ffmpeg -i %s/%s_%s.wma -acodec mp3 -ab 192k %s/%s_%s.mp3" % \
                (saveDir, stationName, sys.argv[1], saveDir, stationName, sys.argv[1])
    os.system(commandStr)
    print bcolors.WARNING + 'Finish Conversion  \nOutput path:\n%s/%s_%s.mp3' % (saveDir, stationName,sys.argv[1])+ bcolors.ENDC
    

    #Sleep
    #print bcolors.WARNING + '\nSleep after 120 second...'+ bcolors.ENDC
    #time.sleep(120)
    

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
