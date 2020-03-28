import base64
import config
import logging
import boto3
from botocore.errorfactory import ClientError
import io
import json
import os
from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    session,
    url_for,
    make_response,
    send_from_directory,
    send_file,
    jsonify,
    Response
)

# headers
from decorators import add_response_headers

# setup the app
app = Flask(__name__)
# logging
logger = logging.getLogger(__name__)
if os.environ.get('LOGGING') == 'True':
    logging.basicConfig(level=logging.INFO)

# universal resources
s3 = boto3.resource('s3')
client = boto3.client('s3')


# config
logger.info("Choosing config")
if 'prod' in os.environ.get('ENVIRONMENT').lower():
    logger.info("Using production config")
    app.config.from_object(config.ProductionConfig())
else:
    # Only log flask debug in development mode.
    logger.info("Using development config")
    logging.basicConfig(level=logging.DEBUG)
    app.config.from_object(config.DevelopmentConfig())

#headers:
headers= {'Content-Security-Policy': ("default-src 'self'; form-action 'self'; connect-src 'self'; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; script-src 'self' ; style-src 'self' https://fonts.googleapis.com/;")}


def isBase64(sb):
    try:
        if type(sb) == str:
            # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'ascii')
        elif type(sb) == bytes:
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
            return False

def s3_file_exists(key):
    # given a key, return bool for exists, and if exists the mimetype
    try:
        obj =client.head_object(Bucket=os.environ['BUCKET_NAME'],Key=key)
    except ClientError:
        return(False,None)

    if 'directory' in obj['ContentType'].lower():
        return(False,None)
    else:
        return(True,obj['ContentType'])

@app.before_request
def before_request():
    if not request.is_secure and 'dev' not in app.env:
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code)

@app.route('/status')
@add_response_headers(headers=headers)
def status_page():
    return "ok!"


@app.route("/")
@add_response_headers(headers=headers)
def s3_index():
    exists, mimetype=s3_file_exists('index.html')
    if exists:
        file = client.get_object(Bucket=os.environ['BUCKET_NAME'], Key='index.html')
        return Response(
            file['Body'].read(),
            mimetype=mimetype
        )
    else:
        abort(404)

@app.route("/<path:filename>")
@add_response_headers(headers=headers)
def s3_file(filename):
    exists, mimetype=s3_file_exists(filename)
    if exists:
        file = client.get_object(Bucket=os.environ['BUCKET_NAME'], Key=filename)

        return send_file(
            file['Body']._raw_stream,
            mimetype=mimetype,
            as_attachment=False)
    else:
        abort(404)

# for local development.
if __name__ == '__main__':
    app.run()
