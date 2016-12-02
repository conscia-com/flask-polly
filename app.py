#!flask/bin/python
from flask import Flask
from flask import request
from flask import render_template
from flask.json import jsonify
import boto3


# This sets a directory for static files since Apache and Nginx aren't used
app = Flask(__name__, static_url_path='/static')


# AWS Polly is set here. It requires the newest version of Boto3
polly = boto3.client('polly')


# Just a placeholder
@app.route('/')
def index():
    return 'This server hosts different API endpoints.'


# This generates the primary site used where text is inputted
@app.route('/inserttext/', methods=['GET'])
def renderinserttext_page():
    return render_template('inserttext.html')


#  A POST is sent and handled in this function
@app.route('/inserttext/', methods=['POST'])
def texttospeech():
    if request.form["texttospeech"] == "":
# If there is no text inputtet in the field, it will set the returnTag to False
        return render_template('inserttext.html', returnTag = False)
    else:
# If the textfield contains data, it will save the sound to the disk to make it available for the webpage.
        resultVoice = ConvertTextToVoice(request.form["texttospeech"], 'Naja')
        soundResult = resultVoice['AudioStream']
        with open('static/sound.mp3', 'wb') as handle:
            handle.write(soundResult.read())
        #returnTag = True
        resultVoice = None
        soundResult = None
        return render_template('inserttext.html', returnTag = True)


# The text is sent to AWS Polly and a StreamObject is returned
def ConvertTextToVoice(text, voice):
    result = polly.synthesize_speech(OutputFormat='mp3', Text=text, VoiceId=voice)
    return result


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')





