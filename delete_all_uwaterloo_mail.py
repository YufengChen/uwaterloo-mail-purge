import requests
session = requests.Session()

def delete(start, sm_token):
    data = [
        ('smtoken', sm_token),
        ('mailbox', 'INBOX'),
        ('startMessage', '1'),
        ('targetMailbox', 'INBOX'),
        ('delete', 'Delete'),
        ('location', '/webmail/src/right_main.php?newsort=1&startMessage=1&mailbox=INBOX'),
        ('moveAllMessages', '1'),
    ]

    for i in range(1000):
        data += [('msg[{}]'.format(i), start + i)]

    response = session.post('https://mailservices.uwaterloo.ca/webmail/src/move_messages.php', data=data)


def get_start_and_sm_token():
    params = (
        ('PG_SHOWALL', '0'),
        ('sort', '0'),
        ('startMessage', '1'),
        ('mailbox', 'INBOX'),
    )

    response = session.get('https://mailservices.uwaterloo.ca/webmail/src/right_main.php', params=params)
    sm_token = response.text.split('name="smtoken" value="')[1].split('">')[0]
    if 'name="msg[0]" id="msg' not in response.text:
        return None, None
    start = int(response.text.split('name="msg[0]" id="msg')[1].split('" value="')[0])
    return start, sm_token


def sign_in(user_name, password):
    data = [
        ('login_username', user_name),
        ('secretkey', password),
        ('js_autodetect_results', '1'),
        ('just_logged_in', '1'),
    ]

    response = session.post('https://mailservices.uwaterloo.ca/webmail/src/redirect.php', data=data)
    return 'Unknown user or password incorrect.' not in response.text


def main():
    user_name = input('User name: ')
    password = input('Password: ')
    if not sign_in(user_name, password):
        print('Log in failed')
        return

    while True:
        start, sm_token = get_start_and_sm_token()
        if start is None:
            print('All mail deleted')
            break
        delete(start, sm_token)


if __name__ == "__main__":
    main()
