import sys
import csv
import math

# some constants
input_columns = [
    "time",
    "email",
    "school",
    "event",
    "pos",
    "1",
    "2",
    "3",
    "pos",
    "1",
    "2",
    "3",
    "pos",
    "1",
    "2",
    "3",
    "pos",
    "1",
    "2",
    "3",
    "qb_1",
    "center_1",
    "wr_1",
    "qb_2",
    "center_2",
    "wr_2",
    "qb_3",
    "center_3",
    "wr_3",
    "kicker_score",
    "fumble_time",
    "1",
    "2",
    "3",
    "1",
    "2",
    "3",
    "1",
    "2",
    "3",
]

# events are keys, high score wins boolean as value
events = {
    'Shuttle Run': False,
    'Three-Cone Drill': False,
    'Strength Test': True,
    'QB Accuracy Test': True,
    'Speed Test': False,
    'Longest Field Goal': True,
    'QB Longest Throw': True,
}

positions = [
    'Running Back',
    'Wide Receiver',
    'Defender',
    'Center',
    'QB',
    'Kicker',
]

num_of_schools = 10


def main(data_path):
    raw_data = read_csv(data_path)
    keyed_entrys = rows_into_entrys(raw_data)
    entries = massage_entrys(keyed_entrys)
    rankings = get_rankings(entries)
    get_scores(rankings)

# read csv into data structure
def read_csv(path):
    raw_data = []

    # read data into nested list structure
    with open(path, newline='') as csv_data:
        reader = csv.reader(csv_data)
        for csv_row in reader:
            raw_data.append(csv_row)
    
    return raw_data

def rows_into_entrys(raw_data):
    keyed_entrys = []
    # iterate over each submission - put data in struct
    for i in range(1, len(raw_data)):
        keyed_entry = {}
        for j in range(len(raw_data[i])):
            datum = raw_data[i][j]
            if datum != '':
                keyed_entry[input_columns[j]] = datum
        if not '1' in keyed_entry:
            keyed_entry['1'] = ''
        if not '2' in keyed_entry:
            keyed_entry['2'] = ''
        if not '3' in keyed_entry:
            keyed_entry['3'] = ''
        if keyed_entry['event'] == 'QB Accuracy Test':
            if not 'center_1' in keyed_entry:
                keyed_entry['center_1'] = ''
            if not 'center_2' in keyed_entry:
                keyed_entry['center_2'] = ''
            if not 'center_3' in keyed_entry:
                keyed_entry['center_3'] = ''
            if not 'qb_1' in keyed_entry:
                keyed_entry['qb_1'] = ''
            if not 'qb_2' in keyed_entry:
                keyed_entry['qb_2'] = ''
            if not 'qb_3' in keyed_entry:
                keyed_entry['qb_3'] = ''
            if not 'wr_1' in keyed_entry:
                keyed_entry['wr_1'] = ''
            if not 'wr_2' in keyed_entry:
                keyed_entry['wr_2'] = ''
            if not 'wr_3' in keyed_entry:
                keyed_entry['wr_3'] = ''
        keyed_entrys.append(keyed_entry)

    return keyed_entrys

# massage the data and find the best score for each entry
def massage_entrys(keyed_entrys):
    entries = []
    for entry in keyed_entrys:
        if entry['event'] == 'Shuttle Run':
            entries.append(make_entry(entry, entry['pos'], min_num(entry['1'], entry['2'], entry['3'])))
        elif entry['event'] == 'Three-Cone Drill':
            entries.append(make_entry(entry, entry['pos'], min_num(entry['1'], entry['2'], entry['3'])))
        elif entry['event'] == 'Strength Test':
            entries.append(make_entry(entry, entry['pos'], max_num(entry['1'], entry['2'], entry['3'])))
        elif entry['event'] == 'Speed Test':
            entries.append(make_entry(entry, entry['pos'], min_num(entry['1'], entry['2'], entry['3'])))
        elif entry['event'] == 'QB Accuracy Test':
            entries.append(make_entry(entry, 'QB', max_num(entry['qb_1'], entry['qb_2'], entry['qb_3'])))
            entries.append(make_entry(entry, 'Center', max_num(entry['center_1'], entry['center_2'], entry['center_3'])))
            entries.append(make_entry(entry, 'Wide Receiver', max_num(entry['wr_1'], entry['wr_2'], entry['wr_3'])))
        elif entry['event'] == 'Longest Field Goal':
            entries.append(make_entry(entry, 'Kicker', max_num(entry['1'], entry['2'], entry['3'])))
        elif entry['event'] == 'QB Longest Throw':
            entries.append(make_entry(entry, 'QB', max_num(entry['1'], entry['2'], entry['3'])))

    to_remove = []
    for i in range(len(entries)):
        item = entries[i]
        if item['event'] == 'QB Accuracy Test' and item['score'] <= 0:
            to_remove.append(i)
    
    for index in range(len(to_remove)-1, -1, -1):
        del entries[to_remove[index]]

    for item in entries:
        print(item)

    print()
    return entries

def get_rankings(entries):
    rankings = {} 
    for pos in positions:
        pos_rankings = {}
        for event, high_wins in events.items():
            rev = False
            if high_wins:
                rev = True
            filtered = filter(lambda e: e['pos'] == pos and e['event'] == event, entries)
            ranked = sorted(filtered, key=lambda e: e['score'], reverse=rev)
            pos_rankings[event] = get_school_scores(ranked)
        print(pos, pos_rankings)
        print()
        rankings[pos] = pos_rankings

    return rankings

def get_scores(rankings):
    positional_scores = {}
    for pos, event_rankings in rankings.items():
        scores = {}
        for event, schools in event_rankings.items():
            for school, event_score in schools.items():
                add_to_value(scores, school, event_score)
        positional_scores[pos] = scores
        print('{ ', pos, ': ', scores, ' }')
    print()

    positional_ranking = {}
    for pos, score in positional_scores.items():
        positional_ranking[pos] = rank_scores(score)
        print('{ ', pos, ': ', positional_ranking[pos], ' }')
    print()


    overall_scores = {}
    for pos, pos_scores in positional_ranking.items():
        for school, score in pos_scores.items():
            add_to_value(overall_scores, school, score)
    print(overall_scores)



def make_entry(keyed_entry, pos, score):
    return {'time': keyed_entry['time'], 'email': keyed_entry['email'], 'school': keyed_entry['school'], 'event': keyed_entry['event'], 'pos': pos, 'score': score}

def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def max_num(n1, n2, n3):
    nums = []
    if is_float(n1):
        nums.append(float(n1))
    if is_float(n2):
        nums.append(float(n2))
    if is_float(n3):
        nums.append(float(n3))
    
    if len(nums) > 0:
        return max(nums)
    else:
        return -math.inf

def min_num(n1, n2, n3):
    nums = []
    if is_float(n1):
        nums.append(float(n1))
    if is_float(n2):
        nums.append(float(n2))
    if is_float(n3):
        nums.append(float(n3))
    
    if len(nums) > 0:
        return min(nums)
    else:
        return math.inf

def get_school_scores(entries):
    schools = {}
    rank = 0
    for index in range(len(entries)):
        schools[entries[index]['school']] = num_of_schools - rank
        if rank == 0:
            schools[entries[index]['school']] += 1
        if index + 1 < len(entries) and entries[index]['score'] != entries[index+1]['score']:
            rank = index + 1

    return schools

def rank_scores(scores):
    ranked_schools = sorted(scores.items(), key=lambda e: e[1], reverse=True)
    ranked_scores = {}
    rank =  0
    for index in range(len(ranked_schools)):
        ranked_scores[ranked_schools[index][0]] = num_of_schools - rank
        if rank == 0:
            ranked_scores[ranked_schools[index][0]] += 1
        if index + 1 < len(ranked_schools) and ranked_schools[index][1] != ranked_schools[index + 1][1]:
            rank = index +1

    return ranked_scores





def add_to_value(d, key, amt):
    if not key in d:
        d[key] = amt
    else:
        d[key] += amt

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Program needs score file")
        exit(1)
    main(sys.argv[1])

