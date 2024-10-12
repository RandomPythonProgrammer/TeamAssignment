import os
import random

class Team:
    def __init__(self, categories, members=[]):
        self.members = members
        self.scores = {category: 0 for category in categories}

    def addMember(self, member):
        self.members.append(member)
        for category in self.scores.keys():
            self.scores[category] += float(member[category])

    def __repr__(self):
        return '\n'.join([
        '---TEAM---',
        'Summary:',
        f'Scores: {self.scores}',
        f'Count: {len(self.members)}',
        *(member['name'] for member in self.members)
        ])

class CSV:
    def __init__(self, filepath):
        self.data = []
        self.headers = []
        header = True

        # Read data out of CSV
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                values = line.strip().split(',')
                if header:
                    self.headers.extend(values)
                    header = False
                else:
                    entry = {}
                    for i in range(len(self.headers)):
                        entry[self.headers[i]] = values[i]
                    self.data.append(entry)

        # Make the headers immutable
        self.headers = tuple(self.headers)
        

def getBest(people, category):
    # Looks for highest of category
    highest = people[0]
    for person in people:
        if person[category] > highest[category]:
            highest = person
    return highest


def getLowestTeam(teams, category):
    # Gets the team with lowest score in category
    lowest = teams[0]
    for team in teams:
        if team.scores[category] < lowest.scores[category]:
            lowest = team
    return lowest


def findByName(people, name):
    for person in people:
        if person['name'] == name:
            return person


def main():
    numTeams = int(input('Number of teams: '))
    categories = [item.strip() for item in input('Categories separated by commas: ').split(',')]
    print(f'Reading from {os.path.join('data', 'people.csv')}')
    data = CSV(os.path.join('data', 'people.csv'))
    random.shuffle(data.data)
    random.shuffle(categories)

    teams = []

    for i in range(numTeams):
        manual = []
        print(f'Team: {i}')
        names = [item.strip() for item in input('Manual assignment separated by commas: ').split(',')]
        for name in names:
            person = findByName(data.data, name)
            data.data.remove(person)
            manual.append(person)
        teams.append(Team(categories, manual))


    index = 0
    while len(data.data) > 0:
        picks = [team for team in teams if len(team.members)//len(categories) <= index]
        for category in categories:
            if len(data.data) > 0:
                pick = getLowestTeam(picks, category)
                member = getBest(data.data, category)
                data.data.remove(member)
                pick.addMember(member)
        picks.remove(pick)
        index += 1
    print('\n'.join([str(team) for team in teams]))


if __name__ == '__main__':
    main()
        