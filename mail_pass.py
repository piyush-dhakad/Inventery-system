#mail='chouhanvishal273@gmail.com'
#mail_pass='jiqruamhvpktnvzk'
import smtplib
server = smtplib.SMTP('smtp.gmail.com',587)
server.connect()
server.set_debuglevel(True)
try:
    server.verify(email)
except Exception:
    print('ok')
finally:
    server.quit()