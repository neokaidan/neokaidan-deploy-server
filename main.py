#! /usr/bin/python3
import server as srv


def main():
    with srv.app.app_context():
        srv.start_server()


if __name__ == "__main__":
    main()
