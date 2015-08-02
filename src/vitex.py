from os.path import pardir, sep
import sys
sys.path.append(pardir + sep)
from resumeParser import RMLParser as rmlp

if __name__ == "__main__":
	parsed = rmlp(sys.argv[1])
	print("Success!")
