#!/usr/bin/env python2.4
# coding: utf-8
'''
ATENÇÃO, ESTA LIB DEPENDE DO ARQUIVO: ../imgs/logo.png
NOME DA LIB:        sendMail.py
VERSÃO:             1.0
OBJETIVO:           ENVIO DE E-MAILS COM E SEM ANEXO
DESCRIÇÃO:          POSSIBILITA O ENVIO DE E-MAILS COM OU SEM ANEXO PARA VARIOS E-MAILS
                    É POSSÍVEL INSERIR 4 LINHAS NO CORPO DO E-MAIL PODENDO EXTENDER UTILIZANDO TAGS HTML
HISTÓRICO:          V1.0 - 17/04/2020   DANIEL ALVES DIAS JUNIOR
                                        - INSERIDO EM PRODUÇÃO.
'''
import smtplib, time, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email import Encoders

class Email:
    def __init__(self, filename, diretorioPython):
        self.filename = filename
        self.diretorioPython = diretorioPython

    def enderecoFrom(self, From):
        self.From = From

    def enderecosTo(self, emails):
        self.emails = emails

    def assunto(self, assunto):
        self.assunto = assunto
    
    def corpo(self, linha01, linha02, linha03, linha04):
        self.linha01 = linha01
        self.linha02 = linha02
        self.linha03 = linha03
        self.linha04 = linha04
    
    def assinatura(self, assinatura):
        self.assinatura = assinatura

    def enviar_anexo(self):
        path, file = os.path.split(self.filename)
        
        msg = MIMEMultipart()
        msg['Subject'] = self.assunto
        msg['From'] = self.From
        msg['CCO'] = ', '.join(self.emails)
        
        #toaddr = msg['To']
        
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(self.filename, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename=' + file + '')
        
        friendMsg = saudacao(int(time.strftime('%H')))
        
        html = '''
        <html>
        <head>
        <meta http-equiv='Content-Type' content='text/html; charset='UTF-8'>
        </head>
        <body>
            <div style='margin: 30; padding: .2em;'>
                <img src='cid:logo.png' width='91' height='89' align='left'>                     
            </div>
            <br />
            <br />
            <br />
            <br />
            <br />
            <div style='margin: 30; padding: .2em; font-family: Verdana, Geneva, sans-serif; font-size: 11px;'>
                <h1>%s,</h1>
                Segue em anexo o arquivo <b>%s</b>
                <br /><br />
                <b>%s</b>
                <br /><br />
                <b>%s</b> 
                <br /><br />
                <b>%s</b> 
                <br /><br /> 
                <b>%s</b> 
                <br /><br />
                Grato,
                <br /><br />
                %s
                <br />
                <br />
                <span style='font-size: 8px';>> Essa é uma mensagem automática, gentileza não responder.</span>
            </div>
        </body>
        </html>
        ''' % (friendMsg, file, self.linha01, self.linha02, self.linha03, self.linha04, self.assinatura)

        msg.attach(MIMEText(html, 'html'))
        
        fp = open('%s/imgs/'%(self.diretorioPython) + 'logo.png', 'rb')
        msgImgLOGO = MIMEImage(fp.read())
        fp.close()
        
        msgImgLOGO.add_header('Content-ID', '<logo.png>')
        msg.attach(msgImgLOGO)
        msg.attach(part)
        
        s = smtplib.SMTP('localhost')
        s.sendmail(self.From, self.emails, msg.as_string())
        s.quit()

    def enviar(self):
        path, file = os.path.split(self.filename)
        
        msg = MIMEMultipart()
        msg['Subject'] = self.assunto
        msg['From'] = self.From
        msg['CCO'] = ', '.join(self.emails)
        
        #toaddr = msg['To']
        
        #part = MIMEBase('application', 'octet-stream')
        #part.set_payload(open(self.filename, 'rb').read())
        #Encoders.encode_base64(part)
        #part.add_header('Content-Disposition', 'attachment; filename='' + file + ''')
        
        friendMsg = saudacao(int(time.strftime('%H')))
        
        html = '''
        <html>
        <head>
        <meta http-equiv='Content-Type' content='text/html; charset='UTF-8'>
        </head>
        <body>
            <div style='margin: 30; padding: .2em;'>
                <img src='cid:logo.png' width='91' height='89' align='left'>                     
            </div>
            <br />
            <br />
            <br />
            <br />
            <br />
            <div style='margin: 30; padding: .2em; font-family: Verdana, Geneva, sans-serif; font-size: 11px;'>
                <h1>%s,</h1>
                <br /><br />
                <b>%s</b>
                <br /><br />
                <b>%s</b> 
                <br /><br />
                <b>%s</b> 
                <br /><br /> 
                <b>%s</b> 
                <br /><br />
                Grato,
                <br /><br />
                %s
                <br />
                <br />
                <span style='font-size: 8px';>> Essa é uma mensagem automática, gentileza não responder.</span>
            </div>
        </body>
        </html>
        ''' % (friendMsg, self.linha01, self.linha02, self.linha03, self.linha04, self.assinatura)

        msg.attach(MIMEText(html, 'html'))
        
        fp = open('%s/imgs/'%(self.diretorioPython) + 'dxc.png', 'rb')
        msgImgLOGO = MIMEImage(fp.read())
        fp.close()
        
        msgImgLOGO.add_header('Content-ID', '<logo.png>')
        msg.attach(msgImgLOGO)
        #msg.attach(part)
        
        s = smtplib.SMTP('LOCALHOST')
        s.sendmail(self.From, self.emails, msg.as_string())
        s.quit()

def saudacao(hour_now):
    if 6 < hour_now < 12:
        friendMsg = "Bom dia"
    elif 18 > hour_now >= 12:
        friendMsg = "Boa tarde"
    elif hour_now >= 18 or 0 <= hour_now <= 6:
        friendMsg = "Boa noite"
    return friendMsg