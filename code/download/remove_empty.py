
import os


def main():

    datadir = '../../data'
    for name in os.listdir(datadir):
        filename = os.path.join(datadir, name)
        if not filename.endswith('.csv'): continue

        with open(filename, 'r') as f:
            text = f.read()
        if '<title>404 Not Found</title>' in text:
            os.remove(filename)


if __name__ == '__main__':
    main()
