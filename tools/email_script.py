    #!/usr/bin/env python

class SendEmail:

    def __init__(self, LOG, **kwargs):
        self.LOG = LOG
        for name, value in kwargs.items():
            print('{0} = {1}'.format(name, value))

        try:
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders
        except ImportError:
            print('import error')


    def send(self):
        from_addr = "Hydro.Pi.Alert@gmail.com"
        to_addr = "talzoor@gmail.com"

        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = "Test Alert"
        body = 'This is an extended email test'
        msg.attach(MIMEText(body, 'plain'))

        filename = "Pi_switch.log"
        path = "/home/pi/PythonScripts/Hydro_Pi/"
        attachment = open("{}{}".format(path, filename), "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= {}".format(filename))
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_addr, "tzHydro11")
        text = msg.as_string()
        server.sendmail(from_addr, to_addr, text)
        server.quit()


if __name__ == '__main__':
    email_inst = SendEmail('')
    email_inst.send()
