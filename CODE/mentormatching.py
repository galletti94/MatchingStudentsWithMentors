import numpy as np
import pandas as pd
import regex as re
import math
import time


coaches = pd.read_csv("../DATA/coaches.csv").fillna('')
students = pd.read_csv("../DATA/students.csv").fillna('')
studentProjectNames = pd.read_csv('../DATA/studentProjectNames.csv', names = ['student', 'project'])
mentees = pd.read_csv('../DATA/Mentee-Application-Form.csv')
mentors = pd.read_csv('../DATA/Mentor-Application-Form.csv')
coachPreferences = pd.read_csv('../DATA/mentorPreferences.csv').fillna('')


def MentorPrefs(coachPrefs, projectNames):
    preferences = []
    for i in range(len(list(coachPrefs.columns))-2):
        mentorProjectInterest = []
        for j in range(len(list(coachPrefs.iloc[:,i]))):
            if len(coachPrefs.iloc[j, i])<3:
                break
            mentorProjectInterest.append(' '.join(re.findall(r'\w+', coachPrefs.iloc[j, i].lower())))
        
        mentorStudentInterest = []
        for j in range(len(mentorProjectInterest)):
            for k in range(len(projectNames.iloc[:, 0])):
                pn = re.findall(r'\w+', projectNames.iloc[k, 1].lower())
                mn = re.findall(r'\w+', mentorProjectInterest[j])
                
                if len(set(pn).intersection(mn)) > 1:
                    mentorStudentInterest.append(projectNames.iloc[k, 0])

        preferences.append(mentorStudentInterest)
    
    for i in range(len(preferences)):
        for j in range(7 - len(preferences[i])):
            preferences[i].append('')

    emails = list(map(lambda x: x.split('@')[0], list(map(lambda x : x.split('(')[1].split(')')[0], list(coachPreferences.columns)))))
    
    names = pd.DataFrame(preferences, index= emails[:len(emails) -2] ).transpose()
    
    return names



def MentorPrefsAddScore(studentPrefs, coachPrefs):

    for i in range(len(list(coachPrefs.columns))):
        coach = list(coachPrefs.columns)[i]
        studentlst = list(coachPrefs.loc[:, coach])
        for j in range(len(studentlst)):
            student = studentlst[j]
            if len(student) < 1:
                break
            restudent = re.findall(r'\w+', student)[0]
            k = 0
            prefs = list(studentPrefs.loc[:, restudent])
            while k < len(prefs) and prefs[k].split('#')[0].lower() != coach.lower():
                k +=1
            if k == len(prefs):
                score = '?'
            else:
                score = prefs[k].split('#')[1]

            if score == '0':
                score = str(9 - j)
            
            coachPrefs.iloc[j, i] = re.findall(r'\w+', coachPrefs.iloc[j, i])[0]+'#'+score
    
    return coachPrefs
            

def match3(coachPrefs, allstudents):
    t = 1
    names = [re.findall(r'\w+', x.split()[0])[0] for x in list(allstudents.iloc[:, 1])]
    d = dict((x, 0) for x in names)
    matching = []
    paired = []
    
    for j in range(len(coachPrefs.index)):

        
        try:
            thestudents = [[x.split('#')[0], int(x.split('#')[1])] for x in list(coachPrefs.iloc[j, :])]
        except IndexError:
            continue
        
    
        while getmaxtuple(thestudents)[1] > 0:

            maxtuple = getmaxtuple(thestudents)
            student = maxtuple[0]
            ind = thestudents.index(maxtuple)
            mentor = coachPrefs.columns[ind]

            print('matching = ', matching)
            if len(matching) == 6:
                break
            
            if d[student] < t and not(mentor in paired):
                d[student] += 1
                matching.append([student, mentor])
                paired.append(mentor)
            
            thestudents[ind][1] = 0

    matching = pd.DataFrame(matching, columns=['student', 'mentor'])
    return matching

def emailToName(coachPrefs, coachMatching):
    emails = list(map(lambda x: x.split('@')[0], list(map(lambda x : x.split('(')[1].split(')')[0], list(coachPrefs.columns)))))
    
    names = list(map(lambda x : x.split('(')[0], list(coachPrefs.columns)))
    

    for i in range(len(list(coachMatching.iloc[:, 1]))):
        for j in range(len(emails)):
            if coachMatching.iloc[i, 1] == emails[j]:
                coachMatching.iloc[i, 1] = names[j]
    
    print(coachMatching)
    return coachMatching
        
    

########################################
##### Identifying feature location #####
########################################

print(len(students))

coachLanguages = [x for x in list(coaches.iloc[1,24:61]) if x != '']
studentLanguages = []
for i in range(3, 8):
    studentLanguages += [x for x in students.iloc[1, i].split(';') if x != '']

c1 = [x for x in list(coaches.iloc[1, 61:67]) if x != '']
c2 = coaches.iloc[1, 23].split()
coachSkills = c1 + c2

s1 = students.iloc[1, 8].split(';')
s2 = students.iloc[1, 9].split(';')
s3 = []
for i in range(len(s2)):
    s3 += s2[i].split()

studentsSkills = [x for x in s1 + s3 if x != '']

print(studentProjectNames)
mentorProjectInterest = []
for i in range(13, 22):
    mentorProjectInterest += re.findall(r'"(.*?)"', coaches.iloc[1, i])

mentorStudentInterest = []
for i in range(len(mentorProjectInterest)):
    for j in range(len(studentProjectNames.iloc[:, 0])):
        if len(set(mentorProjectInterest[i].split()).intersection(studentProjectNames.iloc[j, 1].split())) > 1:
            mentorStudentInterest.append(studentProjectNames.iloc[j, 0])


###############################################
########### end of identification #############
###############################################


def JaccardSim(listA, listB):
    if len(listA) == 0 or len(listB) == 0:
        return 0.0
    return len(set(listA).intersection(listB)) / len(set(listA).union(listB))



def StudentSimilarityMentor(allstudents, allcoaches, t, tupleBinary): #t is parameter descibing similarity function, tupleBinary is whether return only names (0) or tuples with more information (1)
    start = time.time()
    
    similarities = []
    for i in range(len(allstudents)):

        ##########################################
        #### reset similarity list to empty  #####
        #### + find the student languages    #####
        ############  and skills  ################
        ##########################################

        similarity = []
        studentLanguages = []
        for k in range(3, 8):
            studentLanguages += [x for x in allstudents.iloc[i, k].split(';') if x != '']
        
        s1 = allstudents.iloc[i, 8].split(';')
        s2 = allstudents.iloc[i, 9].split(';')
        s3 = []
        for k in range(len(s2)):
            s3 += s2[k].lower().split()
        studentSkills = [x for x in s1 + s3 if x != '']

        for j in range(len(allcoaches)):

            #############################################
            ######## Find and compute similarity ########
            ##### between student i and all mentors #####
            #############################################
            
            coachLanguages = [x for x in list(allcoaches.iloc[j,24:61]) if x != '']
            coachSkills = [x.lower() for x in list(allcoaches.iloc[j, 61:67]) if x != ''] + allcoaches.iloc[j, 23].lower().split()

            jaccardLang = JaccardSim(studentLanguages, coachLanguages)
            jaccardSkill = JaccardSim(studentSkills, coachSkills)

            similarity.append([jaccardSkill, jaccardLang, j])
            
        if t == 'sl':
            similarities.append(list(reversed(sorted([[x[0] + x[1], x[2]] for x in similarity], key = lambda x : x[0]))))
        elif t == 's':
            similarities.append(list(reversed(sorted([[x[0], x[2]] for x in similarity], key = lambda x : x[0]))))
        elif t == 'l':
            similarities.append(list(reversed(sorted([[x[1], x[2]] for x in similarity], key = lambda x : x[0]))))
        else:
            raise ValueError('Wrong tuning parameter')
    

    ###########################################
    ########## sort the similarities ##########
    ##### first by skill then by language #####
    ###########################################

    sims = []
    for i in range(len(similarities)):
        sims.append(list(map(lambda x : x[-1], similarities[i])))

    topics = []
    for i in range(len(similarities)):
        topics.append(list(map(lambda x : allcoaches.iloc[x, 23], sims[i])))
        
    topics = pd.DataFrame(topics, index= list(map(lambda x : x.split()[0], allstudents.iloc[:,1]))).transpose()
            
    titles = []
    for i in range(len(similarities)):
        titles.append(list(map(lambda x : allcoaches.iloc[x, 3], sims[i])))

    titles = pd.DataFrame(titles, index= list(map(lambda x : x.split()[0], allstudents.iloc[:,1]))).transpose()

    if tupleBinary == 0:
        names = []
        for i in range(len(similarities)):
            names.append(list(map(lambda x : allcoaches.iloc[x[-1], 1].split('@')[0], similarities[i])))
            
    elif tupleBinary == 1:
        names = []
        for i in range(len(similarities)):
            names.append(list(map(lambda x : allcoaches.iloc[x[-1], 1].split('@')[0] + '#' +  str(int(x[0]* 10**3)), similarities[i])))
        
    else:
        raise ValueError('Please Enter a tuple parameter of 1 or 0')

    names = pd.DataFrame(names, index= list(map(lambda x : re.findall(r'\w+', x.split()[0])[0], allstudents.iloc[:,1]))).transpose()
    
    end = time.time()
    
    return names


def MentorPreferences(allcoaches, allstudents):
    preferences = []
    for i in range(len(allcoaches)):
        mentorProjectInterest = []
        for j in range(13, 22):
            mentorProjectInterest += re.findall(r'"(.*?)"', coaches.iloc[i, j])

        mentorStudentInterest = []
        for j in range(len(mentorProjectInterest)):
            for k in range(len(studentProjectNames.iloc[:, 0])):
                if len(set(mentorProjectInterest[j].split()).intersection(studentProjectNames.iloc[k, 1].split())) > 1:
                    mentorStudentInterest.append(studentProjectNames.iloc[k, 0])

        preferences.append(mentorStudentInterest)

    names = pd.DataFrame(preferences, index= list(map(lambda x : x.split('@')[0], allcoaches.iloc[:,1]))).transpose()
    
    return names


def FeasibleMatching(studentPreferences, mentorPreferences):
    start = time.time()
    sc = list(studentPreferences.columns)

    for i in range(len(sc)):
        for j in range(len(list(studentPreferences.iloc[:,i]))):
            if sc[i] not in list(mentorPreferences.loc[:, studentPreferences.iloc[j, i]]):
                studentPreferences.iloc[j, i] = ''

    end = time.time()
    
    return studentPreferences



def match1(studentpreferences, allcoaches, t):

    names = [x.split('@')[0] for x in list(allcoaches.iloc[:, 1])]
    d = dict((x, 0) for x in names)
    matching = []
    
    for i in range(len(studentpreferences.columns)):
        
        student = studentpreferences.columns[i]
        
        for j in range(len(studentpreferences.index)):
            
            others = list(studentpreferences.iloc[j, :i]) + list(studentpreferences.iloc[i+1:, j])
            mentor = studentpreferences.iloc[j, i]
            
            if mentor in others:
                if d[mentor] < t:
                    d[mentor] += 1
                    matching.append([mentor, student])
                    break
            else:
                 if d[mentor] < t:
                    d[mentor] += 1
                    matching.append([mentor, student])
                    break

    matching = pd.DataFrame(matching, columns=['mentor', 'student'])
    return matching


def getmaxtuple(lstoflsts):
    res = lstoflsts[0]
    for i in range(1, len(lstoflsts)):
        if lstoflsts[i][1]> res[1]:
            res = lstoflsts[i]
    return res
        

def match2(studentpreferences, allcoaches, t, MenteeNumConstraint):

    names = [x.split('@')[0] for x in list(allcoaches.iloc[:, 1])]
    if MenteeNumConstraint == 0:
        d = dict((x, 0) for x in names)
    elif MenteeNumConstraint == 1:
        yesNo = list(map(lambda x : t if x == 'Yes' else 1, list(allcoaches.iloc[:,4])))
        d = dict()
        for i in range(len(yesNo)):
            if yesNo[i] == 1:
                d[names[i]] = 0
            else:
                d[names[i]] = t - 1
    else:
        raise ValueError('last parameter must be 0 or 1')
    
    matching = []
    paired = []
    
    for j in range(len(studentpreferences.index)):

        mentors = [[x.split('#')[0], int(x.split('#')[1])] for x in list(studentpreferences.iloc[j, :])]
        
        while getmaxtuple(mentors)[1] > 0:

            maxtuple = getmaxtuple(mentors)
            mentor = maxtuple[0]
            ind = mentors.index(maxtuple)
            student = studentpreferences.columns[ind]
            
            if d[mentor] < t and not(student in paired):
                d[mentor] += 1
                matching.append([mentor, student])
                paired.append(student)
            
            mentors[ind][1] = 0

    matching = pd.DataFrame(matching, columns=['mentor', 'student'])
    return matching


def MenteeSimilarityMentor(allmentees, allmentors, t, tupleBinary):
    start = time.time()
    
    similarities = []
    for i in range(len(allmentees)):

        similarity = []
        menteeInterests = str(allmentees.iloc[i, 3]).split(';')
        menteeClubs = str(allmentees.iloc[i, 4]).split(';')

        for j in range(len(allmentors)):

            weight = allmentors.iloc[j, 5]
            if math.isnan(weight):
                weight = 1
            
  
            mentorInterests = str(allmentors.iloc[j, 8]).split(';')
            mentorClubs = str(allmentors.iloc[j, 9]).split(';')

            jaccardInterest = JaccardSim(menteeInterests, mentorInterests)
            jaccardClubs = JaccardSim(menteeClubs, mentorClubs)

            similarity.append([weight * jaccardInterest, weight * jaccardClubs, j])
            
        if t == 'ic':
            similarities.append(list(reversed(sorted([[x[0] + x[1], x[2]] for x in similarity], key = lambda x : x[0]))))
        elif t == 'i':
            similarities.append(list(reversed(sorted([[x[0], x[2]] for x in similarity], key = lambda x : x[0]))))
        elif t == 'c':
            similarities.append(list(reversed(sorted([[x[1], x[2]] for x in similarity], key = lambda x : x[0]))))
        else:
            raise ValueError('Wrong tuning parameter')

    sims = []
    for i in range(len(similarities)):
        sims.append(list(map(lambda x : x[-1], similarities[i])))

    if tupleBinary == 0:
        names = []
        for i in range(len(similarities)):
            names.append(list(map(lambda x : allmentors.iloc[x[-1], 1], similarities[i])))
            
    elif tupleBinary == 1:
        names = []
        for i in range(len(similarities)):
            names.append(list(map(lambda x : allmentors.iloc[x[-1], 1] + '#' +  str(int(x[0])), similarities[i])))
        
    else:
        raise ValueError('Please Enter a tuple parameter of 1 or 0')

    names = pd.DataFrame(names, index= list(allmentees.iloc[:,1])).transpose()
    
    end = time.time()
    
    return names
