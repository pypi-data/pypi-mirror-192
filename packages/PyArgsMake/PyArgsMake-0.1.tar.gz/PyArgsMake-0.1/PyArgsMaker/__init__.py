import sys

def arg(arg, prefix, command, nonarg=None):
    try:
        if sys.argv[1] == prefix + arg:
            command()
    except:
        nonarg()