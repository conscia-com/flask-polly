#!flask/bin/python
from flask import Flask, send_file, redirect, session
from flask import request
from flask import render_template
import tempfile
import boto3
import os
import httplib


# This sets a directory for static files since Apache and Nginx aren't used
app = Flask(__name__, static_url_path='/static')

# Make sessions work
app.secret_key = os.urandom(24)

# AWS Polly is set here. It requires the newest version of Boto3
polly = boto3.client('polly')

# Just a placeholder
@app.route('/')
def index():
    return redirect("/inserttext")


# This generates the primary site used where text is inputted
@app.route('/inserttext/', methods=['GET', 'POST'])
def renderinserttext_page():

    if request.method == 'POST':
        if "texttospeech" in request.form and request.form["texttospeech"] != "":
            sentence = request.form["texttospeech"]
            session['sentence'] = sentence

    return render_template('inserttext.html')


@app.route('/say.mp3', methods=['GET'])
def say():
    sentence = session.pop("sentence", None)
    if sentence is None:
        return (httplib.NO_CONTENT, 204) # sentence not set

    resultVoice = ConvertTextToVoice(sentence, 'Naja')
    soundResult = resultVoice['AudioStream']

    f = tempfile.TemporaryFile()
    f.write(soundResult.read())

    response = send_file(f, as_attachment=True,
                         attachment_filename='say.mp3',
                         add_etags=False)

    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)

    response.headers.extend({
        'Content-Length': size,
        'Cache-Control': 'no-cache'
    })

    return response


# The text is sent to AWS Polly and a StreamObject is returned
def ConvertTextToVoice(text, voice):
    result = polly.synthesize_speech(OutputFormat='mp3', Text=text, VoiceId=voice)
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





