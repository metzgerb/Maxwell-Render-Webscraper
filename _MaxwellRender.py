import requests
import re
import os
from datetime import datetime

def get_filename_from_cd(cd):
    """
    Get filename from content-disposition
    """
    if not cd:
        return None
    fname = re.findall('filename=(.+)', cd)
    if len(fname) == 0:
        return None
    return fname[0]

starttime = datetime.now()    
#set header for user agent
useragent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
#check if range should be specified
userinput = input('Do you want to specify your own range of IDs (y/n): ')

if(userinput == 'n'):
    #check for highest number by looking through image folders
    
    print("Locating largest ID...")
    minnumber = 1
    maxnumber = 0
    for k in range(7000,0,-1):
        url = 'http://www.maxwellrender.com/materials/static/mxmaterials/img/' + "/".join(str(k)) + '/'
        r = requests.head(url, headers = useragent)
        if (r.status_code == requests.codes.ok):
            maxnumber = k
            break
    
    print("Largest ID: " + str(maxnumber))
    endtime = datetime.now()
    print("Time to find largest ID: " + str(endtime - starttime))

else:
    minnumber = int(input('Enter smallest ID to check: '))
    maxnumber = int(input('Enter largest ID to check: '))

#get current directory
destination = os.getcwd()
filecount = 0
dlstart = datetime.now()

#loop through urls and check for no files
for x in range(minnumber,maxnumber+1):
    #attempt to access
    print('Attempting ID: ' + str(x))
    url = 'http://materia.maxwellrender.com/API/v1/download/material/' + str(x)
    r = requests.get(url, headers = useragent, allow_redirects=True)
    
    #get filename
    filename = get_filename_from_cd(r.headers.get('content-disposition'))
    
    #check if filename exists
    if(filename):    
        filename = filename.strip('\"')
        print('Found: ' + filename)
        filename = destination + '\\' + str(x).rjust(4,'0') + '__' + filename
        
        #save file to current directory
        open(filename, 'wb').write(r.content)
        #increment file counter
        filecount+=1
        
dlend = datetime.now()
#print completion message
print('Complete: ' + str(filecount) + ' file(s) downloaded.')
print("Time to download: " + str(dlend - dlstart))
print("Total Time: " + str(dlend - starttime))
