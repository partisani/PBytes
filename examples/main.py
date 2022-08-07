import pbytes
import bson
import json
from sys import argv

def _main(args):

	for arg in args:
		if arg == "--run":
			filename = args[args.index(arg) + 1]
			parser = pbytes.Parser(pbytes._bytecode_to_dict_(filename))
			parser._run()
		if arg == "--compile":
			filename = args[args.index(arg) + 1]
			targetname = args[args.index(arg) + 2]
			filebuffer = open(filename, "r")
			targetbuffer = open(targetname, "wb")

			filecontent = filebuffer.read()
			targetbuffer.write(bson.dumps(json.loads(filecontent)))

	return 0

if __name__ == "__main__":
	exit(_main(argv))
