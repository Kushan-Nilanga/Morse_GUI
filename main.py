import csv
import time
from curses.ascii import isalnum
from guizero import App, TextBox, PushButton, Text
import RPi.GPIO as GPIO


def read_morse_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        return dict((row[0], row[1]) for row in reader)


morse_lookup = read_morse_csv('morsecode.csv')


def send_morse(code):
    for signal in code:
        if signal == '.':
            GPIO.output(40, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(40, GPIO.LOW)

        if signal == '-':
            GPIO.output(40, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(40, GPIO.LOW)
        time.sleep(0.5)


def send_code():
    txt = t_bx.value
    alnum_filter = filter(isalnum, txt)
    txt = "".join(alnum_filter).upper()
    out.clear()
    out.append(f"Sending: {txt}")

    # sending message
    for letter in txt:
        morse = morse_lookup[letter]
        print(letter, morse)
        send_morse(morse)
        time.sleep(1)
    
    out.clear()


if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40, GPIO.OUT)

    app = App(title='Morse Code', height=100)
    t_bx = TextBox(app)
    PushButton(app, command=send_code)
    out = Text(app, "")
    app.display()
