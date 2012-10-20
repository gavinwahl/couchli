import pprint
import urlparse
import json
import os
import tempfile
import subprocess
try:
    import readline
    histfile = os.path.join(os.path.expanduser("~"), ".couchli_history")
    try:
        readline.read_history_file(histfile)
    except IOError:
        pass
    import atexit
    atexit.register(readline.write_history_file, histfile)
    del histfile
except ImportError:
    pass

import requests


def edit_in_editor(current):
    EDITOR = os.environ.get('EDITOR', 'vim')
    with tempfile.NamedTemporaryFile(mode='w+') as f:
        f.write(current)
        f.flush()
        subprocess.call([EDITOR, f.name])
        f.seek(0)
        return f.read()


def complete_json_object(s):
    curlies = 0
    state = 1
    states = {
        (1, '"'): 2,
        (2, '\\'): 3,
        (3, None): 2,
        (2, '"'): 1,
    }
    for c in s:
        if state == 1:
            if c == '{':
                curlies += 1
            elif c == '}':
                curlies -= 1
        state = states.get((state, c)) or states.get((state, None)) or state
    return state == 1 and curlies == 0


class Interactive(object):
    def __init__(self):
        self.prefix = ''
        self.docs = {}
        self.previous_location = ''

    def build_url(self, url):
        return urlparse.urljoin(self.prefix, url)

    def print_response(self, resp):
        print resp.status_code,
        print json.dumps(resp.json, indent=4, sort_keys=True)

    def read_a_json(self, start):
        r = [start]
        while not complete_json_object('\n'.join(r)):
            r.append(raw_input())
        j = '\n'.join(r)
        try:
            json.loads(j)
            return j
        except ValueError:
            print "That's not json, dummy"

    def do_request(self, method, url, data=None):
        if url:
            url = self.build_url(url)
        else:
            url = self.previous_location

        prev_doc = self.docs.get(url)
        headers = {}
        if data:
            headers['content-type'] = 'application/json'
        if method != 'get' and prev_doc and '_rev' in prev_doc:
            headers['if-match'] = prev_doc['_rev']

        print "%s %s %r" % (method.upper(), url, headers)
        resp = getattr(requests, method)(url, data=data, headers=headers)
        if method == 'get':
            self.previous_location = url
        else:
            self.previous_location = (resp.headers.get('Location') or
                                      self.previous_location)
        self.docs[url] = resp.json
        self.print_response(resp)

    def do_one(self):
        command_line = raw_input('> ')
        command_line, _, comment = command_line.partition('#')
        if command_line:
            command, _, args = command_line.partition(' ')
            command = command.lower()
            return getattr(self, 'command_%s' % command)(args)

    def command_get(self, url):
        self.do_request('get', url)

    def command_put(self, args):
        url, _, content = args.partition(' ')
        if content:
            new = self.read_a_json(content)
        else:
            if url:
                url = self.build_url(url)
            else:
                url = self.build_url(self.previous_location)
            print repr(url)
            response = requests.get(url)
            if response.status_code == 200:
                current = json.dumps(response.json, indent=4, sort_keys=True)
            else:
                current = ''
            new = edit_in_editor(current)

        self.do_request('put', url, new)

    def command_post(self, args):
        url, _, content = args.partition(' ')
        if content:
            content = self.read_a_json(content)
        else:
            content = edit_in_editor('')

        self.do_request('post', url, content)

    def command_delete(self, url):
        self.do_request('delete', url)

    def command_use(self, base):
        base = base.strip()
        if not base:
            print self.prefix
            return
        if not base.endswith('/'):
            base += '/'
        self.previous_location = self.prefix = self.build_url(base)

i = Interactive()
while True:
    i.do_one()
