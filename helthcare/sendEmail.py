from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.conf import settings
# from mysetting import dafultname

dafultname = "http://localhost/"

class Email:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.host=settings.HOST
        self.password=settings.APP_PASS


    def send(self, to_addrs=None, subject=None , HTMLmsg=None):
        print(f"Email Sending==> {to_addrs}")

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.host
        msg['To'] = to_addrs

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(HTMLmsg, 'html')
        msg.attach(part1)
        # Try to log in to server and send email
        try:
            server_ssl = smtplib.SMTP(self.smtp_server, self.port)
            server_ssl.ehlo()
            server_ssl.starttls()
            server_ssl.login(self.host, self.password)
            server_ssl.sendmail(self.host, to_addrs, msg.as_string())
            print(f"Email Sent Success==> {to_addrs}")
            return True

        except Exception as e:
            print("Error--",e)
            return False

        finally:
            try:
                print("COnnection is closed")
                server_ssl.quit()
            except:
                print("COnnection  closed Error")
                pass



    def verifyEmailpage(self ,token=None):
        html = f"""\
        <html>
        <head></head>
        <body
            style="width: auto; height: auto; display: flex; justify-content: center; align-items: center;background-color: white;">

            <div
                style="position: fixed; top: 0; bottom: 0; left: 0;right: 0;margin: auto;background-color: white; width: 600px;height: 500px;border-radius: 12px;">
                <div style="text-align: center;justify-content: center;align-items: center;">
                    <div style="text-align: center;justify-content: center;align-items: center;">
                        <h1
                            style="text-align: center; font-size: 50px; justify-content: center; align-items: center; text-shadow: 1px 1px 1px grey;">
                            DarkStar Tech </h1>
                    </div>
                    <div>
                        <p
                            style="padding: 0px 20px 0px 20px ; text-align: center; font-size: 16px; justify-content: center; align-items: center; color: #5c5b5b; line-height: 1.8; display: block; font-style: normal; font-family: 'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;">
                            Thanks for signing up. We're happy to have you! To finalize your registration, we ask you to confirm
                            you own this email address.</p>
                    </div>

                    <div style="margin-top: 50px;">
                        <a href="{dafultname}verified/{token}"
                            style="margin-top: 30px; text-decoration: none; padding: 8px 30px 8px 30px; font-size: 24px;cursor: pointer;text-align: center; color: #fff;background-color: #0065ff;border: none;border-radius: 25px;">CONFIRM</a>
                    </div>

                    <hr style="margin-top: 70px; background-color: #a1a1a1;  padding: 1px 0px 0px 0px; border: none;">
                    <div>
                        <p
                            style="padding: 0px 80px 0px 60px ; text-align: left; font-size: 16px; justify-content: center; align-items: center; color: #747373; line-height: 1.8; display: block; font-style: normal; font-family: 'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;">
                            Should you have any questions or need any help, please contact us at <a
                                href="{dafultname}contacts">{dafultname}contacts</a></p>

                    </div>
                </div>
                <div
                    style="margin: 50px 0px 10px 20px; justify-content: left; font-family:'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;font-size:13px;font-style:normal;font-weight:400;line-height:1.5;color:#666666">
                    Copyright © DarkStar Tech, Inc.
                </div>

                <div style="margin-bottom: 50px;"></div>
            </div>
            </div>
        </body>
        </html>
        """

        return html

    def forgotPasswordPage(self,name=None,loginlink=None,resetlink=None):
        html = f"""\
        <html>
        <head></head>
        <body
            style="width: auto; height: auto;top: 0px; display: flex; justify-content: center; align-items: center;background-color: white;">

            <div
                style="position: relative; top: 0px; bottom: 0; left: 0;right: 0;margin: auto;background-color: white; width: 600px;height: 700px;border-radius: 12px;">
                <div style="text-align: center;justify-content: center;align-items: center;">
                    <div style="text-align: center;justify-content: center;align-items: center;">
                        <h1
                            style="text-align: center; font-size: 50px; justify-content: center; align-items: center; text-shadow: 1px 1px 1px grey;">
                            DarkStar Tech</h1>
                    </div>
                    <h2 style="text-align: left; justify-content: left;align-items: left; margin-left: 25px;">Hi {name},</h2>
                    <div>
                        <p
                            style="padding: 0px 20px 0px 20px ; text-align: center; font-size: 16px; justify-content: center; align-items: center; color: #5c5b5b; line-height: 1.8; display: block; font-style: normal; font-family: 'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;">
                            We got a message that you forgot your password.
                            If this was you, you can get right back into your account or reset your password now.</p>
                    </div>

                    <div style="margin-top: 50px;">
                        <a href="{loginlink}"
                            style="margin-top: 30px; text-decoration: none; padding: 8px 90px 8px 85px; font-size: 24px;cursor: pointer;text-align: center; color: #fff;background-color: #0065ff;border: none;border-radius: 25px;">
                            Just Login </a>
                    </div>
                    <div style="margin-top: 20px; margin-bottom: 30px;">
                        <a href="{resetlink}"
                            style="margin-top: 30px; text-decoration: none; padding: 8px 30px 8px 30px; font-size: 24px;cursor: pointer;text-align: center; color: #fff;background-color: #0065ff;border: none;border-radius: 25px;">
                            Reset your password</a>
                    </div>
                    <div>
                        <p
                            style="padding: 0px 20px 0px 20px ; text-align: center; font-size: 16px; justify-content: center; align-items: center; color: #5c5b5b; line-height: 1.8; display: block; font-style: normal; font-family: 'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;">
                            If you didn’t request a login link or a password reset, you can ignore this message and <a style="text-decoration: none;" href="{dafultname}contacts">learn more about why you may have received it.</a></p>
                    </div>
                    <hr style="margin-top: 70px; background-color: #a1a1a1;  padding: 1px 0px 0px 0px; border: none;">
                    <div>
                        <p
                            style="padding: 0px 80px 0px 60px ; text-align: left; font-size: 16px; justify-content: center; align-items: center; color: #747373; line-height: 1.8; display: block; font-style: normal; font-family: 'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;">
                            Should you have any questions or need any help, please contact us at <a
                                href="{dafultname}contacts">{dafultname}contacts</a></p>

                    </div>
                </div>
                <div
                    style="margin: 30px 0px 50px 20px; justify-content: left; font-family:'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;font-size:13px;font-style:normal;font-weight:400;line-height:1.5;color:#666666">
                    Copyright © DarkStar Tech, Inc.
                </div>


            </div>
            </div>
        </body>
        </html>
        """

        return html

    def sendInfoPage(self, name, email, devId):

        html = f"""\
        <html>
        <head></head>
        <body
            style="width: auto; height: auto;top: 0px; display: flex; justify-content: center; align-items: center;background-color: white;">

            <div
                style="position: relative; top: 0px; bottom: 0; left: 0;right: 0;margin: auto;background-color: white; width: 600px;height: 700px;border-radius: 12px;">
                <div style="text-align: center;justify-content: center;align-items: center;">
                    <div style="text-align: center;justify-content: center;align-items: center;">
                        <h1
                            style="text-align: center; font-size: 50px; justify-content: center; align-items: center; text-shadow: 1px 1px 1px grey;">
                            DarkStar Tech</h1>
                    </div>
                    <h2 style="text-align: left; justify-content: left;align-items: left; margin-left: 25px;">Hi Aditya Mukhiya,</h2>
                    <div>
                        <h3 style="text-align: left; justify-content: left;align-items: left; margin-left: 40px;margin-bottom: -5px;">
                        Some one just login to MShare Apllication. </h3>
                            <h4 style="text-align: left; justify-content: left;align-items: left; margin-left: 60px;margin-bottom: -20px;">Name : {name}</h4>
                            <h4 style="text-align: left; justify-content: left;align-items: left; margin-left: 60px;margin-bottom: -20px;">Email : {email}</h4>
                            <h4 style="text-align: left; justify-content: left;align-items: left; margin-left: 60px;margin-bottom: -20px;">DevId : {devId}</h4>
                    </div>

                </div>
                <hr style="margin-top: 70px; background-color: #a1a1a1;  padding: 1px 0px 0px 0px; border: none;">
                    <div>
                        <p
                            style="padding: 0px 80px 0px 60px ; text-align: left; font-size: 16px; justify-content: center; align-items: center; color: #747373; line-height: 1.8; display: block; font-style: normal; font-family: 'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;">
                            Should you have any questions or need any help, please contact us at <a
                                href="{dafultname}contacts">{dafultname}contacts</a></p>

                    </div>
                <div
                    style="margin: 30px 0px 50px 20px; justify-content: left; font-family:'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;font-size:13px;font-style:normal;font-weight:400;line-height:1.5;color:#666666">
                    Copyright © DarkStar Tech, Inc.
                </div>


            </div>
            </div>
        </body>
        </html>
        """

        return html

    def send_otp(self, user, otp):

        html = f"""<html>\
        <head></head>
        <body
            style="width: auto; height: auto; display: flex; justify-content: center; align-items: center;background-color: white;">

            <div
                style="position: fixed; top: 0; bottom: 0; left: 0;right: 0;margin: auto;background-color: white; width: 600px;height: 500px;border-radius: 12px;">
                <div style="text-align: center;justify-content: center;align-items: center;">
                    <div style="text-align: center; justify-content: center;align-items: center;">
                        <h1
                            style="text-align: center; font-size: 50px; justify-content: center; align-items: center; text-shadow: 1px 1px 1px grey;">
                            DarkStar Tech </h1>
                    </div>
                    <h6 style="text-align: left; padding: 0px 10px 0px 20px; font-size: 18px; color: rgb(67, 66, 66);" >Dear {user},</h6>
                    <div style="justify-content: center; margin-top: 35px;">
                        <p style="padding: 0px 20px 0px 20px; text-align: left; justify-content: left; align-items: left; margin-top: 35px; font-size: 18px">
                            The OTP towards validating your email address  is: <strong> {otp}</strong></p><br>

                        <p style="padding: 0px 20px 0px 20px; text-align: left; font-weight: 450; font-size: 15.5px; justify-content: left; align-items: left; color: #686666; display: block; font-style: normal; font-family :'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;">
                            This OTP is valid upto 2 Minutes. Do not share it with anyone by any means. This is confidential and to be used by you only.</p>
                    </div>


                    <hr style="margin-top: 70px; background-color: #a1a1a1;  padding: 1px 0px 0px 0px; border: none;">
                    <div>
                        <p
                            style="padding: 0px 20px 0px 20px ; text-align: left; font-size: 16px; justify-content: center; align-items: center; color: #747373; line-height: 1.8; display: block; font-style: normal; font-family: 'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;">
                            Should you have any questions or need any help, please contact us at <a
                                href="{dafultname}contacts">{dafultname}contacts</a></p>

                    </div>
                </div>
                <div
                    style="margin: 50px 0px 10px 20px; justify-content: left; font-family:'Source Sans Pro',-apple-system,BlinkMacSystemFont,'Segoe UI','Helvetica Neue',Arial,sans-serif;font-size:13px;font-style:normal;font-weight:400;line-height:1.5;color:#666666">
                    Copyright © DarkStar Tech, Inc.
                </div>

                <div style="margin-bottom: 50px;"></div>
            </div>
            </div>
        </body>
        </html>"""

        return html

if __name__ == "__main__":
    mail = Email()

