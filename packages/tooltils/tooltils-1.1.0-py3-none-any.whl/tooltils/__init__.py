# Copyright(c) 2023 ebots
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__title__:   str = 'tooltils'
__author__:  str = 'feetbots'
__version__: str = '1.1.0'
__license__: str = 'MIT'

f"""
# tooltils | v{__version__}
A lightweight python utility library built on standard modules
"""

class bm:
    from io import TextIOWrapper, UnsupportedOperation
    from time import time as ctime, localtime, sleep
    from urllib.request import urlopen, Request
    from json.decoder import JSONDecodeError
    from json import dumps, load as jload
    from urllib.error import URLError
    from os.path import getsize
    from json import dumps
    from os import system


class errors:
    class ConnectionError(Exception):
        """Unable to connect to server"""
        def __init__(self, message=None, *args):
            self.message = message

        def __str__(self):
            if self.message:
                return self.message
            return 'Unable to connect'

    class JSONDecoderError(Exception):
        """Unable to decode JSON input"""
        def __init__(self, message=None, *args):
            self.message = message

        def __str__(self):
            if self.message:
                return self.message
            return 'Unable to decode JSON'


class requests:
    """Basic http methods"""

    def get(_url: str, _params: dict={}):
        """Call a URL and return JSON data"""

        try:
            if not _url.startswith('https://') and not _url.startswith('http://'):
                _url = 'https://' + _url

            if _params != {}:
                if _url[-1] == '?':
                    _furl: str = _url
                else:
                    _furl: str = _url + '?'

                for i in _params.keys():
                    if i + '=' not in _furl:
                        _furl += i + '=' + _params[i] + '&'

                data = bm.urlopen(_furl[0:-1])
            else:
                data = bm.urlopen(_url)
        except bm.URLError:
            raise errors.ConnectionError('Nodename nor servername provided, or not known')

        try:
            tempJSON: dict = eval((str(data.read()).replace('true', 'True').replace('false', 'False').replace('null', 'None'))[2:-1])
        except:
            raise errors.JSONDecoderError('Unable to parse JSON data from given url({0})'.format(_url))

        class response:
            code:   int = data.getcode()
            json:  dict = tempJSON
            pretty: str = bm.dumps(json, indent=2)
            text:   str = data.read()

        return response
    
    def post(_url: str, _params: dict={}):
        """Post dictionary data to a URL and return JSON data"""

        if not _url.startswith('https://') and not _url.startswith('http://'):
            _url: str = 'https://' + _url
        
        try:
            req = bm.Request(_url, method='POST')
            if _params != {}:
                jdata: dict = bm.dumps(_params).encode()
                req.add_header('Content-Type', 'application/json')
                req.add_header('Content-Length', len(jdata))
            
            data = bm.urlopen(_url, data=jdata)
            tempJSON: dict = eval((str(data.read()).replace('true', 'True').replace('false', 'False').replace('null', 'None'))[2:-1])
        except (bm.URLError, bm.JSONDecodeError, SyntaxError, NameError, TypeError, ValueError, ZeroDivisionError) as err:
            if type(err) is bm.URLError:
                raise errors.ConnectionError('Nodename nor servername provided, or not known')
            else:
                raise errors.JSONDecoderError('Unable to parse JSON data from given url({0})'.format(_url))
        
        class response:
            code:   int = data.getcode()
            json:  dict = tempJSON
            pretty: str = bm.dumps(json, indent=2)
            text:   str = data.read()
        
        return response

class files:
    """Custom file methods"""

    def clear(_file: bm.TextIOWrapper):
        """Clear a file using truncate"""

        if type(_file) is not bm.TextIOWrapper:
            with open(_file, 'r+') as _file:
                pass
        try:
            _file.seek(0)
            _file.truncate(0)
        except (bm.UnsupportedOperation, ValueError):
            raise bm.UnsupportedOperation('File is not writeable or has been closed')

class json:
    """Custom JSON methods"""

    def load(_file: bm.TextIOWrapper) -> dict | list:
        """Load data as a dictionary or list type"""

        if type(_file) is not bm.TextIOWrapper:
            raise TypeError('Expected type _io.TextIOWrapper but received {0}'.format(type(_file)))
        elif _file.mode[0] == 'w':
            raise TypeError('Cannot read from file in write mode')
        try:
            return bm.jload(_file)
        except (bm.JSONDecodeError, SyntaxError, NameError, TypeError, ValueError, ZeroDivisionError):
            raise errors.JSONDecoderError('JSON file was typed incorrectly or was dangerous')

    def set(_file: bm.TextIOWrapper, _settings: dict) -> None:
        """Set a key value in a JSON file"""

        data: dict | list = json.load(_file)
        listdata: list = []
        appljson: str = ''

        if type(data) is dict:
            data.update(_settings)
            appljson: str = bm.dumps(data, indent=2)
        elif type(data) is list:
            for i in data:
                i.update(_settings)
                listdata.append(i)
            listdata.pop(-1)
            appljson: str = bm.dumps(listdata, indent=2)

        files.clear(_file)
        _file.write(appljson)
    
    def add(_file: bm.TextIOWrapper, _keys: dict) -> None:
        """Add a key value pair to a JSON file"""

        data: dict | list = json.load(_file)
        for i in _keys.keys():
            if type(data) is list:
                data.append({i: _keys[i]})
            else:
                data[i] = _keys[i]
        
        appljson: str = bm.dumps(data, indent=2)
        files.clear(_file)
        _file.write(appljson)

    def remove(_file: bm.TextIOWrapper, _key: str) -> None:
        """Remove a key value pair from a JSON file"""

        data: dict | list = json.load(_file)
        listdata: list = []
        if type(data) is dict:
            try:
                data.pop(_key)
            except KeyError:
                pass
            appljson = bm.dumps(data, indent=2)
        else:
            for i in data:
                try:
                    i.pop(_key)
                except KeyError:
                    pass
                listdata.append(i)
            appljson = bm.dumps(listdata, indent=2)
        files.clear(_file)
        _file.write(appljson)

class time:
    """Time related methods"""

    def epoch() -> float:
        """Return epoch based off system clock (If applicable)"""

        return bm.ctime()

    def getdate(format: int=0, timestamp: float=bm.ctime()) -> str:
        """Convert epoch to human formatted date"""

        date = bm.localtime(timestamp)
        month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                 'August', 'September', 'October', 'November', 'December'][date.tm_mon - 1]
        day_end = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th',
                   'th'][int(str(date.tm_mday)[-1])] if str(date.tm_mday) not in ['11', '12', '13'] else 'th'
        hour = date.tm_hour % 12 if date.tm_hour % 12 != 0 else 12
        min = str(date.tm_min) if len(str(date.tm_min)) != 1 else f'0{date.tm_min}'
        sec = str(date.tm_sec + 1) if len(str(date.tm_sec + 1)) != 1 else f'0{date.tm_sec + 1}'
        formats = ['{0}-{1}-{2} {3}:{4}:{5}'.format(date.tm_year, date.tm_mon if len(str(date.tm_mon)) != 1 else f'0{date.tm_mon}',
                                                    date.tm_mday, date.tm_hour if len(str(date.tm_hour)) != 1 else f'0{date.tm_hour}', min, sec),
                   '{0}:{1} {2} on the {3}{4} of {5}, {6}'.format(hour, min, 'PM' if date.tm_hour >= 12 else 'AM',
                                                                  date.tm_mday, day_end, month, date.tm_year)]
        return formats[format]

    def sleep(ms: float) -> None:
        """Delay execution for x amount of milliseconds (If applicable)"""

        bm.sleep(ms / 1000)

class logging:
    """General logging functions and ANSI escape sequence colour codes"""

    colours: list = ['pink', 'green', 'blue', 'yellow',
                     'red', 'white', 'cyan', 'gray', '']
    cvalues: list = ['35', '32', '34', '33',
                     '31', '38', '36', '30', '0']

    def ctext(text: str='', colour: str='', bold: bool=False) -> str:
        """Return text in specified colour"""

        try:
            cvalue = logging.cvalues[logging.colours.index(colour)]
        except ValueError:
            cvalue = colour

        bm.system('')
        return '\u001b[{0}{1}{2}\u001b[0m'.format(cvalue, ';1m' if bold else 'm', text)

    def log(type: int, header: str, details: str) -> None:
        """Log text to the terminal as an info, warning or error type"""

        try:
            data = [[logging.ctext('INFO', 'blue', True), '     '],
                    [logging.ctext('WARNING', 'yellow', True), '  '],
                    [logging.ctext('ERROR', 'red', True), '    ']][type - 1]
        except IndexError:
            raise IndexError('Unknown type ({0})'.format(type))

        bm.system('')
        print('{0} {1}{2}{3} {4}'.format(logging.ctext(time.getdate(), 'gray', True), data[0], data[1],
                                         logging.ctext(header, 'pink'), details))

class wave:
    def length(_file: bm.TextIOWrapper | str) -> float:
        """Return the length of a wave file in seconds"""

        _file: str = _file.name if type(_file) is bm.TextIOWrapper else _file
        with open(_file, encoding='latin-1') as _f:
            _f.seek(28)
            sdata: str = _f.read(4)
        rate: int = 0
        for i in range(4):
            rate += ord(sdata[i]) * pow(256, i)

        return round((bm.getsize(_file) - 44) * 1000 / rate / 1000, 2)

class string:
    """Custom string modifying methods"""

    def reverse(_text: str) -> str:
        """Reverse a string"""

        text: str = ''
        inc: int = -1
        for i in _text:
            text += _text[inc]
            inc -= 1
        return text


    def cstrip(_text: str, _chars: str) -> str:
        """Strip a string using a character list as a filter"""

        for i in _chars:
            _text = _text.replace(i, '')
        return _text

    def mreplace(_text: str, _chars: dict) -> str:
        """Multi replace words in a string using a dictionary"""

        for i in _chars.keys():
            _text = _text.replace(i, _chars[i])
        return _text

    def cipher(_text: str, _shift: int) -> str:
        """A simple caeser cipher utilising place shifting"""

        return ''.join([chr((ord(i) + _shift - (65 if i.isupper() else 97)) % 26 + (65 if i.isupper() else 97)) for i in _text])

    def halve(_text: str) -> list:
        """Halve text and return both halves as a list"""

        i: int = len(_text)
        if i % 2 == 0:
            return [_text[0: i // 2], _text[i // 2:]]
        else:
            return [_text[0:(i // 2 + 1)], _text[(i // 2 + 1):]]

class types:
    """Custom type methods"""

    class list():
        """Convert a dictionary or tuple to a list"""

        def __new__(self, _list: dict | tuple) -> list:
            nlist: list = []

            if type(_list) is dict:
                for i in _list.keys():
                    nlist.append(i)
                    nlist.append(_list[i])
            elif type(_list) is tuple:
                for i in _list:
                    nlist.append(i)

            return nlist
    
    class tuple():
        """Convert a dictionary or list to a tuple"""

        def __new__(self, _tuple: dict | list) -> tuple:
            ntuple: tuple = ()

            if type(_tuple) is dict:
                for i in _tuple.keys():
                    ntuple += (i, _tuple[i])
            elif type(_tuple) is list:
                for i in _tuple:
                    ntuple += (i, '')
                    ntuple = ntuple[:-1]

            return ntuple
    
    class dict():
        """Convert a list or tuple to a dictionary"""
        
        def __new__(self, _dict: list | tuple) -> dict:
            ndict: dict = {}

            try:
                for i, item in enumerate(_dict, 0):
                    ndict[item] = _dict[i + 1]
            except IndexError:
                if len(_dict) % 2 != 0:
                    raise IndexError('Odd number of items in list')
                return ndict
    
    class bool():
        """Convert a list, tuple, string, integer or dictionary to a boolean"""
        
        def __new__(self, _bool: list | tuple | str | int | dict) -> bool:
            if type(_bool) is list or type(_bool) is tuple or type(_bool) is dict:
                if len(_bool) != 0:
                    return True
            elif type(_bool) is str:
                if _bool.lower() == 'true':
                    return True
                elif _bool.lower() == 'false':
                    return False
                elif len(_bool) != 0:
                    return True
            elif type(_bool) is int:
                if _bool != 0:
                    return True
                else:
                    return False

            return True
