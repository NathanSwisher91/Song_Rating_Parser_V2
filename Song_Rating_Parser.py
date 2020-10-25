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


def createSortedSongAndArtistListFromDict(songDict, artistDict):
    songList = []
    for songKey, songData in songDict.items():
        songList.append([songData['Average'], songKey])
    songList.sort()
    songPlacement = len(songList)
    for song in songList:
        song[0] = songPlacement
        songPlacement = songPlacement - 1
    for artist in artistDict.keys():
        lastArtistIndex = -1
        for index, song in enumerate(songList):
            if artist in song[1]:
                lastArtistIndex = index

        songList.insert(lastArtistIndex + 1, [None, artist])

    return songList


def fillOutArtistData(artistName, artistRatingInfo, userInfo):
    scoreList = artistRatingInfo['ScoreList']
    scoreTotal = 0
    for num in scoreList:
        scoreTotal = scoreTotal + num
    average = round(scoreTotal / len(scoreList), 3)
    artistRatingInfo['Average'] = str(average)
    artistRatingInfo['Points'] = str(scoreTotal)
    scoreArtistUserInfo = artistRatingInfo['UserInfo']
    scoreArtistUserInfo.sort(reverse=True)
    artistRatingInfo['ScoreInfo'] = fillOutScoreData(artistRatingInfo['UserInfo'])

    userArtistList = []
    for user in userInfo.keys():
        userAverage = averageStringFromList(userInfo[user][artistName])
        userArtistList.append([userAverage, user])
        i = 0
        for artistUser in artistRatingInfo['UserInfo']:
            if artistUser[1] == user:
                artistRatingInfo['UserInfo'][i] = [userAverage, artistUser[1], artistUser[0], artistUser[2]]
            i = i + 1

    artistRatingInfo['UserInfo'].sort(reverse=True)

    userArtistList.sort(reverse=True)
    index = 0
    lastAverage = ''
    biggestFanString = ''
    for userAverage in userArtistList:
        if index < 3 or userAverage[0] == lastAverage:
            biggestFanString = biggestFanString + userAverage[1] + ' (' + userAverage[0] + '), '
            index = index + 1
            lastAverage = userAverage[0]
    artistRatingInfo['Biggest Fans'] = biggestFanString[:-2]

    userArtistList.sort()
    index = 0
    lastAverage = ''
    biggestAntiString = ''
    for userAverage in userArtistList:
        if index < 3 or userAverage[0] == lastAverage:
            biggestAntiString = biggestAntiString + userAverage[1] + ' (' + userAverage[0] + '), '
            index = index + 1
            lastAverage = userAverage[0]
    artistRatingInfo['Biggest Antis'] = biggestAntiString[:-2]

    print(artistName)
    print(artistRatingInfo)



userInfo = {}
artistInfo = {}
songInfo = {}
firstFile = True
with os.scandir('Rating/') as ratings:
    for rating in ratings:
        userName = rating.name[:-4]
        userInfo[userName] = {'AllScores': []}

        with open(rating, newline='', encoding='utf-8') as file:
            fileReader = csv.reader(file)
            next(fileReader)
            for row in fileReader:
                artist = row[0]
                songOrArtist = row[1]
                score = row[2]
                comment = row[3]
                link = row[4]

                if firstFile and songOrArtist != 'Overall' and songOrArtist != 'N/A' and (songOrArtist + ' - ' + artist) not in songInfo:
                    songInfo[songOrArtist + ' - ' + artist] = {'Average': 0, 'Points': 0, 'Controversy': 0, 'Link': link,
                                                               'UserInfo': []}
                elif firstFile and artist not in artistInfo:
                    artistInfo[artist] = {'Average': '0', 'Points': '0', 'Biggest Fans': '',
                                          'Biggest Antis': '', 'Songs': [], 'UserInfo': [], 'ScoreInfo': {},
                                          'ScoreList': []}


                if score != '':
                    score = int(score)

                if songOrArtist == 'Overall':
                    artistInfo[artist]['UserInfo'].append([score, userName, comment])
                elif songOrArtist != 'N/A':
                    userInfo[userName]['AllScores'].append(score)
                    songInfo[songOrArtist + ' - ' + artist]['UserInfo'].append([score, userName, comment])
                    if artist not in userInfo[userName]:
                        userInfo[userName][artist] = []
                        userInfo[userName][artist].append(score)
                    else:
                        userInfo[userName][artist].append(score)
                else:
                    if artist in artistInfo:
                        del artistInfo[artist]
                    if artist in userInfo[userName]:
                        del userInfo[userName][artist]

        if firstFile:
            firstFile = False

print(userInfo)
fillOutSongData(songInfo)
sortedSongAndArtistList = createSortedSongAndArtistListFromDict(songInfo, artistInfo)

results = open('Results.txt', 'w', encoding='utf-8')
results.write('AVERAGES\n')

for userKey, userValue in userInfo.items():
    results.write('__**' + userKey + '**__\n')
    overallAverageInfo = averageTotalMostUsedStringsFromList(userValue['AllScores'])
    averages = []
    for artistKey, artistValue in userValue.items():
        if artistKey != 'AllScores':
            averages.append([averageStringFromList(artistValue), artistKey])
    averages.sort(reverse=True)
    for group in averages:
        results.write('**' + group[1] + ':** ' + group[0] + '\n')
    results.write('**Overall Average:** ' + overallAverageInfo[0] + '\n')
    results.write('**Total Points:** ' + overallAverageInfo[1] + '\n')
    results.write('**Most Used Score:** ' + overallAverageInfo[2] + '\n')
    results.write('----------------------\n')

results.write('\n\nCOMPATIBILITY\n')
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
    results.write('----------------------\n')

results.write('\n\nRANKINGS\n')
for songOrArtist in sortedSongAndArtistList:
    if songOrArtist[0] is None:
        artistName = songOrArtist[1]
        artistRatingInfo = artistInfo[artistName]
        artistSongList = artistRatingInfo['Songs']
        artistSongList.sort()
        fillOutArtistData(artistName, artistRatingInfo, userInfo)


        results.write('__**' + artistName + '**__\n')
        results.write('**Overall Average:** ' + artistRatingInfo['Average'] + '\n')
        results.write('**Total Points:** ' + artistRatingInfo['Points'] + '\n')

        results.write('**Biggest Fans:** ' + artistRatingInfo['Biggest Fans'] + '\n')
        results.write('**Biggest Antis:** ' + artistRatingInfo['Biggest Antis'] + '\n\n')

        results.write('__Rankings__\n')
        for songRanking in artistSongList:
            results.write(songRanking[0] + ') ' + songRanking[1] + '\n')

        results.write('\n__Scores__\n')
        for scoreValue, scoreUsers in artistRatingInfo['ScoreInfo'].items():
            results.write(str(scoreValue) + ' - ' + ', '.join(str(i) for i in scoreUsers) + '\n')

        results.write('\n__Comments__\n')
        for commentRanking in artistRatingInfo['UserInfo']:
            if commentRanking[3] != '':
                results.write('**' + commentRanking[1] + ' (' + str(commentRanking[0] + '):** "' + commentRanking[3] + '"\n'))
        results.write('\n\n')
    else:
        songPlacement = str(songOrArtist[0])
        songAndArtistTitle = songOrArtist[1]
        artistTitle = songAndArtistTitle.split(' - ')[1]
        songTitle = songAndArtistTitle.split(' - ')[0]

        if artistTitle in artistInfo:
            artistInfo[artistTitle]['Songs'].append([songPlacement, songTitle])

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
            if artistTitle in artistInfo:
                artistInfo[artistTitle]['ScoreList'].append(commentInfo[0])
            if commentInfo[2] != '':
                results.write('**' + commentInfo[1] + ' (' + str(commentInfo[0]) + '):** "' + commentInfo[2] + '"\n')

        results.write('\n----------------------\n\n')

results.close()