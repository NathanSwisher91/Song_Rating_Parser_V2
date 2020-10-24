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


def fillOutArtistData(artistName, artistRatingInfo):
    print(artistName)
    print(artistRatingInfo)
    scoreList = artistRatingInfo['ScoreList']
    scoreTotal = 0
    for num in scoreList:
        scoreTotal = scoreTotal + num
    average = round(scoreTotal / len(scoreList), 3)
    artistRatingInfo['Average'] = str(average)
    artistRatingInfo['Points'] = str(scoreTotal)



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

                if firstFile and songOrArtist != 'Overall' and songOrArtist != 'N/A' and (songOrArtist + ' - ' + artist) not in songInfo:
                    songInfo[songOrArtist + ' - ' + artist] = {'Average': 0, 'Points': 0, 'Controversy': 0, 'UserInfo': []}
                elif firstFile and artist not in artistInfo:
                    artistInfo[artist] = {'Average': '0', 'Points': '0', 'Biggest Fans': '',
                                          'Biggest Antis': '', 'Songs': [], 'UserInfo': [], 'ScoreInfo': [],
                                          'CommentInfo': [], 'ScoreList': []}


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
        fillOutArtistData(artistName, artistRatingInfo)


        results.write('__**' + artistName + '**__\n')
        results.write('**Overall Average:** ' + artistRatingInfo['Average'] + '\n')
        results.write('**Total Points:** ' + artistRatingInfo['Points'] + '\n')
        results.write('**Controversy:** ' + artistRatingInfo['Controversy'] + '\n\n')

        results.write('**Biggest Fans:** ' + artistRatingInfo['Biggest Fans'] + '\n')
        results.write('**Biggest Antis:** ' + artistRatingInfo['Biggest Antis'] + '\n\n')

        results.write('__Rankings__\n')
        for songRanking in artistSongList:
            results.write(songRanking[0] + ') ' + songRanking[1] + '\n')

        results.write('\n__Scores__\n')
        for scoreRanking in artistRatingInfo['ScoreInfo']:
            results.write(scoreRanking[0] + ' - ' + scoreRanking[1] + '\n')

        results.write('\n__Comments__\n')
        for commentRanking in artistRatingInfo['CommentInfo']:
            if commentRanking[2] != '':
                results.write('**' + commentRanking[1] + ' (' + str(commentRanking[0] + '):** "' + commentRanking[2] + '"\n'))
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

#######################################################################################

with open('Averages.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        averages.append(row)

average_list = []
for average_fields in averages:
    if average_fields[0] == '':
        pass
    elif average_fields[1] == '':
        results.write('__**' + average_fields[0] + '**__\n')
        average_list = []
    elif average_fields[0].strip() == 'Average':
        average_list.sort(reverse=True)
        for group in average_list:
            results.write('**' + group[1] + ':** ' + str(round(float(group[0]), 2)) + '\n')
        results.write('\n')
        results.write('**Overall Average:** ' + average_fields[1] + '\n')
    elif average_fields[0].strip() == 'Mode':
        results.write('**Most Used Score:** ' + average_fields[1] + '\n')
        results.write('----------------------\n')
    else:
        average_list.append([average_fields[1], average_fields[0]])


results.write('\n\nCOMPATIBILITY\n')

compatibility = []

with open('Compatibility.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        compatibility.append(row)

comp = []
individual_comp_list = []
index = -1
for compatibility_fields in compatibility:
    if compatibility_fields[0] == '':
        pass
    elif compatibility_fields[1] == '':
        if individual_comp_list:
            individual_comp_list.sort(reverse=True)
            comp[index].insert(0, float(individual_comp_list[0][0]))
            comp[index].append('**' + individual_comp_list[0][2] + ':** ' + str(individual_comp_list[0][0]) + '% :heart:\n')
            for ind_comp in individual_comp_list[1:]:
                comp[index].append('**' + ind_comp[2] + ':** ' + str(ind_comp[0]) + '% \n')
        individual_comp_list = []
        index = index + 1
        comp.append(['__**' + compatibility_fields[0] + '**__\n'])
    else:
        individual_comp_list.append([float(compatibility_fields[1][:-1]), compatibility_fields[2], compatibility_fields[0]])

if individual_comp_list:
    individual_comp_list.sort(reverse=True)
    comp[index].insert(0, float(individual_comp_list[0][0]))
    comp[index].append('**' + individual_comp_list[0][2] + ':** ' + str(individual_comp_list[0][0]) + '% :heart:\n')
    for ind_comp in individual_comp_list[1:]:
        comp[index].append('**' + ind_comp[2] + ':** ' + str(ind_comp[0]) + '% \n')

comp.sort()

for element in comp:
    iterated_elements = iter(element)
    next(iterated_elements)
    for line in iterated_elements:
        results.write(line)
    results.write('\n')

results.write('\nRANKINGS\n\n')

overall = []

with open('Overall.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        overall.append(row)

comments = []

with open('Comments.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        comments.append(row)

rating_list = []
artist_list = []
artist_scores = []

first_line = True
for overall_fields, comments_fields in zip(overall, comments):
    if first_line:
        overall_header = overall_fields
        comments_header = comments_fields
        first_line = False
    elif overall_fields[0] != '' and overall_fields[1] == '':
        if '{' in overall_fields[0]:
            current_group = overall_fields[0].split('{')[0]
            number_of_songs = overall_fields[0].split('{', 1)[1].split('}')[0]
            i = 4
            for score in overall_fields[4:]:
                if score != '':
                    artist_scores.append([int(score), overall_header[i]])
                i = i + 1
            artist_scores.sort(key=lambda l: [-l[0], l[1].lower()])
        else:
            current_group = ''
            number_of_songs = 1
    elif overall_fields[0].strip() == 'Total':
        artist = [round(float(overall_fields[1]), 3), round(float(overall_fields[3]), 2), current_group, overall_fields[2], artist_scores]
        ratings = []
        for rating, name in zip(overall_fields[4:], overall_header[4:]):
            if name != '':
                ratings.append([round(float(rating)/float(number_of_songs), 2), name, comments_fields[comments_header.index(name)]])
        ratings.sort(key=lambda l: [-float(l[0]), l[1].lower()])
        artist.append(ratings)
        artist_list.append(artist)
        artist_scores = []
    elif overall_fields[0].strip() == 'N/A':
        pass
    elif overall_fields[0].strip() == 'Final Thoughts':
        pass
    else:
        songOrArtist = [round(float(overall_fields[1]), 2), round(float(overall_fields[3]), 2), overall_fields[0], current_group, overall_fields[2]]
        ratings = []
        for rating, name in zip(overall_fields[4:], overall_header[4:]):
            if name != '':
                ratings.append([rating, name, comments_fields[comments_header.index(name)]])
        ratings.sort(key=lambda l: [-float(l[0]), l[1].lower()])
        songOrArtist.append(ratings)
        rating_list.append(songOrArtist)

rating_list.sort(key=lambda l: [l[0], -l[1]])
rank = len(rating_list)
for rating in rating_list:
    rating.insert(0, rank)
    rank = rank - 1

pre_fan_anti_section = True
first_line = True
ratings = []
for overall_fields in overall:
    if not pre_fan_anti_section:
        if first_line:
            artist_name = overall_fields[0].strip()
            fandom_name = overall_fields[1]
            ratings = []
            first_line = False
        elif overall_fields[0] == '':
            first_line = True
            for artist in artist_list:
                if artist[2].strip().lower() == artist_name.lower():
                    biggest_fans = '**Biggest ' + fandom_name + 's:** '
                    biggest_antis = '**Biggest Antis:** '

                    ratings.sort(key=lambda l: [-l[1], l[0].lower()])

                    biggest_fans = biggest_fans + ratings[0][0] + ' (' + str(ratings[0][1]) + '), '
                    biggest_fans = biggest_fans + ratings[1][0] + ' (' + str(ratings[1][1]) + '), '
                    biggest_antis = biggest_antis + ratings[len(ratings) - 1][0] + ' (' + str(
                        ratings[len(ratings) - 1][1]) + '), '
                    biggest_antis = biggest_antis + ratings[len(ratings) - 2][0] + ' (' + str(
                        ratings[len(ratings) - 2][1]) + '), '

                    fan_score = ratings[2][1]
                    anti_score = ratings[len(ratings) - 3][1]

                    for rating in ratings[2:]:
                        if rating[1] == fan_score:
                            biggest_fans = biggest_fans + rating[0] + ' (' + str(rating[1]) + '), '

                    ratings.sort(key=lambda l: [l[1], l[0].lower()])
                    for rating in ratings[2:]:
                        if rating[1] == anti_score:
                            biggest_antis = biggest_antis + rating[0] + ' (' + str(rating[1]) + '), '

                    biggest_fans = biggest_fans[:-2]
                    biggest_antis = biggest_antis[:-2]
                    artist.append(biggest_fans)
                    artist.append(biggest_antis)
        else:
            ratings.append([overall_fields[0], round(float(overall_fields[1]), 2)])
    if overall_fields[0].strip() == 'Biggest Fans/Antis':
        pre_fan_anti_section = False

try:
    for artist in artist_list:
        if artist[2].strip().lower() == artist_name.lower():
            biggest_fans = '**Biggest ' + fandom_name + 's:** '
            biggest_antis = '**Biggest Antis:** '

            ratings.sort(key=lambda l: [-l[1], l[0].lower()])

            biggest_fans = biggest_fans + ratings[0][0] + ' (' + str(ratings[0][1]) + '), '
            biggest_fans = biggest_fans + ratings[1][0] + ' (' + str(ratings[1][1]) + '), '
            biggest_antis = biggest_antis + ratings[len(ratings)-1][0] + ' (' + str(ratings[len(ratings)-1][1]) + '), '
            biggest_antis = biggest_antis + ratings[len(ratings)-2][0] + ' (' + str(ratings[len(ratings)-2][1]) + '), '

            fan_score = ratings[2][1]
            anti_score = ratings[len(ratings) - 3][1]

            for rating in ratings[2:]:
                if rating[1] == fan_score:
                    biggest_fans = biggest_fans + rating[0] + ' (' + str(rating[1]) + '), '

            ratings.sort(key=lambda l: [l[1], l[0].lower()])
            for rating in ratings[2:]:
                if rating[1] == anti_score:
                    biggest_antis = biggest_antis + rating[0] + ' (' + str(rating[1]) + '), '

            biggest_fans = biggest_fans[:-2]
            biggest_antis = biggest_antis[:-2]
            artist.append(biggest_fans)
            artist.append(biggest_antis)
except NameError:
    pass

reversed_song_list = sorted(rating_list)

for artist in artist_list:
    artist.insert(0, artist.pop(2))
    last_index = -1
    for songOrArtist in rating_list:
        if songOrArtist[4] == artist[0]:
            last_index = rating_list.index(songOrArtist)
    rating_list.insert(last_index+1, artist)

# EACH SONG OBJECT
# [rating, average, controversy, song name, group name, total, [[score1, name1, comment1, ....]]

# EACH ARTIST OBJECT
# [group name, average, controversy, total, [[score, name],...][[average, name, comment]...], 'BIGGEST FAN INFO STRING',
# 'BIGGEST ANTI INFO STRING']

for rating in rating_list:
    if isinstance(rating[0], int):
        song_link = None
        if '{' in rating[3]:
            song_link = rating[3].split('{', 1)[1].split('}')[0]
            song_name = rating[3].split('{')[0]
        else:
            song_name = rating[3]
        results.write('__**' + str(rating[0]) + ') ' + song_name + ' - ' + rating[4] + '**__\n')
        if song_link is not None:
            results.write('<' + song_link + '>\n')
        results.write('**Average:** ' + str(rating[1]) + '\n')
        results.write('**Total Points:** ' + str(rating[5]) + '\n')
        results.write('**Controversy:** ' + str(rating[2]) + '\n\n')
        results.write('__Scores__')

        last_used_score = -1
        score_string = ''
        for score in rating[6]:
            if score[0] == last_used_score:
                score_string = score_string + score[1] + ', '
                pass
            else:
                score_string = score_string[:-2]
                results.write(score_string)
                last_used_score = score[0]
                score_string = '\n' + str(last_used_score) + ' - ' + score[1] + ', '

        score_string = score_string[:-2]
        results.write(score_string)

        results.write('\n\n__Comments__\n')
        for score in rating[6]:
            if score[2] != '':
                results.write('**' + score[1] + ' (' + str(score[0]) + '):** "' + score[2] + '"\n')

        results.write('\n---------------------\n\n')
    else:
        results.write('\n\n')
        results.write('__**' + rating[0] + '**__\n')
        results.write('**Overall Average:** ' + str(rating[1]) + '\n')
        results.write('**Total Points:** ' + str(rating[3]) + '\n\n')
        results.write(rating[6] + '\n')
        results.write(rating[7] + '\n')
        results.write('\n__Rankings__\n')

        for songOrArtist in reversed_song_list:
            if songOrArtist[4] == rating[0]:
                results.write(str(songOrArtist[0]) + ') ' + songOrArtist[3].split('{')[0] + '\n')

        results.write('\n__Scores__')

        last_used_score = -1
        score_string = ''
        for score in rating[4]:
            if score[0] == last_used_score:
                score_string = score_string + score[1] + ', '
                pass
            else:
                score_string = score_string[:-2]
                results.write(score_string)
                last_used_score = score[0]
                score_string = '\n' + str(last_used_score) + ' - ' + score[1] + ', '

        score_string = score_string[:-2]
        results.write(score_string)

        results.write('\n\n__Comments__\n')
        for score in rating[5]:
            if score[2] != '':
                results.write('**' + score[1] + ' (' + str(score[0]) + '):** "' + score[2] + '"\n')
        results.write('\n\n\n---------------------\n\n')
        pass

results.close()