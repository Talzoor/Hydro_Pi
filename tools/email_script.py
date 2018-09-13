#!/usr/bin/env python
try:
    import linecache
    import sys
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    import base64
    from datetime import datetime


except ImportError:
    LOG.warning('import error')


class SendEmail:

    def __init__(self, _log, _conf):

        self.LOG = _log
        self.configuration = _conf

        self.to_addr        = "talzoor@gmail.com"
        self.from_addr      = "Hydro.Pi.Alert@gmail.com"
        self.mail_subject   = "-- Hydro Pi alert --"
        self.mail_body      = "Your Hydroponic system speaking :)"
        self.mail_msg       = ""
        self.file_full_path = "/home/pi/PythonScripts/Hydro_Pi/Pi_switch.log"

        self.sent_today = _conf[0]
        self.counter_need_reset = False

    def send(self, **kwargs):
        try:
            if "subject" in kwargs:
                self.mail_subject = kwargs["subject"]
            if "to" in kwargs:
                self.to_addr = kwargs["to"]
            if "log_file" in kwargs:
                self.file_full_path = kwargs["log_file"]
            if "msg" in kwargs:
                self.mail_msg += kwargs["msg"] + '\n'

        except KeyError:
            self.LOG.warning("email init error")
            pass

        try:
            if not self.check_send_time(self.configuration):
                return 0
            else:
                from_addr = self.from_addr
                to_addr = self.to_addr
                mail_subject = self.mail_subject
                mail_body = self.mail_body
                mail_msg = self.mail_msg


                msg_root = MIMEMultipart('related')
                msg_root['From'] = from_addr
                msg_root['To'] = to_addr
                msg_root['Subject'] = mail_subject
                msg_root.preamble = 'preamble: This is a multi-part message in MIME format.'

                msgAlternative = MIMEMultipart('alternative')
                msg_root.attach(msgAlternative)

                msgText = MIMEText('This is the alternative plain text message.')
                msgAlternative.attach(msgText)

                line1 = "<body style=font-size:24px;><p>{text}</p></body>".format(text=mail_msg)
                line2 = "<body style=font-size:18px;><p>{text}</p></body>".format(text=mail_body)

                msgText = MIMEText("{}{}".format(line1, line2), 'html')
                msgAlternative.attach(msgText)

                filename = self.file_full_path[self.file_full_path.rfind('/')+1:]
                attachment = open(self.file_full_path, "rb")

                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= {}".format(filename))
                msg_root.attach(part)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                p_encode = b'dHpIeWRybzEx'
                p_decoded = base64.b64decode(p_encode).decode("utf-8")
                server.login(from_addr, p_decoded)
                text = msg_root.as_string()
                server.sendmail(from_addr, to_addr, text)
                server.quit()
                self.LOG.info("email sent!")

                self.mail_msg = ""
                self.sent_today -= 1

        except:
            self.raise_exception("email.send")

    def raise_exception(self, _str_func):
        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)
        self.LOG.warning("\n\nfucn '{}' error: \n{}, {} \nline:{}- {}".format(_str_func, exc_type, exc_obj, lineno, line))

    def check_send_time(self, vars):
        send_it = False
        days = int(vars[0])
        time_hr = int(vars[1])
        if self.sent_today >= 1:
            hr_now = int(datetime.now().strftime('%H'))
            min_now = int(datetime.now().strftime('%M'))
            if hr_now >= time_hr:
                send_it = True
            if time_hr == hr_now and \
                    (min_now in range(0, 5)) and \
                    self.counter_need_reset is False:
                self.counter_need_reset = True
                self.sent_today = days

        elif self.sent_today < 1:
            send_it = False

        if self.counter_need_reset is True and hr_now is time_hr+1:
            self.counter_need_reset = False

        return send_it

