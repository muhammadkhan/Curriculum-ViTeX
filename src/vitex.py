from resumeParser import RMLParser as rmlp
import sys

if __name__ == "__main__":
	parsed = rmlp(sys.argv[1])
	print("Success!")
