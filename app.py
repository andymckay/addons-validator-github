import BaseHTTPServer
import json
import logging
import os
import tempfile
import requests
import sample

log = logging.getLogger(__name__)
addons_validator = '/Users/andy/sandboxes/addons-validator'
bin_file = 'bin/addons-validator'
user = 'andymckay-limited-access'
token = os.environ['GITHUB_API_TOKEN']
auth = (user, token)
context = 'addons/validator'


class handler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        data = json.loads(self.rfile.read(content_len))

        self.send_response(200)
        self.end_headers()
        self.wfile.write('')

        urls = get_urls(data)
        post_data = {
            'state': 'pending',
            'context': context
        }
        res = requests.post(urls['status_url'], json=post_data, auth=auth)
        res.raise_for_status()

        result = check(data)
        notify(data, result, urls)


def notify(data, result, urls):
    errors = False
    for notice in result.get('notices', []):
        post_data = {
            'state': 'error',
            'description': notice['description'][:130],
            'context': context
        }
        res = requests.post(urls['status_url'], json=post_data, auth=auth)
        res.raise_for_status()
        errors = True

    for error in result.get('errors', []):
        post_data = {
            'body': error['description'],
            'path': os.path.join(*error['file'].split(os.sep)[1:]),
            'position': error['line'],
            'commit_id': data['pull_request']['head']['sha']
        }
        res = requests.post(urls['comment_url'], json=post_data, auth=auth)
        res.raise_for_status()
        errors = True

    if not errors:
        post_data = {
            'state': 'success',
            'context': context
        }
        res = requests.post(urls['status_url'], json=post_data, auth=auth)
        res.raise_for_status()


def check(data):
    tempdir = tempfile.mkdtemp()
    url = data['pull_request']['head']['repo']['archive_url']
    url = url.replace('{archive_format}', 'zipball')
    url = url.replace('{/ref}', '/' + data['pull_request']['head']['sha'])

    response = requests.get(url, auth=auth)
    response.raise_for_status()

    path = os.path.join(tempdir, 'pull-request.xpi')
    open(path, 'wb').write(response.content)

    cmd = '%s %s -o json' % (bin_file, path)
    current = os.curdir
    try:
        os.chdir(addons_validator)
        stdin, stdout, stderr = os.popen3(cmd)
        stdin.close()
    finally:
        os.chdir(current)

    stdout = stdout.read()
    result = json.loads(stdout)
    return result


def get_urls(data):
    c_url = data['pull_request']['head']['repo']['pulls_url']
    c_url = c_url.replace('{/number}', '/' + str(data['pull_request']['number']))
    c_url = c_url + '/comments'

    url = data['pull_request']['head']['repo']['statuses_url']
    url = url.replace('{sha}', data['pull_request']['head']['sha'])
    return {'comment_url': c_url, 'status_url': url}


def listen(options):
    address = (options['HOST'] or 'localhost', int(options['PORT'] or 8000))
    httpd = BaseHTTPServer.HTTPServer(address, handler)
    log.info('Server listening at: {0}:{1}. CTRL-C to exit.'.format(*address))
    httpd.serve_forever()


if __name__=='__main__':
    # Just check we have access.
    res = requests.get('https://api.github.com/user', auth=auth)
    res.raise_for_status()

    listen({'HOST': 'localhost', 'PORT': 8000})
    #check(sample.data)
    #notify(sample.data, sample.result)
