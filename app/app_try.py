from flask import Flask, render_template, request,session
from random_words import RandomWords
app = Flask(__name__)

@app.route('/start')
def first():
    session['count'] = 0
    return render_template('number1.html')

@app.route('/number2',methods=['POST','GET'])
def index():
        rw = RandomWords()
        print(session['count'])
        session['count'] += 1
        count = 7 - session['count']

        if session['count'] == 1:
            session['guesses'] = []
            session['wordform'] = 'Guess ! \n'
            session['word'] =rw.random_word().upper()
            session['wordlen'] = len(session['word'])
            name = request.form['word']
            session['wordform'] = "Welcome " + name + " ! "
            for i in range(session['wordlen']):
                session['guesses'].append("?")
                session['wordform'] += "_?_"
            return render_template('number2.html',word=session['wordform'],count=count)

        else:
            guess = str(request.form['gue']).upper()
            if len(guess) > 1 or session['word'].find(guess) == -1 :

                    if session['count'] == 7:
                        lost = "YOU LOST ! The Word was "
                        lost += session['word']
                        return lost
                    return render_template('number2.html', word=session['wordform'],count=count)

            else:
                indexing = 0
                session['count'] -= 1
                session['wordform'] =""
                while indexing < session['wordlen']:
                    indexing = str(session['word']).find(guess, indexing)
                    if indexing == -1:
                        break
                    session['guesses'][indexing]= guess
                    indexing += 1
                for i in range((session['wordlen'])):
                    session['wordform'] += "_ " + str(session['guesses'][i]) + " _"

                if not '?' in session['guesses']:
                    text = "YOU WIN !! THE WORD IS "
                    for i in range(session['wordlen']):
                        text += session['guesses'][i]
                    return text

                return render_template('number2.html', word=session['wordform'],count = count)


if __name__ == '__main__':
    app.secret_key='it_is_so_secret'
    app.run(host='0.0.0.0', port="5000", debug=True)