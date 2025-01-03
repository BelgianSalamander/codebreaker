import os
import time
import signal
import json
import asyncio
import sys
import random
import results
os.chdir(os.path.join(os.path.dirname(__file__),".."))
import database
import judge
import problems

UPDATE_COMPLETED = '''
UPDATE results
SET status = ?, score = ?, complete = TRUE
WHERE id = ? AND complete = FALSE;
'''

should_run = True

async def run_worker(number):
    while should_run:
        jobs_to_do = await database.fetch_all('SELECT * FROM results WHERE complete = FALSE ORDER BY id ASC')
        if len(jobs_to_do) > 0:
            job = jobs_to_do[0]
            print('Processing job -', job['id'])
            problem = problems.get_problem(job['problem'])
            score, status = await judge.run_judge(problem, job['proposed_input'], job['correct_output'])
            best_score = await results.get_user_problem_best(job['owner'], job['problem'])
            if best_score > 0 and score > 0:
                score = 0
                status = 'Code already broken!'
            await database.connection.execute(UPDATE_COMPLETED, [status, int(score), job['id']])
            await database.connection.commit()
        else:
            await asyncio.sleep(0.2)

def handle_sigterm(a, b):
    global should_run
    should_run = False
    print('Caught sigterm, stopping...')

def handle_sigint(a, b):
    global should_run
    should_run = False
    print('Caught sigint, stopping...')

if __name__ == '__main__':
    print('Started')
    signal.signal(signal.SIGTERM, handle_sigterm)
    signal.signal(signal.SIGINT, handle_sigint)
    num_threads = 1 if len(sys.argv) == 1 else int(sys.argv[1])

    problems.load_problem_info()
    loop = asyncio.get_event_loop()
    task = loop.create_task(problems.compile_problem_executables())
    loop.run_until_complete(task)
    problems.load_problem_executables()

    worker_list = [
        asyncio.ensure_future(run_worker(i)) for i in range(num_threads)
    ]
    loop.run_until_complete(asyncio.wait(worker_list))

    loop.run_until_complete(database.connection.close())

    loop.close()
