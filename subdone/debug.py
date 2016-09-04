
import sys



def debug(*args):
    argsstr = "\n".join([str(x) for x in args])
    sys.stdout.write("\ndebug>>>>>>>>>>>\n" + argsstr + "\n")