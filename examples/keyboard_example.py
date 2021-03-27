from generalutils.devel import KeyboardMonitor
from time import sleep


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
