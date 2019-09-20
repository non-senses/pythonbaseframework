import sys

class Logger():
    def info(self, string):
        sys.stdout.write(string+"\n")

    def error(self, string):
        sys.stdout.write(string+"\n")


loggerInstance = Logger()