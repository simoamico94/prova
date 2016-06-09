from flask import Flask, render_template, url_for, redirect, request
import db_interaction
import session
import datetime
import random
import glob


app = Flask(__name__)

DATE_TIME = datetime.datetime.now()

# number of images for each emotion
JOY = 6
SADNESS = 12
ANGER = 1
FEAR = 7

# set of image (generated randomly) and populated in profile()
IMG_SET = ["", "", "", ""]


@app.route('/')
def hello_world():
    # if no address is given, redirect to the index page
    return redirect('index.html')


# default page
@app.route('/index.html')
def index():
    return render_template('index.html')


# FAKE login page
@app.route('/login.html', methods=['POST'])
def login():
    # retrieve form parameters
    username = request.form['username']
    password = request.form['password']

    # verify if user is already registered
    if db_interaction.db_verify_user(username, password):
        return redirect(url_for('profile', username=username))
    else:
        print "Login failed."
        return redirect('index.html')


# FAKE create an account page
@app.route('/create-account.html', methods=['POST'])
def create_account():
    # retrieve form parameters
    username = request.form['username']
    password = request.form['password']
    name = request.form['name']
    surname = request.form['surname']
    born_date = request.form['bornDate']

    # add user to the DB
    db_interaction.db_add_user(username, password, name, surname, born_date)
    print "Created new account"

    return redirect('index.html')


# profile page
@app.route('/user/<username>')
def profile(username):
    # retrieve user info from db
    user = db_interaction.db_get_user(username)

    # pick a random image path from each emotion directory and put it into the image set
    # NB: glob returns a list of the file matching the parameter
    global IMG_SET
    IMG_SET[0] = str(glob.glob("./static/img/joy/*.jpg")[random.randint(0, JOY)])
    IMG_SET[1] = str(glob.glob("./static/img/sadness/*.jpg")[random.randint(0, SADNESS)])
    IMG_SET[2] = str(glob.glob("./static/img/anger/*.jpg")[random.randint(0, ANGER)])
    IMG_SET[3] = str(glob.glob("./static/img/fear/*.jpg")[random.randint(0, FEAR)])

    # shuffle the content of the image set
    random.shuffle(IMG_SET)

    # --------- Graph data section ----------- #
    # get info of past sessions
    # takes only last 4 session info from db
    # TODO get also physical data here
    sessions = db_interaction.db_get_sessions(username)

    data_size = len(sessions)

    if data_size == 0:
        # if there are no sessions, return no data for the graph
        data = 0
    else:
        # initialize the matrix to store data from sessions
        data = [[0 for x in range(7)] for y in range(data_size + 1)]

        # Data column titles in the first row
        data[0] = ['Date', 'Sadness', 'Anger', 'Joy', 'Fear', 'Initial state', 'Final state']

        # translate sessions into a matrix (takes only 4 elements, see above)
        i = 1
        for s in sessions:
            if i < 5:
                data[i] = [s[0], s[2], s[3], s[1], s[4], s[5], s[6]]
                i += 1
            else:
                break

    return render_template('profile.html', user=user, data=data, img_set=IMG_SET)


# session page
@app.route('/<username>/session', methods=['POST'])
def new_session(username):
    # save datetime to a global var
    global DATE_TIME
    DATE_TIME = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # retrieve form parameters
    pre_status = int(request.form['pre_status'])
    joy = int(request.form['joy'])
    sadness = int(request.form['sadness'])
    anger = int(request.form['anger'])
    fear = int(request.form['fear'])
    img_n = int(request.form['radio'])

    # takes emotion values from the image chosen
    # global IMG_SET ----> not necessary, already declared as global in profile() at this point
    values = session.compute_img(IMG_SET[img_n])

    # sum image values to the corresponding emotion value
    joy = joy + values[0]
    sadness = sadness + values[1]
    anger = anger + values[2]
    fear = fear + values[3]

    # compute the resulting emotion
    mood = session.compute_mood(joy, sadness, anger, fear)

    # get light and music info from db
    emotion_info1 = db_interaction.db_get_emotion(mood[0])
    emotion_info2 = db_interaction.db_get_emotion(mood[1])

    # put session info on the db
    db_interaction.db_add_session(username, DATE_TIME, pre_status, joy, sadness, anger, fear)

    # start light for the resulting emotion
    # ------------>  session.light_on(emotion_info1[0], emotion_info2[0])

    # start music for the resulting emotion
    # TODO: NEED TO IMPLEMENT COMBINED PLAYLIST WITH TWO MOODS
    # ------------> session.start_playlist(emotion_info[1])

    return render_template('session.html', username=username)


# FAKE close session page
@app.route('/user/<username>/close-session', methods=['POST'])
def close_session(username):
    # retrieve form parameters
    post_status = request.form['post_status']

    # save datetime of the end of session
    end_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # update the current session on the db, adding the final emotion status and the datetime when session ends
    db_interaction.db_close_session(username, DATE_TIME, post_status, end_datetime)

    # stop the music playing in background
    # ------------> session.stop_playlist()

    # turn off the lights
    # ------------>  session.light_off()

    print "Closing session"

    return redirect(url_for('profile', username=username))


if __name__ == '__main__':
    # app.run(debug=True)
     app.run(host='0.0.0.0', port=5000, debug=False)
