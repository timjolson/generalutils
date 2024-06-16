from types import MethodType, FunctionType, LambdaType
from types import SimpleNamespace
from logging import Formatter, LogRecord
import sys
import os


def is_func(func):
    """Check if 'func' is an instance of (MethodType, FunctionType, LambdaType)

    :param func: thing to check if it's a function
    :return: bool, whether 'func' is an instance of (MethodType, FunctionType, LambdaType)
    """
    return isinstance(func, (MethodType, FunctionType, LambdaType))


def get_all_funcs(localDict):
    """Get names of all functions in a dictionary. Uses is_func.
    Ignores names starting with dunder '__'

    :param localDict: dictionary to check for functions
    :return: [strings], names of functions in localDict where is_func()==True
    """
    return [x[0] for x in filter(lambda x: is_func(x[1]), localDict.items()) if not x[0].startswith('__')]


def get_all_classes(localDict):
    """Get names of all classes in a dictionary.
    Ignores names starting with dunder '__'

    :param localDict: dictionary to check for classes
    :return: [strings], names of functions in localDict where isinstance(obj, type)==True
    """
    return [x[0] for x in filter(lambda x: isinstance(x[1], type), localDict.items()) if not x[0].startswith('__')]


def apply_default_args(defaultargs, kw_dict):
    """Returns (dict, namespace) of defaultargs overridden by kwargs. Any keys in kwargs not in defaultargs
    raise a ValueError.

    :param defaultargs: dict of defaults
    :param kw_dict: dict of kwargs to process
    :return: dict, SimpleNamespace
    """
    unknown_args = kw_dict.keys() - defaultargs.keys()
    if unknown_args:
        raise ValueError(f"Unknown argument(s): {unknown_args}")
    a = defaultargs.copy()
    a.update(kw_dict)
    return a, SimpleNamespace(**a)


class KeyboardMonitor:
    """
    Use in a `with` statement to intercept keyboard input in a terminal. Upon exiting the `with` code block,
    the terminal is reverted to its calling (normal) state. Special return values can be seen
    in KeyboardMonitor.translate.keys().

    On *nix platforms, within `with` statement, KeyboardMonitor wraps builtin `print` function.

    ```
    with KeyboardMonitor() as key_pressed:
        print('press `q`')
        while key_pressed() != 'q':  # loop until you get a key
            print('.')               # overrides builtin `print` function
            sleep(0.5)

        print('try `A`')
        while True:
            KeyboardMonitor.write('.')  # write does not include an ending newline character
            key = key_pressed()  # store key if you want to compare it or do different things for different keys
            if key is None:  # key is `None` by default
                pass
            elif key == 'a':
                print("Pressed `a`, keys are case sensitive.")
            elif key == 'A':  # keys are case sensitive
                print("Pressed `A`.")
                break
            else:
                print(f"Pressed `{key}` :: Try something else")
            sleep(0.5)
    ```

    Inspired by
    https://gitlab.com/smiley1983/halite3-match-manager/blob/master/keyboard_detection.py
    """
    if os.name == 'nt':
        import msvcrt  # windows keyboard stuff
    else:
        import termios  # keyboard takeover on *nix
        from select import select  # input handling in terminal on *nix

    import builtins as __builtin__  # will replace `print` while inside `with` block

    translate = {
        'TAB': b'\t', 'ESC': b'\x1b',
        'F1': b'\x1bOP', 'F2': b'\x1bOQ',
        'F3': b'\x1bOR', 'F4': b'\x1bOS',
        'F5': b'\x1b[15~', 'F6': b'\x1b[17~',
        'F7': b'\x1b[18~', 'F8': b'\x1b[19~',
        'F9': b'\x1b[20~', 'F10': b'\x1b[21~',
        'F11': b'\x1b[23~\x1b', 'F12': b'\x1b[24~\x08',
    }
    rev_trans = {v: k for k, v in translate.items()}

    def __enter__(self):
        if os.name == 'nt':
            return self.query_keyboard

        # save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = KeyboardMonitor.termios.tcgetattr(self.fd)
        self.old_term = KeyboardMonitor.termios.tcgetattr(self.fd)

        # new terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~KeyboardMonitor.termios.ICANON & ~KeyboardMonitor.termios.ECHO)

        # switch to unbuffered terminal
        KeyboardMonitor.termios.tcsetattr(self.fd, KeyboardMonitor.termios.TCSAFLUSH, self.new_term)

        # replace builtin `print` function to include flush
        KeyboardMonitor.old_print = KeyboardMonitor.__builtin__.print  # backup

        def __new_print(*args, end='\n', **kwargs):
            if 'end' not in kwargs.keys():  # set default end character to newline
                kwargs.update({'end': end})
            KeyboardMonitor.old_print(*args, **kwargs)
            sys.stdout.flush()  # push to terminal
        KeyboardMonitor.__builtin__.print = __new_print  # replace `print`

        return self.query_keyboard

    def __exit__(self, type, value, traceback):
        if os.name == 'nt':
            return

        KeyboardMonitor.__builtin__.print = KeyboardMonitor.old_print

        # swith to normal terminal
        KeyboardMonitor.termios.tcsetattr(self.fd, KeyboardMonitor.termios.TCSAFLUSH, self.old_term)

    @staticmethod
    def write(*args):
        sys.stdout.write(*args)
        sys.stdout.flush()

    def query_keyboard(self):
        key = '' if os.name == 'nt' else bytes(0)

        while True:  # read all input bytes
            read = None
            if os.name == 'nt':
                read = KeyboardMonitor.msvcrt.getch().decode('utf-8') or None
            else:
                dr, dw, de = KeyboardMonitor.select([sys.stdin], [], [], 0)
                if dr:
                    read = os.read(sys.stdin.fileno(), 1)
            if read is None:  # no more input
                break
            key += read  # concatenate input bytes

        if key == b'':  # no keys pressed
            rv = None
        elif key in self.rev_trans.keys():  # special return value
            rv = self.rev_trans[key]
        elif key != b'':  # non empty (likely just a standard key)
            try:
                rv = key.decode('utf-8')
            except AttributeError as e:
                rv = str(key)
        else:
            raise TypeError(f"key `{key}` of type `{type(key)}` is not supported")
        return rv


class MultilineFormatter(Formatter):
    """
    Inspired by https://stackoverflow.com/a/45217732
    """
    def format(self, record: LogRecord):
        save_msg = record.msg
        if not isinstance(save_msg, str):
            save_msg = str(save_msg)
        output = ""
        for line in save_msg.splitlines():
            record.msg = line
            output += super().format(record) + "\n"
        output = output[:-1]
        record.msg = save_msg
        record.message = output
        return output


__all__ = ['is_func', 'get_all_funcs', 'get_all_classes', 'apply_default_args', 'MultilineFormatter']
