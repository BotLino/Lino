import os
import json
import requests as req
import subprocess as sp

# constants

ngrok_url = 'http://127.0.0.1:4040'
ngrok_tunnels = '/api/tunnels'
ngrok_path = 'ngrok/ngrok'
ngrok_cmd = ['./' + ngrok_path, 'http', '5002']
tunnel_name = 'command_line'
webhook_env_name = 'WEBHOOK_URL'
envs = {
        'TRAINING_EPOCHS': None,
        'TELEGRAM_ACCESS_TOKEN': None,
        'VERIFY': None,
        'PSID': None,
        'FACEBOOK_ACCESS_TOKEN': None,
        'SECRET': None,
        'TELEGRAM_DB_URI': None,
        'FACEBOOK_DB_URI': None
}

# methods

def file_exists(filepath):
    if os.path.isfile(filepath):
        return True
    return False

def make_error(msg):
    print('Error: ' + msg)
    exit()

def start_ngrok():
    # starts ngrok and wait for it to be ready
    print('Starting ngrok')
    pid = sp.Popen(ngrok_cmd).pid

def verify():
    # verifies if ran from Lino's folder
    # and if docker-compose file exists
    # and set ngrok path
    cwd = os.getcwd()
    folder = cwd.split('/')[-1]

    if folder != 'Lino':
        make_error('You must run this script from Lino\'s root directory.')

    if not file_exists('docker-compose.yml'):
        make_error('docker-compose.yml file not found in current directory.')

    if not file_exists(ngrok_path):
        make_error('Couldn\'t find ngrok binary.')

def get_webhook():
    # connects to ngrok api and get the new webhook
    print('Connecting to ngrok API...')
    try:
        res = req.get(ngrok_url + ngrok_tunnels)
    except:
        make_error('Can\'t connect. Is ngrok running?')
    res = json.loads(res.text)
    for tunnel in res['tunnels']:
        if tunnel['name'] == tunnel_name:
            return tunnel['public_url'] + '/webhook'
    make_error('Couldn\'t find tunnel with name ' + tunnel_name)

def modify_webhook(webhook):
    # modifies docker-compose with new webhook
    print('Modifying webhook env variable')
    lines = read_compose()

    for ind, line in enumerate(lines):
        pos = line.find(webhook_env_name)
        if pos is not -1:
            lines[ind] = line[0:pos] + webhook_env_name + '=' + webhook

    with open('docker-compose.yml', 'w') as dc:
        for line in lines:
            dc.write(line + '\n')

def get_envs():
    for env in envs:
        value = find_env(env)
        envs[env] = value

def find_env(env_name):
    lines = read_compose()
    for ind, line in enumerate(lines):
        pos = line.find(env_name)
        if pos is not -1:
            start = pos + len(env_name) + 1
            return (line[start::].strip(), ind)

def ask_envs():
    # asks for each env in evs list
    print('Set environment variables')
    print('Leave it blank to use the already set value')
    print('Insert # to comment the variable')
    for env in envs:
        env_value = envs[env][0]
        env_index = envs[env][1]
        v = input(env + '( ' + env_value + ' ) : ')
        if v.strip() != '' and v.strip() != '#':
            envs[env] = (v, env_index)
        elif v.strip() == '#':
            envs[env] = ('#' + env_value, env_index)

def modify_envs():
    # modify envs in docker-compose
    print('Modifying envs in docker-compose')
    lines = read_compose()
    for env in envs:
        env_value = envs[env][0]
        env_ind = envs[env][1]
        if env_value[0] == '#':
            lines[env_ind] = '#' + lines[env_ind]
            continue
        operator = '='
        if '$' in env_value:
            operator = ': '
        new_line = env + operator + env_value
        pos = lines[env_ind].find('- ')
        lines[env_ind] = lines[env_ind][0:pos+2] + new_line
    write_compose(lines)

def read_compose():
    with open('docker-compose.yml') as dc:
        return dc.read().split('\n')

def write_compose(lines):
    with open('docker-compose.yml', 'w') as dc:
        for line in lines:
            dc.write(line + '\n')

if __name__ == '__main__':
    print('Chatbots, roll out!')
    verify()
    # start_ngrok()
    menv = input('Change all envs? [y/N]: ')
    if menv == 'y' or menv == 'Y':
        get_envs()
        ask_envs()
        modify_envs()
    webhook = get_webhook()
    modify_webhook(webhook)
    exit()
