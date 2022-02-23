'''
Title: Random Game Picker for GOG Galaxy 2.0
Author: Guillermo Ochoa

Description:
uses internal python libraries so you don't need anything else!
All random selection done on the pure query, you can also filter by tag or to not include game pass games if you want
(for example you have a backlog selected and want a random game to play from it)

Have Fun!
'''

import json
import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect("C:\\ProgramData\\GOG.com\\Galaxy\\storage\\galaxy-2.0.db")
    tag = ''
    sub = ''
    if (input("Do you want to filter out game pass games? y/n: ") == 'y'):
        sub = 'and SR.subscriptionId is NULL'
    if (input("Do you want to filter by tag? y/n: ") == 'y'):
        tag = 'and URT.tag = \'' + input('Choose your tag to filter: ') + '\''

    query = 'select distinct GP.value \
        from GamePieces GP \
        inner join UserReleaseTags URT on URT.releaseKey = GP.releaseKey \
        inner join LibraryReleases LR on LR.releaseKey = GP.releaseKey \
        left join SubscriptionReleases SR on SR.LicenseId = LR.Id \
        where 1=1  \
        '+ tag +' \
        and GP.value like \'{"title%\' \
        '+ sub +' \
        group by URT.releaseKey \
        order by random() \
        limit 1'
    
    while(1):
        cursor = conn.execute(query)
        title = json.loads(cursor.fetchone()[0])["title"]
        print('\n'+title+'\n')
        another = input("Chooser another game? y/n: ")
        if (another != 'y'):
            print("Have Fun!")
            break