import csv

results = open('Results_Powerpoint.txt', 'w', encoding='utf-8')

results.write('AVERAGES\n')

averages = []

with open('Averages.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        averages.append(row)

average_list = []
for average_fields in averages:
    if average_fields[0] == '':
        pass
    elif average_fields[1] == '':
        results.write('__' + average_fields[0] + '__\n')
        average_list = []
    elif average_fields[0].strip() == 'Average':
        average_list.sort(reverse=True)
        for group in average_list:
            results.write('' + group[1] + ': ' + str(round(float(group[0]), 2)) + '\n')
        results.write('\n')
        results.write('Overall Average: ' + average_fields[1] + '\n')
    elif average_fields[0].strip() == 'Mode':
        results.write('Most Used Score: ' + average_fields[1] + '\n')
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
            comp[index].append('' + individual_comp_list[0][2] + ': ' + str(individual_comp_list[0][0]) + '% ('+str(individual_comp_list[0][1])+')\n')
            for ind_comp in individual_comp_list[1:]:
                comp[index].append('' + ind_comp[2] + ': ' + str(ind_comp[0]) + '% ('+str(ind_comp[1])+')\n')
        individual_comp_list = []
        index = index + 1
        comp.append(['__' + compatibility_fields[0] + '__\n'])
    else:
        individual_comp_list.append([float(compatibility_fields[1][:-1]), round(float(compatibility_fields[2]), 3), compatibility_fields[0]])

if individual_comp_list:
    individual_comp_list.sort(reverse=True)
    comp[index].insert(0, float(individual_comp_list[0][0]))
    comp[index].append('' + individual_comp_list[0][2] + ': ' + str(individual_comp_list[0][0]) + '% :heart:\n')
    for ind_comp in individual_comp_list[1:]:
        comp[index].append('' + ind_comp[2] + ': ' + str(ind_comp[0]) + '% \n')

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
        current_group = overall_fields[0].split('{')[0]
        number_of_songs = overall_fields[0].split('{', 1)[1].split('}')[0]
        i = 4
        for score in overall_fields[4:]:
            if score != '':
                artist_scores.append([int(score), overall_header[i]])
            i = i + 1
        artist_scores.sort(key=lambda l: [-l[0], l[1].lower()])
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
    else:
        song = [round(float(overall_fields[1]), 2), round(float(overall_fields[3]), 2), overall_fields[0], current_group, overall_fields[2]]
        ratings = []
        for rating, name in zip(overall_fields[4:], overall_header[4:]):
            if name != '':
                ratings.append([rating, name, comments_fields[comments_header.index(name)]])
        ratings.sort(key=lambda l: [-float(l[0]), l[1].lower()])
        song.append(ratings)
        rating_list.append(song)

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
                if artist[2].strip() == artist_name:
                    biggest_fans = 'Biggest ' + fandom_name + 's: '
                    biggest_antis = 'Biggest Antis: '

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

for artist in artist_list:
    if artist[2].strip() == artist_name:
        biggest_fans = 'Biggest ' + fandom_name + 's: '
        biggest_antis = 'Biggest Antis: '

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

reversed_song_list = sorted(rating_list)

for artist in artist_list:
    artist.insert(0, artist.pop(2))
    last_index = -1
    for song in rating_list:
        if song[4] == artist[0]:
            last_index = rating_list.index(song)
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
        results.write('__' + str(rating[0]) + ') ' + song_name + ' - ' + rating[4] + '__\n')
        if song_link is not None:
            results.write('<' + song_link + '>\n')
        results.write('Average: ' + str(rating[1]) + '\n')
        results.write('Total Points: ' + str(rating[5]) + '\n')
        results.write('Controversy: ' + str(rating[2]) + '\n\n')
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
                results.write('"' + score[2] + '" - ' + score[1] + ' (' + str(score[0]) + ')\n')

        results.write('\n---------------------\n\n')
    else:
        results.write('\n\n')
        results.write('__' + rating[0] + '__\n')
        results.write('Overall Average: ' + str(rating[1]) + '\n')
        results.write('Total Points: ' + str(rating[3]) + '\n\n')
        results.write(rating[6] + '\n')
        results.write(rating[7] + '\n')
        results.write('\n__Rankings__\n')

        for song in reversed_song_list:
            if song[4] == rating[0]:
                results.write(str(song[0]) + ') ' + song[3].split('{')[0] + '\n')

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
                results.write('' + score[1] + ' (' + str(score[0]) + '): "' + score[2] + '"\n')
        results.write('\n\n\n---------------------\n\n')
        pass

results.close()