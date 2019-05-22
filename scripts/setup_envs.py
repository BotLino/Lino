import yaml
import json
import requests as req
import re

docker_compose_path = 'docker-compose.yml'
envs = {}


def print_error(msg):
    print('\x1b[1;31m' + msg + '\x1b[0m')


def process_env_yaml(text):
    if isinstance(text, dict):
        name = list(text.keys())[0]
        value = text[name]
        return (name, value)
    text = text.split('=')
    return (text[0], text[1])


def load_envs():
    read = read_file(docker_compose_path)
    dump = yaml.load(read)
    services = dump['services']
    for service in services:
        if 'environment' not in services[service]:
            continue
        if service not in envs:
            envs[service] = {}
        service_envs = services[service]['environment']
        for env in service_envs:
            res = process_env_yaml(env)
            envs[service][res[0]] = res[1]


def read_file(path):
    with open(path, 'r') as f:
        doc = f.read()
    return doc


def change_envs():
    for service in envs:
        print()
        print('No input means no change')
        print('Service: ' + service)
        local_envs = envs[service]
        for env in local_envs:
            value = local_envs[env]
            new = input(env + ' (' + value + ') = ')
            new = new.strip()
            if new == '':
                continue
            envs[service][env] = new


def change_ngrok():
    try:
        res = req.get('http://localhost:4040/api/tunnels')
    except Exception:
        print_error('ERROR: Can\'t connect to ngrok')
        exit()
    url = ''
    res = json.loads(res.text)
    tunnels = res['tunnels']
    for tunnel in tunnels:
        if tunnel['name'] != 'command_line':
            continue
        url = tunnel['public_url']
    for service in envs:
        for env in envs[service]:
            if env != 'WEBHOOK_URL':
                continue
            envs[service][env] = url


def unprocess_env(name, value):
    match = re.match(r'\$\{.+\}', value)
    if match:
        ret = dict()
        ret[name] = value
        return ret
    return name + '=' + value


def envs_to_list():
    for serv in envs:
        new_envs = envs[serv]
        to_yaml = []
        for env in new_envs:
            plain = unprocess_env(env, envs[serv][env])
            to_yaml.append(plain)
        envs[serv] = to_yaml


def write_changes():
    read = read_file('docker-compose.yml')
    with open('docker-compose.yml.bkp', 'w') as f:
        f.write(read)
    dump = yaml.load(read)
    for service in dump['services']:
        if service not in envs:
            continue
        dump['services'][service]['environment'] = envs[service]
    with open('docker-compose.yml', 'w') as dc:
        yaml.dump(dump, dc, default_flow_style=False)


def lint():
    read = read_file('docker-compose.yml')
    version_regex = r'(version: \'\d+\') *\n'
    ret = re.search(version_regex, read)
    if ret:
        read = read[0:ret.start()] + '' + read[ret.end():]
        read = ret.group(0) + '\n' + read
    with open('docker-compose.yml', 'w') as f:
        f.write(read)


def main():
    load_envs()
    changed = False

    ans = input('Change envs? [y/N] ')
    if ans == 'y' or ans == 'Y':
        changed = True
        change_envs()

    ans = input('Change ngrok automatically? [y/N] ')
    if ans == 'y' or ans == 'Y':
        changed = True
        change_ngrok()

    envs_to_list()

    if changed:
        write_changes()
        lint()


if __name__ == '__main__':
    main()
