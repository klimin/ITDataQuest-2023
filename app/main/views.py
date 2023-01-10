import sqlite3
from flask import render_template, session, redirect, url_for, flash, request
from config import conf
from . import main
from .forms import *
from datetime import datetime
import os

def timedelta_to_str(duration):
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)

    s = ''
    if days == 1:
        s = s + str(days) + ' day'
    elif days > 1:
        s = s + str(days) + ' days'

    if hours == 1:
        if days != 0:
            s = s + ', '
        s = s + str(hours) + ' hour'
    elif hours > 1:
        if days != 0:
            s = s + ', '
        s = s + str(hours) + ' hours'

    if minutes == 1:
        if (hours != 0) or (days != 0):
            s = s + ', '
        s = s + str(minutes) + ' minute'
    elif minutes > 1:
        if (hours != 0) or (days != 0):
            s = s + ', '
        s = s + str(minutes) + ' minutes'

    if seconds == 1:
        if (hours != 0) or (days != 0) or (minutes != 0):
            s = s + ', '
        s = s + str(seconds) + ' second'
    elif seconds > 1:
        if (hours != 0) or (days != 0) or (minutes != 0):
            s = s + ', '
        s = s + str(seconds) + ' seconds'

    return s


# To make sessions permanent (for Edge)
@main.before_request
def make_session_permanent():
    session.permanent = True


# Injection
@main.context_processor
def inject():
    return dict(conf=conf, str=str)


# Show home Page
@main.route('/', methods=['GET', 'POST'])
def index():
    # Create 'data' folder and create empty database
    # To create new database you should delete folder and database file: `data\danquest2023.db`
    if not os.path.exists(r'data'):
        os.makedirs(r'data' )

        conn = sqlite3.connect(conf.db)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE results (name TEXT,stage INT,start DATETIME,end DATETIME,elapsed TEXT,status TEXT,"
                        "email TEXT,delta BIGINT,q1 INT,q2 INT,q3 INT,q4 INT,q5 INT,q6 INT,q7 INT,q8 INT,q9 INT,q10 INT,"
                        "q11 INT,q12 INT,q13 INT,q14 INT,q15 INT,q16 INT,q17 INT,q18 INT,q19 INT,q20 INT,q21 INT,q22 INT,q23 INT,ip TEXT,user_agent TEXT,q_total INT)")
        cursor.close()

    form = QuestForm()
    form_name = NameForm()
    session.modified = True

    isCompleted = 'danquest2023_completed' in session

    if 'danquest2023_name' in session:
        name = session['danquest2023_name']
    else:
        name = 'Guest'

    if 'danquest2023_email' in session:
        email = session['danquest2023_email']
    else:
        email = ''

    if 'danquest2023_start' in session:
        elapsed = timedelta_to_str(datetime.now() - session['danquest2023_start'])
    else:
        elapsed = 'Just started'

    if 'danquest2023_stage' in session:
        stage_session = session['danquest2023_stage']
    else:
        stage_session = 1

    # Checking stage in arguments
    stage = request.args.get('stage', stage_session, type=int)
    max_stage = stage_session

    # Cannot switch to the future questions (except while God mode is enabled)
    if not conf.god_mode:
        if stage > stage_session:
            stage = stage_session

    # Registration form
    if request.method == 'POST':
        if name == 'Guest':
            conn = sqlite3.connect(conf.db)
            cursor = conn.cursor()
            query = "SELECT email FROM results WHERE email=? LIMIT 1"
            cursor.execute(query, (form_name.email.data,))
            results = cursor.fetchall()
            conn.commit()
            cursor.close()

            if len(results) != 0:
                flash('This email has been registered already! Please, choose another email.', category='danger')
                return redirect(url_for('main.index'))

            session['danquest2023_name'] = form_name.name.data
            session['danquest2023_email'] = form_name.email.data
            session['danquest2023_start'] = datetime.now()

            # Initialization of the total wrong answers
            if 'danquest2023_q_total' not in session:
                session['danquest2023_q_total'] = 0

            # Saving to database
            conn = sqlite3.connect(conf.db)
            cursor = conn.cursor()
            query = "INSERT INTO results (\
                name, stage, start, end, elapsed, status, email, delta, \
                q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, \
                q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q_total, \
                ip, user_agent \
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            td = session['danquest2023_start'] - session['danquest2023_start']

            cursor.execute(query, (session['danquest2023_name'],
                                   1,
                                   session['danquest2023_start'],
                                   session['danquest2023_start'],
                                   'Just registered',
                                   'Registered',
                                   session['danquest2023_email'],
                                   td.seconds,
                                   0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                                   request.remote_addr,
                                   request.user_agent.string))
            conn.commit()
            cursor.close()
            flash('You have been successfully registered. In case you will use the same browser, your progress will be saved \
                (you can close and re-open the quest at any time without progress loss). Good luck with ' + conf.site_title + ' 🤞')
            return redirect(url_for('main.index'))
        else:
            # Initialization of the wrong answers
            if 'danquest2023_q'+str(stage) not in session:
                session['danquest2023_q' + str(stage)] = 0

            # Checking answers

            # Question #1
            if stage == 1 and form.keyword.data.upper().strip() == '5074':
                stage += 1
                flash('A good beginning makes a good ending! You have spy skills!', category='success')

            # Question #2
            elif stage == 2 and form.keyword.data.upper().strip() == 'O':
                stage += 1
                flash('Greetings, Maze winner!', category='success')

            # Question #3
            elif stage == 3 and form.keyword.data.upper().strip() in ['GOOGOL', '1E100', '1' + '0'*100]:
                stage += 1
                flash('Yes! The total number of elementary particles in the universe is less than googol!', category='success')

            # Question #4
            elif stage == 4 and form.keyword.data.upper().strip() == 'CODE':
                stage += 1
                flash('Easy-peasy, lemon squeezy!!', category='success')

            # Question #5
            elif stage == 5 and form.keyword.data.upper().strip() == '401':
                stage += 1
                flash('Great! There is no so faithful friend, as a good book! ', category='success')

            # Question #6
            elif stage == 6 and form.keyword.data.upper().strip() == 'ACTIMEL':
                stage += 1
                flash('Bon appetit!', category='success')

            # Question #7
            elif stage == 7 and form.keyword.data.upper().strip() == 'TURING-COMPLETE':
                stage += 1
                flash('Yes! You can also check Piet, Whitespace, COW, Malbolge, Ook!, etc.', category='success')

            # Question #8
            elif stage == 8 and form.keyword.data.upper().strip() == 'MYSTERY':
                stage += 1
                flash('Yes, you are Sherlock Holmes!', category='success')

            # Question #9
            elif stage == 9 and form.keyword.data.upper().strip() == '34615':
                stage += 1
                flash('Yep!', category='success')

            # Question #10
            elif stage == 10 and form.keyword.data.lower().strip() in ['{7fb2a1c6-dd30-4323-a248-1fa07c0604hc}', '7fb2a1c6-dd30-4323-a248-1fa07c0604hc']:
                stage += 1
                flash('Wow! Great job! You are master of UUID!', category='success')

            # Question #11
            elif stage == 11 and form.keyword.data.upper().strip() == '14.12.1995':
                stage += 1
                flash('Exactly! The domain was registered 27 years ago!', category='success')

            # Question #12
            elif stage == 12 and form.keyword.data.upper().strip() == 'BUSINESS':
                stage += 1
                flash('Excellent, Data Miner!', category='success')

            # Question #13
            elif stage == 13 and form.keyword.data.upper().strip() == 'WAJIMA':
                stage += 1
                flash("It's a marvel that you was escaped!", category='success')

            # Question #14
            elif stage == 14 and form.keyword.data.upper().strip() in ['69', '81', '82', '86', '91', '92', '96', '17', '21', '22', '26', '31', '32', '36', '44', '45', '49', '54', '55', '59', '64', '65']:
                stage += 1
                flash('You did it! Very nice!', category='success')

            # Question #15
            elif stage == 15 and form.keyword.data.upper().strip() == 'QUESTION':
                stage += 1
                flash('Say "Hello" to William Shakespeare!', category='success')

            # Question #16
            elif stage == 16 and form.keyword.data.upper().strip() == '10':
                stage += 1
                flash('The Mathematics is the queen of all sciences!', category='success')

            # Question #17
            elif stage == 17 and form.keyword.data.upper().strip() == '19647':
                stage += 1
                flash('👍', category='success')

            # Question #18
            elif stage == 18 and form.keyword.data.lower().strip() in ['baaf043d03e0416f434872f766619ccf', 'e792ce164cc5654c70ee5164672ab3c3177fd0bd', 'd689dc320587feda8c0cf78acd6b93331d8602d4469901f9bccbe8e52de155cdf1bde68a85d519262d075700d441b287a6fd2ba395f9c2fe696294b3e4d9e348']:
                stage += 1
                flash('Superior security level!', category='success')

            # Question #19
            elif stage == 19 and form.keyword.data.upper().strip() in ['999888777000666000555000000444000000333000222900001000', '999000888000777000000000666000000000555000000000000000444000000000000000333000000000222000900001000']:
                stage += 1
                flash('Right! It seems you are good with numbers!', category='success')

            # Question #20
            elif stage == 20 and form.keyword.data.upper().strip() == 'DATA':
                stage += 1
                flash('Super-duper!', category='success')

            # Question #21
            elif stage == 21 and form.keyword.data.upper().strip() == 'DESCARTES':
                stage += 1
                flash('Vectors rulez!', category='success')

            # Question #22
            elif stage == 22 and form.keyword.data.upper().strip() == 'RATIONALITY':
                stage += 1
                flash('"Your best and wisest refuge from all troubles is in your science" (Ada Lovelace). Congratulations!', category='success')

            # Question #23
            elif stage == 23 and form.keyword.data.upper().strip() == 'IT&DATA':
                session['danquest2023_end'] = datetime.now()

                return redirect(url_for('main.finish'))
            else:
                # Increasing wrong answers in session
                session['danquest2023_q'+str(stage)] = session.get('danquest2023_q'+str(stage)) + 1
                session['danquest2023_q_total'] = session.get('danquest2023_q_total') + 1
                wrong_answers = str(session['danquest2023_q'+str(stage)])

                flash('Your answer is NOT correct. Please, try another answer. Wrong answers: ' + wrong_answers, category='danger')

                # Updating wrong answers statistics
                conn = sqlite3.connect(conf.db)
                cursor = conn.cursor()
                query = "UPDATE results SET q_total=?, q" + str(stage) + "=?, ip=?, user_agent=? WHERE email=?"
                parameters = (session['danquest2023_q_total'],
                              session['danquest2023_q'+str(stage)],
                              request.remote_addr,
                              request.user_agent.string,
                              session['danquest2023_email'])
                cursor.execute(query, parameters)
                conn.commit()
                cursor.close()

            # Updating session
            session['danquest2023_stage'] = stage
            session['danquest2023_end'] = datetime.now()
            elapsed = timedelta_to_str(session['danquest2023_end'] - session['danquest2023_start'])

            # Calculating elapsed time
            td = session['danquest2023_end'] - session['danquest2023_start']

            # Updating DB
            conn = sqlite3.connect(conf.db)
            cursor = conn.cursor()
            query = "UPDATE results SET stage=?, end=?, elapsed=?, status=?, delta=?, ip=?, user_agent=? WHERE email=?"
            parameters = (stage,
                          session['danquest2023_end'],
                          timedelta_to_str(td),
                          'In progress',
                          td.seconds,
                          request.remote_addr,
                          request.user_agent.string,
                          session['danquest2023_email']
                          )
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()

            return redirect(url_for('main.index'))

    return render_template('index.html', form=form, form_name=form_name, name=name, stage=stage, max_stage=max_stage, email=email, elapsed=elapsed, isCompleted=isCompleted)


# Reset request
@main.route('/reset')
@main.route('/reset/')
def reset():
    return render_template('reset.html')


# Confirm reset
@main.route('/confirm')
@main.route('/confirm/')
def confirm():
    session.clear()
    return redirect(url_for('main.index'))


# Finish
@main.route('/finish', methods=['GET', 'POST'])
@main.route('/finish/', methods=['GET', 'POST'])
def finish():
    session.modified = True

    if 'danquest2023_stage' in session:
        stage = session['danquest2023_stage']
        if stage == conf.last_stage:
            session['danquest2023_end'] = datetime.now()
            conn = sqlite3.connect(conf.db)
            cursor = conn.cursor()
            td = session['danquest2023_end'] - session['danquest2023_start']

            query = """UPDATE results SET stage=?, end=?, elapsed=?, status=?, delta=?, ip=? WHERE email=? and status='In progress'"""
            parameters = (session['danquest2023_stage'],
                          session['danquest2023_end'],
                          timedelta_to_str(td),
                          'Completed',
                          td.seconds,
                          request.remote_addr,
                          session['danquest2023_email'],
                          )
            cursor.execute(query, parameters)
            conn.commit()
            cursor.close()

            session['danquest2023_completed'] = True

            return render_template('finish.html')

    return redirect(url_for('main.index'))


# Hi Scores (TOP 5)
@main.route('/hiscore')
@main.route('/hiscore/')
def hiscore():
    conn = sqlite3.connect(conf.db)
    cursor = conn.cursor()
    query = "SELECT name, stage, start, end, elapsed, status, email, delta FROM results"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    new_results = []
    for result in results:
        name = result[0]
        stage = result[1]
        start_date = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S.%f')
        end_date = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S.%f')
        elapsed = result[4]
        status = result[5]
        email = result[6]
        delta = end_date.timestamp() - start_date.timestamp()
        new_results.append((name, stage, start_date, end_date, elapsed, status, email, delta,))

    # ORDER BY status, stage DESC, delta
    new_results.sort(key=lambda x:(x[5], -x[1], x[7]))

    return render_template('hiscore.html', results=new_results[:5])


# Hi Scores (all)
@main.route('/hiscore-all')
@main.route('/hiscore-all/')
def hiscore_all():
    conn = sqlite3.connect(conf.db)
    cursor = conn.cursor()
    query = "SELECT name, stage, start, end, elapsed, status, email, delta, q_total FROM results"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()

    new_results = []
    for result in results:
        name = result[0]
        stage = result[1]
        start_date = datetime.strptime(result[2], '%Y-%m-%d %H:%M:%S.%f')
        end_date = datetime.strptime(result[3], '%Y-%m-%d %H:%M:%S.%f')
        elapsed = result[4]
        status = result[5]
        email = result[6]
        delta = end_date.timestamp() - start_date.timestamp()
        q_total = result[8]
        new_results.append((name, stage, start_date, end_date, elapsed, status, email, delta, q_total,))

    # ORDER BY status, stage DESC, delta
    new_results.sort(key=lambda x:(x[5], -x[1], x[7]))

    return render_template('hiscore-all.html', results=new_results)
