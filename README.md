# flask-polly
A frontend in Flask that sends a text to AWS Polly and returns an audiofile that is played in the browser.

# Requirements
Newest versions of:
* boto3
* flask

Be aware that this python app requires AWS credentials on the machine. See the documentation for AWS CLI on how to set up your credentials: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html


# Howto
In order to run Flask you must have the requirements installed on the computer. See section above. Then you start the application from the console by typing in:

```
$ python app.py
```

Open a browser and type this address: http://localhost:5000/inserttext/

Afterwards type in a text and then click submit.
