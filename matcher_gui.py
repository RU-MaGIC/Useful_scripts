import filecmp
import tkinter
from tkinter import *
from tkinter import filedialog

def print_diff(dcmp):
    #Print out the files that are different
    diffs=[]
    def differ(dcmp):
        for name in dcmp.diff_files:
            print('diff_file %s found to be different between %s and %s' %(name, dcmp.left, dcmp.right))
            diffs.append('diff_file %s found to be different between %s and %s' %(name, dcmp.left, dcmp.right))

        #Print out the ones only in the first directory
        for name in dcmp.left_only:
            print('%s found in %s only' %(name, dcmp.left))
            diffs.append('%s found in %s only' %(name, dcmp.left))

        #Print out the ones only in the second directory
        for name in dcmp.right_only:
            print('%s found in %s only' %(name, dcmp.right))
            diffs.append('%s found in %s only' %(name, dcmp.right))

        #Continue for all subdirectories
        for sub_dcmp in dcmp.subdirs.values():
            differ(sub_dcmp)
    differ(dcmp)

    with open('./differences.txt','w') as file:
        for item in diffs:
            file.write('%s\n' % item)

        file.close()
        
    window=tkinter.Toplevel(background='coral')
    window.title('Difference list')
    basemessage=tkinter.Message(window,background='coral', font=('Helvetica',14),text='''
Differences have been calculated between %s and %s.  There are %s differences identified across the directories.
These will be saved in the current working directory as 'differences.txt'

''' % (dcmp.left, dcmp.right, str(len(diffs))))
    basemessage.pack()
    baseexit=tkinter.Button(window,font=('Helvetica',14),text='Click here to Exit',command=window.destroy)
    baseexit.pack()

def folder1():
    Tk().withdraw()
    global dirname1
    dirname1=filedialog.askdirectory()
    if len(dirname1)>0:
        print(dirname1)
        return(dirname1)

def folder2():
    Tk().withdraw()
    global dirname2
    dirname2=filedialog.askdirectory()
    if len(dirname2)>0:
        print(dirname2)
        return(dirname2)

def fin():
    print(dirname1, dirname2)
    dcmp=filecmp.dircmp(dirname1,dirname2)
    print_diff(dcmp)

basegui=tkinter.Tk()
basegui.config(background='SeaGreen2')
basegui.title('Please choose your function')
label=tkinter.Label(basegui,text='''
Welcome to the quick program to check the differences between your directories. 

Please choose your two directories of comparison, then hit execute.
Make sure you actually select the folder and enter it!
''', font=('Helvetica',16), background='SeaGreen2')
label.pack()



folder1button=tkinter.Button(basegui,width=60,background='orchid1',font=('Helvetica',14),text='Choose your first folder', command=folder1)
folder1button.pack()
folder2button=tkinter.Button(basegui,width=60,background='orchid1',font=('Helvetica',14),text='Choose your second folder', command=folder2)
folder2button.pack()
finbutton=tkinter.Button(basegui,width=60,background='orchid1',font=('Helvetica',14),text='Execute', command=fin)
finbutton.pack()

exitbutton=tkinter.Button(basegui,font=('Helvetica',14), text='Click here to Exit', command=basegui.destroy)
exitbutton.pack()


if __name__=='__main__':
    basegui.mainloop()
                             
