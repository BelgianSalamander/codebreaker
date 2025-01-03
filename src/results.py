import json
import problems
import time
import collections
import database
import random

SELECT_USER_PROBLEM_TOTAL = '''
SELECT sum(score)
FROM results LEFT JOIN users
ON owner = users.username
WHERE complete = TRUE and username = ? and problem = ?;
'''

SELECT_USER_PROBLEM_BEST = '''
SELECT max(score)
FROM results LEFT JOIN users
ON owner = users.username
WHERE complete = TRUE and username = ? and problem = ?;
'''

SELECT_VISIBLE_NAMES = '''
SELECT username
FROM users
WHERE visible = TRUE;
'''

SELECT_SCOREBOARD_SCORES = '''
SELECT username, problem, score
FROM results LEFT JOIN users
ON owner = users.username
WHERE complete = TRUE AND id < ?
ORDER BY results.id ASC;
'''

UPDATE_LIMIT = 2

async def get_user_problem_total(username, problem):
    result, = await database.fetch_one(SELECT_USER_PROBLEM_TOTAL, username, problem)
    if result is None: result = 0
    return result

async def get_user_problem_best(username, problem):
    result, = await database.fetch_one(SELECT_USER_PROBLEM_BEST, username, problem)
    if result is None: result = 0
    return result

async def get_visible_names():
    vals = await database.fetch_all(SELECT_VISIBLE_NAMES)
    return [x['username'] for x in vals]

scoreboard = []
last_update = 0

async def get_scoreboard():
    global scoreboard
    global last_update

    if time.time() - last_update < UPDATE_LIMIT: return scoreboard
    last_update = time.time()

    scores = {}
    scoreboard = []

    names = await get_visible_names()
    probs = problems.get_alphabetical()

    for n in names:
        scores[n] = { p.short_name:[0] for p in probs}

    scoreboard_freeze_id, = await database.fetch_one("SELECT value FROM settings WHERE name = 'scoreboard_freeze_id';")
    if scoreboard_freeze_id is None: scoreboard_freeze_id = 1000000000
    for result in await database.fetch_all(SELECT_SCOREBOARD_SCORES, scoreboard_freeze_id):
        if result['username'] not in names: continue
        scores[result['username']][result['problem']].append(scores[result['username']][result['problem']][-1] + result['score'])

    for n in names:
        scoreboard.append({
            'name': n,
            'scores': [
                {
                    'problem': p.long_name,
                    'score': max(scores[n][p.short_name])
                } for p in probs
            ],
            'total': sum([max(scores[n][p.short_name]) for p in probs])
            })
    scoreboard.sort(key = lambda x: x['total'], reverse = True)
    return scoreboard

