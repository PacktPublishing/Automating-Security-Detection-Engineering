#!/usr/bin/env python3
import sys
#python considers sysargv[0] itself as a script first arg is 1
#you can set the shell env variable e.g. export TEST='bar'
#now run python3 helloWorld-sysargv-example.py $TEST
#no immediate need to refactor scripts that use arguments, just specify the shell variable :)
print('hello foo', sys.argv[1])

#but of course if you wanted to intake direct shell variables
#just comment or remove the argument or parser requirements and replace with similar:
#export TEST='myLittleSecret'
import os
api_secret = os.getenv('TEST') #this is the variable name from the shell without the $ ref