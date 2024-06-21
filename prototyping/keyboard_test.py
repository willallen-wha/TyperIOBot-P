import time
import keyboard as kb

# Test of the keyboard module - wait for space key to be pressed, then wait
# three more seconds for the round to start, and type the provided snippet.
# At the minute, the snippet is typed into prompt.txt ahead of time.

# Store the snippet as a string
sourceFile = open("prototyping/prompt.txt", "rt", encoding="utf-8")
text = sourceFile.read()

# Wait for the space key
kb.wait("space")
# Wait three seconds for the round to start, and an extra 1.5 for the "press
# space to start" prompt to go away
time.sleep(4.5)
# Then type the snippet
kb.write(text)
