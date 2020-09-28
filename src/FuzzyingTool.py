import sys
from RequestHandler import RequestHandler
from OutputHandler import *
import settings

def helpMenu():
    """Creates the Help Menu"""
    print("\nParameters:")
    print(' '*3+"{:<23}".format("-h, --help")+" Display the help menu and exit")
    print(' '*3+"{:<23}".format("-V, --verbose")+" Enable the verbose mode")
    print("\n"+' '*3+"Core:")
    print(' '*5+"{:<21}".format("-u URL")+" Define the target URL")
    print(' '*5+"{:<21}".format("-f FILENAME")+" Define the entry file")
    print("\n"+' '*3+"Request options:")
    print(' '*5+"{:<21}".format("--data DATA")+" Define the POST data")
    print(' '*5+"{:<21}".format("--proxy IP:PORT")+" Define the proxy")
    print(' '*5+"{:<21}".format("--proxies FILENAME")+" Define the proxies file")
    print(' '*5+"{:<21}".format("--cookie COOKIE")+" Define the HTTP Cookie header value")
    print(' '*5+"{:<21}".format("--delay DELAY")+" Define the delay between each request (in seconds)")
    exit("")

def getUrl(argv: list):
    """Get the target URL

    @type argv: list
    @param argv: The arguments given in the execution
    @rtype: str
    @returns url: The target URL
    """
    try:
        return argv[argv.index('-u')+1]
    except ValueError as e:
        oh.errorBox("An URL is needed to make the fuzzying.")

def getMethodAndArgs(argv: list, url: str):
    """Get the param method to use ('?' in URL if GET, or --data) and the request param string

    @type argv: list
    @param argv: The arguments given in the execution
    @type url: str
    @param url: The target URL
    @rtype: tuple(str, str, str)
    @returns (url, method, param): The tuple with the new target URL, the request method and params
    """
    if ('?' in url):
        url, param = url.split('?')
        method = 'GET'
    else:
        method = 'POST'
        try:
            index = argv.index('--data')+1
            param = argv[index]
        except ValueError as e:
            oh.errorBox("You must set at least GET or POST parameters for the Fuzzying test.")
    return (url, method, param)

def getRequestParams(argv: list, param: str):
    """Split all the request parameters into a list of arguments used in the request
       also set the default parameters value if is given

    @type argv: list
    @param argv: The arguments given in the execution
    @type param: str
    @param param: The parameter string of the request
    @rtype: dict
    @returns defaultEntries: The entries of the request
    """
    defaultEntries = {}
    if ('&' in param):
        param = param.split('&', param.count('&'))
        for arg in param:
            if ('=' in arg):
                arg, value = arg.split('=')
                defaultEntries[arg] = value
            else:
                defaultEntries[arg] = ''
    else:
        if ('=' in param):
            arg, value = param.split('=')
            defaultEntries[arg] = value
        else:
            defaultEntries[arg] = ''
    return defaultEntries

def getWordlistFile(argv: list):
    """Get the fuzzying wordlist filename from -f argument, and returns the file object
       if the argument -f doesn't exists, or the file couldn't be open, an error is thrown and the application exits

    @type argv: list
    @param argv: The arguments given in the execution
    """
    try:
        index = argv.index('-f')+1
        fileName = argv[index]
        try:
            settings.wordlistFile = open('../input/'+fileName, 'r')
        except FileNotFoundError as e:
            oh.errorBox("File '"+fileName+"' not found.")
    except ValueError as e:
        oh.errorBox("An file is needed to make the fuzzying")

def checkCookie(argv: list, requestHandler: RequestHandler):
    """Check if the --cookie argument is present, and set the value into the requestHandler

    @type argv: list
    @param argv: The arguments given in the execution
    @type requestHandler: RequestHandler
    @param requestHandler: The object responsible to handle the requests
    """
    if ('--cookie' in argv):
        cookie = argv[argv.index('--cookie')+1]
        cookieSplited = cookie.split('=')
        requestHandler.setCookie({cookieSplited[0]: cookieSplited[1]})
        oh.infoBox("Set cookie: "+cookie)

def checkProxy(argv: list, requestHandler: RequestHandler):
    """Check if the --proxy argument is present, and set the value into the requestHandler

    @type argv: list
    @param argv: The arguments given in the execution
    @type requestHandler: RequestHandler
    @param requestHandler: The object responsible to handle the requests
    """
    if ('--proxy' in argv):
        index = argv.index('--proxy')+1
        proxy = argv[index]
        requestHandler.setProxy({
            'http://': 'http://'+proxy,
            'https://': 'http://'+proxy
        })
        oh.infoBox("Set proxy: "+proxy)

def checkProxies(argv: list):
    """Check if the --proxies argument is present, and open a file

    @type argv: list
    @param argv: The arguments given in the execution
    """
    if ('--proxies' in argv):
        index = argv.index('--proxies')+1
        proxiesFileName = argv[index]
        try:
            settings.proxiesFile = open('../input/'+proxiesFileName, 'r')
        except FileNotFoundError as e:
            oh.errorBox("File '"+fileName+"' not found.")

def checkDelay(argv: list, requestHandler: RequestHandler):
    """Check if the --delay argument is present, and set the value into the requestHandler

    @type argv: list
    @param argv: The arguments given in the execution
    @type requestHandler: RequestHandler
    @param requestHandler: The object responsible to handle the requests
    """
    if ('--delay' in argv):
        delay = argv[argv.index('--delay')+1]
        requestHandler.setDelay(float(delay))
        oh.infoBox("Set delay: "+delay+" second(s)")

def checkVerboseMode(argv: list):
    """Check if the -V or --verbose argument is present, and set the verbose mode

    @type argv: str
    @param argv: The arguments given in the execution
    """
    if ('-V' in argv or '--verbose' in argv):
        settings.verboseMode = True

def main(argv: list):
    """The main function

    @type argv: list
    @param argv: The arguments given in the execution
    """
    if (len(argv) < 2):
        oh.errorBox("Invalid format! Use -h on 2nd parameter to show the help menu.")
    if (argv[1] == '-h' or argv[1] == '--help'):
        helpMenu()
    url = getUrl(argv)
    url, method, param = getMethodAndArgs(argv, url)
    defaultEntries = getRequestParams(argv, param)
    getWordlistFile(argv)
    requestHandler = RequestHandler(url, method, defaultEntries)
    oh.infoBox("Set target: "+url)
    oh.infoBox("Set param method: "+method)
    oh.infoBox("Set parameters: "+str(defaultEntries))
    checkCookie(argv, requestHandler)
    checkProxy(argv, requestHandler)
    checkProxies(argv)
    checkDelay(argv, requestHandler)
    checkVerboseMode(argv)
    requestHandler.start()

if __name__ == "__main__":
   main(sys.argv)