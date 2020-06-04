import smtplib
import csv


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


server = smtplib.SMTP('smtp.gmail.com', 587)
server.set_debuglevel(True)

server.ehlo()
server.starttls()
server.ehlo()

server.login('theyeetllc@gmail.com', 'XXXXXX')

from_address = 'theyeetllc@gmail.com'
##to_address = 'signal@lists.collective2.com'
to_address = ['tobalotv@gmail.com', 'ariesvtb@gmail.com', 'traderdave2112@gmail.com']

signals = []

def parse_file(file):

    with open(file, 'r') as sig:
        reader = csv.reader(sig, delimiter="|")

        for row in reader:
            ticker = row[0]
            action = row[1]
            quantity = row[3]
            if action == 'BUY':
                order = 'BTO ' + quantity + " " + ticker + " @ MARKET DAY (stock)"
                print(order)
                signals.append(order)
            else:
                order = 'SSHORT ' + quantity + " " + ticker + " @ MARKET DAY (stock)"
                print(order)
                signals.append(order)
                
    return signals

sig = parse_file("signal.txt")


try:
    for i in range(len(sig)):
        msg = MIMEMultipart()
        msg['From'] = from_address
        msg['To'] = ", ".join(to_address)
        msg['Subject'] = "C2 Signal"
        body = "systemid=777\npw=quantlyfe420\n" + sig[i]
        msg.attach(MIMEText(body, 'plain'))
        string_msg = msg.as_string()
        server.sendmail(from_address,to_address, string_msg)
finally:
    server.quit()