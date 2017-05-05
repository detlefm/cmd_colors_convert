
# coding: utf-8

# In[13]:

import sys
import os


prgname = 'minrc2reg'

colornames ={
"Black": "ColorTable08",
"BoldBlack": "ColorTable00",
"Red": "ColorTable12",
"BoldRed": "ColorTable04",
"Green": "ColorTable10",
"BoldGreen": "ColorTable02",
"Yellow": "ColorTable15",
"BoldYellow": "ColorTable06",
"Blue": "ColorTable09",
"BoldBlue": "ColorTable01",
"Magenta": "ColorTable13",
"BoldMagenta": "ColorTable05",
"Cyan": "ColorTable11",
"BoldCyan": "ColorTable03",
"White": "ColorTable07",
"BoldWhite": "ColorTable15" 
} 




#fname = 'mintty_color.txt'

arg1 = 'mintty_color.txt'
arg2 = 'test3.txt'

try:
    __IPYTHON__
    arg1 = './mintty/themes'
except:
    if len(sys.argv)==2:
        arg1 = sys.argv[1]
    else:
        print('usage:',sys.argv[0],'PathOrFilename')
        exit(1)




def convert_line(line):
    l = line.strip()
    if (l.count('=')==1 and l.count(',')==2 
        and not l[0] in '#;'):
        z = l.find('=')
        name = l[:z].strip()
        rgb = [int(x.strip()) for x in l[z+1:].split(',')]
        d = colornames.get(name,None)
        if d:
            return ('"{}"=dword:00{:02X}{:02X}{:02X}'.format(d,*reversed(rgb)))
    return None


    
    
def convert_file(fromfile, tofile, license = []):
    with  open(tofile,'w') as outfile:
        print('Windows Registry Editor Version 5.00',file =outfile);
        print('; generated from '+ prgname,file = outfile)        
        for l in license:
            print('; '+l,file=outfile)
        with open(fromfile) as f:
            for line in f:
                regline = convert_line(line)
                if regline:
                    print(regline,file = outfile)
    print('created '+ tofile)
                    
                    
def file_filter(pathname):
    specialnames = ['LICENSE','downloadfrom.txt']
    if os.path.isfile(pathname) and os.path.getsize(pathname)<1000:
        head, tail = os.path.split(pathname)
        if tail in specialnames or tail.lower().endswith('.reg'):
            return False
        return True
    return False


def get_license(foldername):
    if not os.path.isfile(os.path.join(foldername,'LICENSE')):
        return 'Unknown license, hints welcome'
    return "License see LICENSE file"


def get_takenfrom(foldername):
    takenfrom = ['Unknown source, hints welcome']
    tfile = os.path.join(foldername,'downloadfrom.txt')
    if os.path.isfile(tfile):
        with open(tfile) as lf:
            takenfrom  = lf.readlines()
    return takenfrom

    
    
def compute_folder (foldername):
    files = []
    copyright = get_takenfrom(foldername)
    copyright.append(get_license(foldername))
    for f in os.listdir(foldername):
        pathname = os.path.join(foldername,f)
        destname = os.path.join(foldername,f+'.reg')
        if file_filter(pathname):
            convert_file(pathname,destname, copyright)

            


    
if __name__ == '__main__':
    if os.path.isfile(arg1):
        convert_file(arg1,arg1+'.reg')

    else:
        compute_folder(arg1)


# http://html-color-codes.info/ 
# https://github.com/neilpa/cmd-colors-solarized https://github.com/cmderdev/cmder 
# https://github.com/neilpa/cmd-colors-solarized http://html-color-codes.info/
