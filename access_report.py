import argparse
from reporter import AccessReport


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='run access report')
    parser.add_argument('-d', '--database', nargs='?',
                        help='path to maxmind database file')
    parser.add_argument('-f', '--file', nargs='?',
                        help='path to log file to process')

    args = parser.parse_args()
    rp = AccessReport(
        db_file=args.database,
        state_country='United States'
    )
    rp.report(args.file)
