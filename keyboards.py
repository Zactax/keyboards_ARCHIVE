# -*- coding: utf-8 -*-
"""
Name: What Makes A Good Keyboard? (keyboards.py)
Auth: Zac C
Date: Created on Mon Feb 15 11:21:18 2021

Language: Python v3.8.XX (32 bit)
Compiler/Editor: Spyder (anaconda3) v4.2.1
* If you have problems running this program, using the above versions of Python and Spyder are recommended *
"""

""" 
GOALS:
    -- Determine which keyboard is best for typing based on highest average wpm and accuracy.
    -- Determine specifications of keyboards that might make typing easier i.e. keyboard width, height off desk, spacebar width.
    -- Determine if any keyboards become easier to type with over time, and if so, find out why.
METHOD:
    -- Conduct trials that test the user's typing speed using different keyboards.
"""


import random
import time as tm    #used to provide current date and time, and to produce pauses in code (doesn't work in pythonw raw executable).



#Print contents of results.txt
def printResults(delays=True):
    #Get data from results.txt
    results = [[],[],[],[],[],[]]
    # [dates],[users],[boards],[times],[wpms],[errs]
    #Read results.txt and assign values to data lists
    filename = 'results.txt'
    with open(filename,'r') as f:
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
        f.close()
    #Remove headers from each data list
    results[0].pop(0)
    results[1].pop(0)
    results[2].pop(0)
    results[3].pop(0)
    results[4].pop(0)
    results[5].pop(0)
    #Parse dates
    dates = [] #list of new completed dates
    for i in range(len(results[0])):  
        cdate = results[0][i] #current date in loop
        #Make parts
        parts = [] #list of parts of a date
        for p in range(4): parts.append(cdate[p*2:(p+1)*2])
        #Append format marks to parts
        parts.insert(1,"/")
        parts.insert(4,":")
        #Make date strings
        dstring = parts[0]+parts[1]+parts[2]+" "+parts[3]+parts[4]+parts[5]
        dates.append(dstring)
    
    #Fancy print
    print("\n\n")
    print("Printing File:",filename)
    if delays==True: tm.sleep(1)
    print("Date\t\t\tUser\t\t\tBoard\t\t\tTime\t\t\tWPM\t\t\tErr")
    for i in range(len(results[0])):
        string = str( dates[i]+"\t\t\t"+results[1][i]+"\t\t\t"+results[2][i]+"\t\t\t"+results[3][i]+"\t\t\t"+results[4][i]+"\t\t\t"+results[5][i] )
        print(string)
        #add a stylistic delay in printing
        if delays==True: tm.sleep(0.01)
    print()
    print("Printed ",str(len(results[0]))," rows.")
    input("Press Enter to continue > ")
    return


#Write contents of results.txt to a backups folder
def backupResults(): 
    print("\n\n")
    print("[ BACKUP RESULTS ]")
    #create custom date string: MMDDHHmmss
    date = ""
    MM = str(tm.localtime()[1])
    if len(MM)==1: 
        MM = str("0"+MM)
    DD = str(tm.localtime()[2])
    if len(DD)==1: 
        DD = str("0"+DD)
    HH = str(tm.localtime()[3])
    if len(HH)==1: 
        HH = str("0"+HH)
    mm = str(tm.localtime()[4])
    if len(mm)==1: 
        mm = str("0"+mm)
    ss = str(tm.localtime()[5])
    if len(ss) == 1:
        ss = str("0"+ss)
    date = MM + DD + HH + mm + ss
    destname = 'backups/%s.txt' % date 
    #read results.txt and write backup
    with open('results.txt','r') as ori:    #ori=original, bu-backup
        with open(destname,'w') as bu:
            bu.write(ori.read()) #write contents of ori to bu
            bu.close()
        ori.close()
    print("~~~ Backup created as '"+date+".txt' at '"+destname+"' \n\n")
    tm.sleep(2)
    return


#Returns error count from user's response
def levenshteinDistance(word1, word2):
    """ 
    Explaination of Levenshtein distance: 
    
    The 'editing distance', or the sum values of operations it takes to change one word to another.
        Definition:
    The Levenshtein distance between two strings a,b (of length |a| and |b| respectively) is given recursively by lev(a,b) where
    lev(a,b) = {|a|                             if |b| = 0
                |b|                             if |a| = 0
                lev(tail(a),tail(b))            if a[0] = b[0]
                1 + min {lev(tail(a),b)         
                         lev(a,tail(b))         
                         lev(tail(a),tail(b))   otherwise.
    where the tail of some string x is a string of all but the first character of x, and x[n] is the nth character of the string x, starting with character 0.
    Note that the first element in the minimum corresponds to deletion (from a to b), the second refers to insertion, and the third to replacement.
    This definition is recursive.
    
    Sources that helped me understand how to figure this out: 
        *) Wikipedia (https://en.wikipedia.org/wiki/Levenshtein_distance)  
        *) Back To Back SWE (https://www.youtube.com/watch?v=MiqoA-yF-0M)  
    """
    
    #Prints the grid of values of distances --used for debugging 
    def levenDist_Print(distances, word1, word2):  
        ##print()
        #print word2 header
        print("     ",end='')
        for w2 in range(len(word2)):
            print(word2[w2],end='  ')
        print()
        #print table and word1 header
        print("  ",end='')
        for w1 in range(len(word1) + 1):
            if w1 >=1: print(word1[w1-1],end=' ')
            for w2 in range(len(word2) + 1):
                if distances[w1][w2] >= 10: #change spacing to make reading easier
                    ending=" "
                else:
                    ending="  "
                print(distances[w1][w2], end=ending)
            print()
        return
    
    # config vars - make sure the words are strings
    word1 = str(word1)
    word2 = str(word2)
    # make a 2-d array w/ dimentions of 1 + lengths of word1 (x) & word2 (y)
    distances = [] #holds distance values
    for i in range(len(word1)+1):
        distances.append([])    #append empty lists
        for j in range(len(word2)+1):
            distances[i].append(0)  #append empty values to empty lists
    # initialize first row and column of array w/ ints starting from 0
    for w1 in range(len(word1)+1): 
        distances[w1][0] = w1
    # initialize first column of distances
    for w2 in range(len(word2)+1): 
        distances[0][w2] = w2
    # the array is set up to have the indexes of each char in each word visible.
    # calculate distances btwn all letters of the two words
    # the distance btwn two letters is calculated based on a 2x2 grid containing 3 known values and 1 missing value.
    """ Key and Understanding:
    VALUES IN THE CASE OF FIRST CHARACTER IN WORDS 'hello' AND 'kelm':
    [w1-1][w2-1] = 0
    [w1-1][w2] = 'h'
    [w1][w2-1] = 'k'
    [w1][w2] = ???. To be calculated.
    
    KEY OF OPERATIONS FOR UNMATCHING CHARACTERS IN 2x2 MATRIX:
     OPERATION NAME:
    |  Replace  |  Insert  | 
    |  Delete   | [TARGET] | 
     VALUES - EX: AT FIRST CHARACTERS OF 'hello' AND 'kelm':
    |   |     |  k  |  (w2-axis -->)
    |   |  0  |  1  |
    | h |  1  | [T] |
    (w1-axis V)
    Val of target = min of operations + 1 (+1 to show that we've done the operation.)
    In this example, the target would be equal to 1, as Replace (val of 0) was chosen, and 1 was added to it.
    """
    for w1 in range(1, len(word1) + 1):
        for w2 in range(1, len(word2) + 1):
            # compare letters of each word one at a time, and assign values to the array
            # if the two chars at end of the two prefixes being compared are equal, the distance is equal to the value of the top left corner of the 2x2 array.
            if (word1[w1-1] == word2[w2-1]):
                distances[w1][w2] = distances[w1-1][w2-1]
            #if chars !=, then distance of current cell is equal to the minimum of the 3 existing values in the 2x2 matrix after adding a cost of 1.
            # | [w1-1][w2-1] | [w1-1][w2] | 
            # |  [w1][w2-1]  |  [w1][w2]  | 
            else:
                d = distances[w1][w2-1] #delete
                i = distances[w1-1][w2] #insert
                r = distances[w1-1][w2-1] #replace
                if (d <= i and d <= r): 
                    distances[w1][w2] = d + 1 #delete
                elif (i <= d and i <= r): 
                    distances[w1][w2] = i + 1 #insert
                else:
                    distances[w1][w2] = r + 1 #replace 
    
    ### levenDist_Print(distances, word1, word2)
    #total distance is at bottom-right corner of distances array and is returned below
    return distances[len(word1)][len(word2)]


#Get average word length of Phrases for super accurate wpms (for wpms in test(), is assumed to be 5)
def get_ave_word_len():
    allWords = [] #list of all words in Phrases
    for l in Phrases:
        words = l.split()
        for w in words:
            allWords.append(w)
    lens = [] #list of the lengths of words
    for w in allWords:
        lens.append(len(w))
    aveLen = int( sum(lens)/len(allWords) ) #the average length
    return aveLen


#Run a practice trial
def practice(): 
    print("\n\n")
    print("\t[ Practice Trial for Data Collection ]")
    # Print directions
    print("To get used to the current keyboard, and to practice and understand how collecting data will work, a sample trial will be run.")
    print("This trial will only include one phrase to copy, and the user will not be asked to input their name or the name of their keyboard.")
    tm.sleep(1)
    print("\n\tDIRECTIONS::")
    print("A sample phrase will be given.")
    print("Copy the phrase as fast as you can, exactly as it is shown.")
    print("The elapsed time from when the sentance is displayed, to when you enter your response, is the time that will be recorded.")
    print("Your words-per-minute and the number of errors in your response will also be recorded.")
    print("A faster time is prefered to a time spent fixing mistakes, so if you make a mistake in your response, please ignore it and continue.")
    print()
    
    input("Press Enter to run sample trial > ")
    
    print("\n~~~ Sample trial start ~~~")
    # Get date
    date = ""
    month = str(tm.localtime()[1])
    if len(month)==1: month = str("0"+month)
    day = str(tm.localtime()[2])
    if len(day)==1: day = str("0"+day)
    hour = str(tm.localtime()[3])
    if len(hour)==1: hour = str("0"+hour)
    minute = str(tm.localtime()[4])
    if len(minute)==1: minute = str("0"+minute)
    date = month + day + hour + minute    
    # Countdown
    print("Starting in ")
    print("3",end=' ')
    tm.sleep(0.5)
    print("2",end=' ')
    tm.sleep(0.5)
    print("1",end=' ')
    tm.sleep(0.5)
    print("Start\n")
    tm.sleep(0.5)
    # TRIAL
    t0 = tm.time()
    phrase = Phrases[int( random.random()*len(Phrases) )] #get phrase
    print("\n______________________________")
    print(phrase)   #prompt
    userIn = input("> ")
    time = round( tm.time()-t0 , 3)      #Get elapsed time
    
    #Return to main() if userIn = 'exit'
    if userIn=='exit':
        print("Exiting to Main Menu")
        return
    
    print("~~~ Sample trial end ~~~")
    # Get data and print, but don't append to results file
    #calc wpm and accuracy
    #gwpm
    words = userIn.split()
    gwpm = round( ((len(words)/5)/time)*60 , 3)
    #accuracy
    err = round( levenshteinDistance(phrase, userIn) , 3)
    practiceData = [date, "p_user", "p_board", time, gwpm, err] #make practiceData
    print()    
    input("Press Enter to continue with data collection > ")
    return


#Swithes to a new user
def user_login(lastusers, flex): 
    #Method of input differs depending on if flex == True
    
    #Allow flexability if flex == True
    if flex==True:
        print("Enter the user name (without spaces).")
        print("\t\t\t(expecting str)")
        username = input("User name > ")
        #Check username against lastusers
        if username not in lastusers:
            lastusers.append(username)
        #go to main() if 'exit' is entered
        elif username=='exit': 
            print("Returning to Main Menu")
            return "exit" 
        else:
            print("!!! That user name has already been used. Please try again")
            user_login(lastusers, True)
    
    #Get names from list if flex == False
    else: 
        while True:
            ##lastboards = []
            print("Enter the user name from the following list:")
            for i in Users:
                if i not in lastusers: print(i,end=' ') #print the list
            print()
            username = str(input("User name > "))
            if (username in Users) and (username not in lastusers):
                lastusers.append(username) #add current username to list of past users
                break #break out of loop upon successful login
            #go to main() if 'exit' is entered
            elif username=='exit': 
                print("Returning to Main Menu")
                return "exit" 
            else:
                print("!!! User name either not valid or user has already tested during this session. Retrying\n")
    return username


#Switches to a new keyboard
def board_login(lastboards, flex): 
    #Method of input differs depending on if flex == True
    
    #Allow flexability if flex == True
    if flex==True:
        print("Enter the name of the keyboard you're using (without spaces).")
        print("\t\t\t(expecting str)")
        boardname = input("Keyboard name > ")
        #Check boardname against lastboards
        if boardname not in lastboards:
            lastboards.append(boardname)
        #go to main() if 'exit' is entered
        elif boardname=='exit': 
            print("Returning to Main Menu")
            return "exit" 
        else:
            print("!!! That keyboard name has already been used. Please try again")
            board_login(lastboards, True)
    
    #Get names from list if flex == False
    else: 
        while True:
            print("Enter the name of a keyboard from the following list", end='')
            if helper==True: print(", or enter 'exit' to exit data collection", end='')
            print(":")
            if helper==True: print("[H] (The only keyboard names available are the ones I'm testing. Don't try to enter your own keyboard name.)")
            print("\n[", end='')
            for i in Boards:
                if i not in lastboards:
                    print(str(i)+", ",end=' ')
            print("]")
            print("\t\t\t(expecting str)")
            boardname = str(input("Keyboard name > "))
            if (boardname in Boards) and (boardname not in lastboards):
                lastboards.append(boardname)
                break
            #go to main() if 'exit' is entered
            elif boardname=='exit': 
                print("Returning to Main Menu")
                return "exit"
            else:
                print("!!! Board name either not in list or board has already been used.")
                print("Keyboards (including ones that may have already been used):", Boards,"\n")
                tm.sleep(1)
    
    return boardname


#Collect data on a keyboard
def test(showDirections=True, flex=False, lastusers=[], lastboards=[]): 
    #showDirections - bool var to dictate if directions are given every time test func is called - either 'True' or 'False' ('True' by default. Enter w/o apostrophes or quotations). 
    #flex - bool var to set the method for which the amount of keyboards is set, and for how board_login func will operate - either 'True' or 'False' ('False' by default. Enter w/o apostrophes or quotations). 
    
    print("\n\n")
    print("\t[ Collect Data ]")
    # Ask to run a Practice trial if helper == True
    if helper == True:
        print("[H] Would you like to run a practice trial to see what a trial of data collection is like? ")
        print("Enter 'y' for yes. \n\t\t\t(expecting str)")
        practiceRun = str(input("> ")).lower()  #Get input and make lowercase
        if practiceRun == 'y':
            practice()
        print("Continuing to data collection")
        tm.sleep(1)
    print()
    
    if showDirections == True:
        print("\tDIRECTIONS::")
        print("For each keyboard you use, you will be asked to type multiple phrases.")
        print("Type the sentence as fast as you can, exactly as it is shown.")
        print("The elapsed time from when the sentance is displayed, to when you enter your response, is the time that will be recorded.")
        print("Your words-per-minute and the number of errors in your response will also be recorded.")
        print("A faster time is prefered to a time spent fixing mistakes, so if you make a mistake in your response, please ignore it and continue.")
        print()
        input("Press Enter to continue > ")     #input pause
        tm.sleep(1)
        print("\n")
    
    #Print value of flex and the significance
    if helper==True: 
        print("[H]: Helper's flex var is: "+str(flex)+". If True, will allow for flexible inputs of user names and keyboard names.")
        print("\t(This isn't too important for you to know, but still important to state.)")
    # Define dependancies of flex
    if flex==True: 
        bLoopLen = input("How many keyboards are you collecting data for? \n\t\t\t(expecting int) \n> ") 
        #go to main() if 'exit' is entered
        if bLoopLen=='exit': 
            print("Returning to Main Menu")
            return 
        else: bLoopLen = int(bLoopLen)
        uLoopLen = input("How many users are you using to collect this data? \n\t\t\t(expecting int) \n> ")
        #go to main() if 'exit' is entered
        if uLoopLen=='exit': 
            print("Returning to Main Menu")
            return 
        else: uLoopLen = int(uLoopLen)
        print()
    else: 
        bLoopLen = len(Boards)
        uLoopLen = len(Users)
    
    #Boards loop
    for b in range(bLoopLen):
        lastusers = []
        board = board_login(lastboards, flex)  #board login
        #Return to main() if 'exit' was inputed in board_login()
        if board=='exit':
            print("Exiting to Main Menu")
            return 
        print()
        lastphrases = []
        # user loop
        ## This loop is no longer useful, as I'm now the only one testing these keyboards
        for u in range(uLoopLen):
            user = user_login(lastusers, flex)   #user login
            #Return to main() if 'exit' was inputed in user_login()
            if user=='exit':
                print("Exiting to Main Menu")
                return 
            times = []
            wpms = []
            errs = []
            print()
            
            #Get formated date string for each user's login
            date = ""
            month = str(tm.localtime()[1])
            if len(month)==1: month = str("0"+month)
            day = str(tm.localtime()[2])
            if len(day)==1: day = str("0"+day)
            hour = str(tm.localtime()[3])
            if len(hour)==1: hour = str("0"+hour)
            minute = str(tm.localtime()[4])
            if len(minute)==1: minute = str("0"+minute)
            date = month + day + hour + minute
            #Coundown
            print(board,":",user,"- data collection will begin in") 
            for i in range(3, 0, -1):
                print(i,end=' ')
                tm.sleep(0.5)
            print("Start \n")
            tm.sleep(0.5)
            
            #Send prompts and recieve input
            lastphrases = []
            while len(lastphrases) < 10:  
                #The number being compared to len(lastphrases) is number of trials to run for each keyboard.
                # A while loop is used to avoid a bug where a phrase was picked but not printed, and the loop continued. 
                #  This would result in a seperator line being printed, but no phrase, and input would not be collected. 
                #   As such, the while loop is used and the seperator line was put inside of the loop. 
                phrase = Phrases[int( random.random()*len(Phrases) )] #get phrase
                #check to make sure a phrase isn't repeated
                if phrase not in lastphrases:
                    lastphrases.append(phrase) 
                    print("\n______________________________")
                    print(phrase)
                    time0 = tm.time() #initial time
                    userIn = input("> ")    # get the user's response
                    time = tm.time()-time0
                    times.append(time) # update times list
                    print()
                    #Return to main() if userIn == 'exit'
                    if userIn=='exit':
                        print("Exiting to Main Menu")
                        return 
                    #Calculate gwpm and error count
                    #gwpm
                    words = userIn.split()
                    aveWordLen = get_ave_word_len()
                    gwpm = ( ( len(words) / aveWordLen) / time )*60
                    #error count
                    errorCount = levenshteinDistance(phrase, userIn)
                    #wpm
                    ### wpm = abs( gwpm - ((errorCount/time)*60) )       #Not to be used. Gives negative floats. Calc gwpm instead
                    wpms.append(gwpm) 
                    errs.append(errorCount)
                    tm.sleep(0.5)
                
                # Set data array and set data2 string
                timeAve = round(sum(times)/len(times),3)
                wpmAve = round(sum(wpms)/len(wpms),3)
                errAve = round(sum(errs)/len(errs),3)
                data = [date, user, board, timeAve, wpmAve, errAve, len(phrase)]
                # make date2 - turns list elements into a string.
                data2 = ""
                for i in data: data2 = data2 + str(i) + " "
                # NOTE: Although the variables being collected are supposed to be averages, for the sake of accuracy, \
                    # all values will be written after each input is recieved. 
                
                #Write data2 to results.txt 
                with open('results.txt','a') as r:
                    r.write(data2 + "\n")
                    r.close()
            
            input("Press Enter to continue > ")
            print("\n")
    # At this point in the function, testing is done for all users. 
    print()
    print("______________________________\n"+
          "   Data Collection Complete   \n"+
          "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n")
    tm.sleep(1)
    return


#Shows menu for navigation before and after testing and other operations
def main(start=None): 
    #start is an var that can be declared when main() is called to run a certain operation immediately.
    if start != None: print("\n~~~ main.start var is:",start)
    if start==1: sel='1'
    elif start==2: sel='2'
    elif start==100: sel='100'
    elif start==200: sel='200'
    elif start==0: sel='0'
    else:
        #print menu select and get user selection
        print("\n\n")
        print("\t[Main Menu]")
        print("Select an action from the list by inputing its corresponding number:")
        print("\t(Ex: To exit the program, input: '0', without quotations or apostrophes.)")
        print("1: Collect data\n"+
              "2: Run a practice trial of data collection\n"+
              "100: Print results\n"+
              "101: Backup results file\n"+
              "0: Exit program")
        if helper == True: print("\t\t\t(expecting int)")
        sel = str( input("> ") )
    
    #Call funcs
    if sel == '1':      # test -- passed in is showDirections (def=True) and flex (def=False) 
        test(True, True)
        main()
    elif sel == '2':    # practice
        practice()
        main()
    elif sel == '100':  # print results
        printResults()
        main()
    elif sel == '101':  # backup results
        backupResults()
        main()
    elif sel == '0':    # exit program
        print("Thank you for using 'keyboards.py', by Zac C ")
        tm.sleep(2)
        raise SystemExit() 
        exit(0) 
        #If raise SystemExit() fails, program will then exit due to intentional error: "name 'exit' is not defined". 
    else:
        #If user inputs an invalid option, the program will alert them and call main function again.
        #(This is why the title is printed outside this loop)
        print("!!! Invalid selection. Was expecting an integer.")
        print("Valid inputs include: 1, 2, 100, 101, 0")
        tm.sleep(3)
        main()
    return "~~~ return from main()"




#Setup variables and Start program
KeyboardInfo = {'dell':( 0, 278, 90, 17, 9, 9, 3, 5, 2.5, 109, 38 ) ,
                'logitech':( 0, 279, 90, 22, 13, 14, 12, 6, 3, 108, 36 ) ,
                'hp1':( 0, 277, 88, 20, 13, 13, 7, 5, 2, 103, 37 ) ,
                'imicro':( 0, 278, 90, 29, 13, 14, 12, 6, 2, 110, 37 ) ,
                'red':( 0, 275, 90, 20, 13, 15, 12, 5, 4, 111, 36 ) ,
                'hp2':( 0, 279, 90, 21, 14, 15, 10, 6, 2, 103, 37 ) ,
                'tuf':( 1, 277, 91, 20, 15.5, 15, 1, 3.5, 1, 91, 39) }   # tuf keyboard is just an example and not to be used
""" Key of KeyboardInfo dict
Boards = {name:(b_type, b_w, b_l, b_h, k_w, k_l, k_h ,k_space ,k_travel ,space_w ,shift_w)}

b_type = type of keyboard (0=mechanical, 1=membrane)
b_w = width from left of CapsLock to right of Enter key
b_l = hight from bottom of Ctrl to top of ` keys
b_h = distance from top of desk to top of Ctrl key, w/ board laying flat
k_w, k_l, and k_h should be dimentions of A key. key_space should be space between A and S keys
k_travel = distance a key much travel to register a keypress

All measurements are in millimeters. Decimal measurements are approximate

0= b_type 
1= b_w 
2= b_l 
3= b_h 
4=   k_w 
5=   k_l 
6=   k_h 
7=   k_space 
8=   k_travel 
9=     space_w 
10=    shift_w 
"""
Users = ['Zac']
Boards = ['Red','HP','tuf' ]
lastusers = [] # for previously logged users and boards in test() 
lastboards = []

#Get phrases from 'phrases.txt'
with open('phrases.txt','r') as f:
    Phrases = []
    for l in f: #for line in file
        #set len of line 1 short to remove enter char
        llen = len(l)-1
        Phrases.append(l[:llen])
    f.close()

#Set helper setting
# helper - bool to dictate if extra text, info, and directions should be printed throughout the program - either 'True' or 'False' \
    # ('True' by default. Should be 'False' for debugging and development of regular functions and operations.)
helper = False



#    TITLE AND BEGINNING 
print("What Makes A Good Keyboard?\n"+"(keyboards.py)\n"+"by Zac C\n"+"for 2021 Intro CS")
print("\n")

# if helper is on, give extra info about project on startup
if helper == True:
    print("[H]: Helper ON -- Extra text, headers, info, and directions will be displayed to make using the program easier (denoted by '[H]').")
    tm.sleep(1)


# call to main func goes on line below ,,,
main()



