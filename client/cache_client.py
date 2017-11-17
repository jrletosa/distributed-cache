import argparse
import requests
import json


def main():
    parser = argparse.ArgumentParser(
        description='Distributed cache client')
    subparsers = parser.add_subparsers()

    '''Example:
    python cache_client.py get 172.19.0.10 a-key
    '''
    get_cmd = subparsers.add_parser('get')
    get_cmd.add_argument('node_ip')
    get_cmd.add_argument('key')
    get_cmd.set_defaults(func=get_value)

    '''Example:
    python cache_client.py set 172.19.0.10 a-key a-value
    '''
    set_cmd = subparsers.add_parser('set')
    set_cmd.add_argument('node_ip')
    set_cmd.add_argument('key')
    set_cmd.add_argument('value')
    set_cmd.set_defaults(func=set_value)

    '''Example:
    python cache_client.py dump 172.19.0.10
    '''
    dump_cmd = subparsers.add_parser('dump')
    dump_cmd.add_argument('node_ip')
    dump_cmd.set_defaults(func=dump)

    args = parser.parse_args()
    args.func(args)


def get_value(args):
    res = requests.get('http://' + args.node_ip + '/get/{}'.format(args.key))
    print res.json()


def set_value(args):
    payload = {
        'key': args.key,
        'value': args.value
    }
    requests.post('http://' + args.node_ip + '/set', data=json.dumps(payload))


def dump(args):
    res = requests.get('http://' + args.node_ip + '/dump-content')
    print res.json()

if __name__ == "__main__":
    main()
