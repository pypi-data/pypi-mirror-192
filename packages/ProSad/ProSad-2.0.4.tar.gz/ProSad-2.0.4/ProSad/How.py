#Copyright (C) 2022 X CODER
from time import sleep

yellow = '\033[93m' 
white = '\033[00m'
bold = '\033[1m'

text =(f"""
{bold}START!

SAD CoDeR ID: {yellow}@SAD_CODER
{white}
{bold}ProSad Library Version→ {yellow}2.0.4{white}

{bold}Channel Rubika→ {yellow}https://rubika.ir/Source_Python_Sad
{white}{bold}
Please Wait. . . . . . . . . . . . . . . . . . . . . . . . . .
""")

for text in text:
    print (text, flush=True, end="")
    sleep(0.008)