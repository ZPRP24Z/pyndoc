import argparse

def main():
    parser = argparse.ArgumentParser(
        prog='Pyndoc',
        description='Converter of markup languages.')

    parser.add_argument('-f', '--from', dest='from_format', required=True, help='Source format')
    parser.add_argument('-t', '--to', dest='to_format', required=True, help='Target format')
    parser.add_argument('file', help='Input file')
    parser.add_argument('-o', '--output', dest='output', default=None, help='Output file (optional)')

    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()