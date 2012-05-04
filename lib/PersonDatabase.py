#!/usr/bin/env python
#PersonDatabase.py
#
#Copyright 2012 - Patrick F. Wilbur <proj pdub net>
#
#

class PersonDB:
    def __init__(self, path_to_person_flatfile=None):
        self.PersonDatabase = {}
        if path_to_person_flatfile != None and path_to_person_flatfile != '':
            self.loadPersonFlatfile(path_to_person_flatfile)

    def loadPersonFlatfile(self, path):
        self.PersonDatabase = {}
        f = open(path)
        for line in f:
            key, name, telephone, carrier = line.split(':')
            self.PersonDatabase[key] = (name,telephone,carrier.rstrip())
        f.close()
    def getPersonDatabase(self):
        return self.PersonDatabase

    def search(self,query):
        query = query.lower()
        results = {}
        for key in self.PersonDatabase.keys():
            if key.lower() == query:
                return {key: self.PersonDatabase[key]}
        for key in self.PersonDatabase.keys():
            if query in key.lower():
                results[key] = self.PersonDatabase[key]
        for person in self.PersonDatabase.items():
            if query in (person[1][0]).lower():
                results[person[0]] = person[1]
            if query in (person[1][1]).lower():
                results[person[0]] = person[1]
        return results

if __name__ == '__main__':
    d = PersonDB()
    d.PersonDatabase = {'doe1':('Jane Doe','5555551212','Verizon Wireless'),
                        'deer1':('John Deer','5555551313','Verizon Wireless') }
    print('do',d.search('do'))
    print('doe1',d.search('doe1'))
    print('deer',d.search('deer'))
    print('3',d.search('3'))
    print('555',d.search('555'))
    
