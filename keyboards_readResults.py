# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:48:17 2021
@author: Zac C
"""

""" 
DESCRIPTION FOR MR. KLEIN !!!

This program is for the analysis part of my project, where I will be comparing values from results.txt (included) against measurements \
    of the keyboards I'm using, to find correlations between the size of the parts of the keyboards to how well I typed with them.
"""


print("Reading results for 'What Makes A Good Keyboard?' ***\n"+"(keyboards_readResults.py)\n"+"by Zac C\n"+"for 2021 Intro CS")
print()

#Make data lists; make results
dates = []
users = []
boards = []
times = []
wpms = []
errs = []
lens = []
#  Create results as shorthand for data lists
results = []
results.append(dates)
results.append(users)
results.append(boards)
results.append(times)
results.append(wpms)
results.append(errs)
results.append(lens)
#Read results.txt and assign values to data lists
with open('results.txt','r') as f:
    for l in f:
        # split each line of results
        # append splits to data lists
        line = l.split()
        results[0].append(line[0])
        results[1].append(line[1])
        results[2].append(line[2])
        results[3].append(line[3])
        results[4].append(line[4])
        results[5].append(line[5])
        results[6].append(line[6])
    f.close()
#Remove headers from each data list
dates.pop(0)
users.pop(0)
boards.pop(0)
times.pop(0)
wpms.pop(0)
errs.pop(0)
lens.pop(0)
#Parse some lists to floats
for i in range(len(times)): times[i]=float(times[i])
for i in range(len(wpms)): wpms[i]=float(wpms[i])
for i in range(len(errs)): errs[i]=float(errs[i])
for i in range(len(lens)): lens[i]=float(lens[i])
## results is now made and done!
# info can be retrieved from both results a/o the data lists



#Sorting
def sortby(dep, ind, p=False, mode='a'):
    #dep is the list that is to be sorted.   ind is what determines the order of dep.
    #p sets if the results should be printed.   mode sets if dep should be sorted in (a)scending or (d)escending order.
    
    # Sort ind, then find corresponding index in dep list - in ascending order
    indSorted = sorted(ind)
    indexList = [] #holds indexes of keySorted
    for i in range(len(indSorted)):
        for j in range(len(ind)):
            if indSorted[i] == ind[j]:
                indexList.append(j)
    ### print(indexList)
    # Sort dep by ind -- get corresponding value of dep
    final = [] #final list of sorted tuples (ind, dep)
    for i in range(len(dep)):
        final.append( ( indSorted[i], dep[indexList[i]] )) #tuple (ind, dep) is appended to list
    
    #Print sorted lists (opt.)
    if p == True:
        print("DEP sorted in terms of IND")
        print("IND \t|\t DEP")
        for i in range(len(final)):
            print(final[i])
    return final


#Keyboard info
KeyboardInfo = {'dell':( 0, 278, 90, 17, 9, 9, 3, 5, 2.5, 109, 38 ) ,
                'logitech':( 0, 279, 90, 22, 13, 14, 12, 6, 3, 108, 36 ) ,
                'hp1':( 0, 277, 88, 20, 13, 13, 7, 5, 2, 103, 37 ) ,
                'imicro':( 0, 278, 90, 29, 13, 14, 12, 6, 2, 110, 37 ) ,
                'red':( 0, 275, 90, 20, 13, 15, 12, 5, 4, 111, 36 ) ,
                'hp2':( 0, 279, 90, 21, 14, 15, 10, 6, 2, 103, 37 ) }
# b_w, b_l, b_h, k_w, k_l, k_h, k_space, k_travel, space_w, shift_w
dell = [278, 90, 17, 9, 9, 3, 5, 2.5, 109, 38]
logitech = [279, 90, 22, 13, 14, 12, 6, 3, 108, 36]
hp1 = [277, 88, 20, 13, 13, 7, 5, 2, 103, 37]
imicro = [278, 90, 29, 13, 14, 12, 6, 2, 110, 37]
red = [275, 90, 20, 13, 15, 12, 5, 4, 111, 36]
hp2 = [279, 90, 21, 14, 15, 10, 6, 2, 103, 37]

"""
print(sortby(boards, times)[:10])
print(sortby(boards, wpms)[:10])
print(sortby(boards, errs)[:10])
"""

"""
---best score
time = logitech
wpms = logitech
errs = logitech
---most freq out of top 10
time = imicro
wpms = hp1
errs = logitech & imicro

---best board dimentions
time,wpms,errs = [279, 90, 22, 13, 14, 12, 6, 3, 108, 36]
---most freq board dimentions
time = [278, 90, 29, 13, 14, 12, 6, 2, 110, 37]
wpms = [277, 88, 20, 13, 13, 7, 5, 2, 103, 37]
errs =  [279, 90, 22, 13, 14, 12, 6, 3, 108, 36]  \
        [278, 90, 29, 13, 14, 12, 6, 2, 110, 37]
"""

# Best overall board dimentions -- calculated from top 10 most frequent values above
board_width = 278
board_length = 90
board_height = 29
key_width = 13
key_length = 14
key_height = 12
key_space = 6
key_travel = 2
spacebar_width = 110
shift_width = 37
# ^^^ Best overall dimentions for a keyboard



