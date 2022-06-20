from datetime import datetime
import smtplib
from email.message import EmailMessage

def Send_email(user,sensores):
  EMAIL_ADRESS = "GIECC.UCMEXUS@gmail.com"
  EMAIL_PASSWORD = "kvrdhmkhwfrmkaap"

  msg = EmailMessage()
  msg['Subject'] = "Sensores desconectados"
  msg['From'] = EMAIL_ADRESS
  msg['To'] = user

  msg.set_content(f'Se desconectaron los sensores {sensores}')

  time = datetime.today().strftime('%A, %B %d, %Y %H:%M')

  msg.add_alternative(f"""\
  <!DOCTYPE html>
  <html>
      <head>
          <title>Aviso de desconexión</title>
          <style type="text/css">
              a {{color: #d80a3e;}}
              body, #header h1, #header h2, p {{margin: 0; padding: 0;}}
              #main {{border: 1px solid #cfcece;}}
              img {{display: block;}}
              #top-message p, #bottom p {{color: #3f4042; font-size: 12px; font-family: Arial, Helvetica, sans-serif; }}
              #header h1 {{color: #ffffff !important; font-family: "Lucida Grande", sans-serif; font-size: 24px; margin-bottom: 0!important; padding-bottom: 0; }}
              #header p {{color: #ffffff !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; font-size: 12px;  }}
              h5 {{margin: 0 0 0.8em 0;}}
              h5 {{font-size: 18px; color: #444444 !important; font-family: Arial, Helvetica, sans-serif; }}
              p {{font-size: 16px; color: #444444 !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; line-height: 1.5;}}
              script {{font-size: 12px; color: #444444 !important; font-family: "Lucida Grande", "Lucida Sans", "Lucida Sans Unicode", sans-serif; line-height: 1.5;}} 
          </style>
      </head>
      <body>
      <table width="100%" cellpadding="0" cellspacing="0" bgcolor="e4e4e4">
      <tr>
      <td>

      <table id="main" width="600" align="center" cellpadding="0" cellspacing="15" bgcolor="ffffff">
          <tr>
              <td>
                  <table id="header" cellpadding="10" cellspacing="0" align="center" bgcolor="8fb3e9">
                      <tr>
                          <td width="570" align="center"  bgcolor="#00dda9"><h1>Desconexión de sensores</h1></td>
                      </tr>
                      <tr>
                          <td width="570" align="right" bgcolor="#00dda9"> <p>{time}</p></td>
                      </tr>
                  </table>
              </td>
          </tr>
          <tr>
              <td>
                  <table id="content-4" cellpadding="0" cellspacing="0" align="center">
                      <tr>
                          <td width="570" valign="top">
                              <h5>Los sensores {sensores} han dejado de enviar datos, favor de reconectarlos.</h5>
                          </td>
                      </tr>
                  </table>
              </td>
          </tr>
      </table>
      </td>
      </tr>
      </table><!-- wrapper -->
  
      </body>
  </html>
  """,subtype='html')

  with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()

    # setup the parameters of the message
    #password = "GIECCUC8"
    #msg['From'] = "UCMX154872@gmail.com"

def email_test(user):
    EMAIL_ADRESS = "GIECC.UCMEXUS@gmail.com"
    EMAIL_PASSWORD = "kvrdhmkhwfrmkaap"

    msg = EmailMessage()
    msg['Subject'] = "Sensores desconectados"
    msg['From'] = EMAIL_ADRESS
    msg['To'] = user

    msg.set_content(f'Mensaje de prueba, si recibió este correo entonces se introdujo bien su correo al programa de monitorizado.')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        smtp.quit()