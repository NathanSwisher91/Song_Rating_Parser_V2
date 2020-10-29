import csv
import os
from collections import Counter
from itertools import groupby
from statistics import stdev


def averageStringFromList(list):
    sumTotal = 0
    for value in list:
        sumTotal = sumTotal + value

    return str(round(sumTotal / len(list), 2))


def averageTotalMostUsedStringsFromList(list):
    sumTotal = 0
    data = Counter(list)
    for value in list:
        sumTotal = sumTotal + value

    average = sumTotal / len(list)
    freqs = groupby(Counter(list).most_common(), lambda x: x[1])
    modes = [val for val,count in next(freqs)[1]]
    return [str(average), str(sumTotal), ', '.join(str(i) for i in modes)]


def averagePointsControversyStringsFromList(list):
    sumTotal = 0
    for value in list:
        sumTotal = sumTotal + value

    average = round(sumTotal / len(list), 2)

    return [str(average), str(sumTotal), str(round(stdev(list), 2))]


def getCompatFromLists(list1, list2):
    compatSum = 0
    i = 0
    for x,y in zip(list1, list2):
        difference = abs(x-y)
        if difference < 5:
            compatSum = compatSum + 1 - (difference * .2)
    return str(round((compatSum / len(list1)) * 100, 2))


def fillOutScoreData(userList):
    scoreDict = {}
    for userInfo in userList:
        score = userInfo[0]
        userName = userInfo[1]
        if score not in scoreDict:
            scoreDict[score] = [userName]
        else:
            scoreDict[score].append(userName)

        scoreDict[score].sort()

    return scoreDict


def fillOutSongData(songDict):
    for songKey, songData in songDict.items():
        scoreList = []
        userInfo = songData['UserInfo']
        userInfo.sort(reverse=True)
        songData['UserInfo'] = userInfo
        for score in userInfo:
            scoreList.append(score[0])

        parsedData = averagePointsControversyStringsFromList(scoreList)
        songData['Average'] = parsedData[0]
        songData['Points'] = parsedData[1]
        songData['Controversy'] = parsedData[2]
        songData['ScoreInfo'] = fillOutScoreData(userInfo)


def createSortedSongListFromDict(songDict):
    songList = []
    for songKey, songData in songDict.items():
        songList.append([float(songData['Average']), float(songData["Controversy"]), songKey])
    songList.sort(key=lambda l: [l[0], -l[1]])
    songPlacement = len(songList)
    for song in songList:
        song[0] = songPlacement
        songPlacement = songPlacement - 1

    return songList


userInfo = {}
songInfo = {}
firstFile = True
with os.scandir('Quarterly_Rating/') as ratings:
    for rating in ratings:
        userName = rating.name[:-4]
        userInfo[userName] = {'AllScores': [], '11': '', '0': ''}

        with open(rating, newline='', encoding='utf-8') as file:
            fileReader = csv.reader(file)
            next(fileReader)
            for row in fileReader:
                month = row[0]
                artist = row[1]
                song = row[2]
                score = row[3]
                comment = row[4]
                link = row[5]

                if firstFile and artist != 'Overall' and artist != 'N/A' and (song + ' - ' + artist) not in songInfo:
                    songInfo[song + ' - ' + artist] = {'Average': 0, 'Points': 0, 'Controversy': 0, 'Link': link,
                                                               'UserInfo': []}

                if score != '':
                    score = int(score)

                if score == 11:
                    userInfo[userName]['11'] = song + ' - ' + artist
                if score == 0:
                    userInfo[userName]['0'] = song + ' - ' + artist

                if artist != 'N/A' and artist != 'Overall':
                    userInfo[userName]['AllScores'].append(score)
                    songInfo[song + ' - ' + artist]['UserInfo'].append([score, userName, comment])
                    if month not in userInfo[userName]:
                        userInfo[userName][month] = []
                        userInfo[userName][month].append(score)
                    else:
                        userInfo[userName][month].append(score)

        if firstFile:
            firstFile = False

fillOutSongData(songInfo)
sortedSongAndArtistList = createSortedSongListFromDict(songInfo)

results = open('Quarterly_Results.txt', 'w', encoding='utf-8')
results.write('11s\n\n')
for userKey, userValue in userInfo.items():
    if userValue['11'] != '':
        results.write(userKey + ': ' + userValue['11'] + '\n')
results.write('\n----------------------\n\n')
results.write('0s\n\n')
for userKey, userValue in userInfo.items():
    if userValue['0'] != '':
        results.write(userKey + ': ' + userValue['0'] + '\n')
results.write('\n----------------------\n\n')

results.write('AVERAGES\n\n')

for userKey, userValue in userInfo.items():
    results.write('__**' + userKey + '**__\n')
    overallAverageInfo = averageTotalMostUsedStringsFromList(userValue['AllScores'])
    averages = []
    for artistKey, artistValue in userValue.items():
        if artistKey != 'AllScores' and artistKey != '11' and artistKey != '0':
            averages.append([averageStringFromList(artistValue), artistKey])
    averages.sort(reverse=True)
    for group in averages:
        results.write('**' + group[1] + ':** ' + group[0] + '\n')
    results.write('\n**Overall Average:** ' + overallAverageInfo[0] + '\n')
    results.write('**Total Points:** ' + overallAverageInfo[1] + '\n')
    results.write('**Most Used Score:** ' + overallAverageInfo[2] + '\n')
    results.write('\n----------------------\n\n')

results.write('\nCOMPATIBILITY\n\n')
overallCompatList = []
for userKey, userValue in userInfo.items():
    user1Scores = userValue['AllScores']
    compatList = []
    for userKey2, userValue2 in userInfo.items():
        if userKey != userKey2:
            user2Scores = userValue2['AllScores']
            compatList.append([getCompatFromLists(user1Scores, user2Scores), userKey2])
    compatList.sort(reverse=True)
    overallCompatList.append([compatList[0][0], userKey, compatList])

overallCompatList.sort()

for userCompat in overallCompatList:
    results.write('__**' + userCompat[1] + '**__\n')
    firstCompat = True
    for compat in userCompat[2]:
        if firstCompat:
            results.write('**' + compat[1] + ':** ' + compat[0] + '% :heart:\n')
            firstCompat = False
        else:
            results.write('**' + compat[1] + ':** ' + compat[0] + '%\n')
    results.write('\n----------------------\n\n')

results.write('\n\nRANKINGS\n\n')
for songOrArtist in sortedSongAndArtistList:
    songPlacement = str(songOrArtist[0])
    songAndArtistTitle = songOrArtist[2]
    artistTitle = songAndArtistTitle.split(' - ')[1]
    songTitle = songAndArtistTitle.split(' - ')[0]

    songRatingInfo = songInfo[songAndArtistTitle]

    results.write('__**' + songPlacement + ') ' + songAndArtistTitle + '**__\n')
    results.write('<' + songRatingInfo['Link'] + '>\n')
    results.write('**Average:** ' + songRatingInfo['Average'] + '\n')
    results.write('**Total Points:** ' + songRatingInfo['Points'] + '\n')
    results.write('**Controversy:** ' + songRatingInfo['Controversy'] + '\n\n')

    results.write('__Scores__\n')
    for scoreValue, scoreUsers in songRatingInfo['ScoreInfo'].items():
        results.write(str(scoreValue) + ' - ' + ', '.join(str(i) for i in scoreUsers) + '\n')

    results.write('\n__Comments__\n')
    for commentInfo in songRatingInfo['UserInfo']:
        if commentInfo[2] != '':
            results.write('**' + commentInfo[1] + ' (' + str(commentInfo[0]) + '):** "' + commentInfo[2] + '"\n')

    results.write('\n----------------------\n\n')

results.close()