# generalutils.devel

    def is_func(func):
        Check if 'func' is an instance of (MethodType, FunctionType, LambdaType)
    
        :param func: thing to check if it's a function
        :return: bool, whether 'func' is an instance of (MethodType, FunctionType, LambdaType)

    def get_all_funcs(localDict):
        Get names of all functions in a dictionary. Uses is_func.
        Ignores names starting with dunder '__'
    
        :param localDict: dictionary to check for functions
        :return: [strings], names of functions in localDict where is_func()==True

    def get_all_classes(localDict):
        Get names of all classes in a dictionary.
        Ignores names starting with dunder '__'
    
        :param localDict: dictionary to check for classes
        :return: [strings], names of functions in localDict where isinstance(obj, type)==True

    def apply_default_args(defaultargs, kw_dict):
        Returns (dict, namespace) of defaultargs overridden by kwargs. Any keys in kwargs not in defaultargs
        raise a ValueError.
    
        :param defaultargs: dict of defaults
        :param kw_dict: dict of kwargs to process
        :return: dict, SimpleNamespace

    class KeyboardMonitor:
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
