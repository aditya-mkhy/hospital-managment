# Password Validator

class Validator:
    def __init__(self, passwd: str = None, email="", name="", username="") -> None:
        self.passwd = passwd
        self.email = email
        self.name = name
        self.username = username

        self.passwd_min_length = 8


    def check_length(self):
        if len(self.passwd) < self.passwd_min_length:
            error = f"Please create a password that is at least {self.passwd_min_length} characters in length"
            return error

        return False

    def check_isnumeric(self):
        if self.passwd.isnumeric():
            return "Your password can't be entirely numeric."
        return False

    def check_number(self):
        count = 0
        for ch in self.passwd:
            if ch.isdigit():
                count += 1

        if count >= 2:
            return False
        else:
            return "Password must contain atleast two or more numbers."

    def check_upper_lower_ch(self):
        up_count = 0
        low_count = 0

        for ch in self.passwd:
            if ch.islower():
                low_count += 1

            elif ch.isupper():
                up_count += 1

        if up_count == 0:
            return "Use atleast one uppercase letter in your password."

        elif low_count == 0:
            return "Use atleast one lowercase letter in your password."

        else:
            return False

    def check_special_char(self):
        sp = """ !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
        for c in self.passwd:
            if c in sp:
                return False
        return "Use atleast one Special Character in your password."

    def check_phone(self):
        fnum = ""
        for num in self.passwd:
            if num in self.phone:
                fnum += num
                if len(fnum) > 2:
                    return f"Your password can't contain three or more than three contiguous digits from your phone number. [{fnum}]"
            else:
                fnum = ""

        return False



    def check_email(self):
        email = self.email[:self.email.find("@")]

        if email in self.passwd.lower():
            return "Your password can't contain the part of your email address."

        return False

    def check_name(self):
        for name in self.name.split(" "):
            if name.strip() != "":
                if name.lower() in self.passwd.lower():
                    return "Password can't contain your name."

        return False



    def validate(self):
        error = self.check_length()
        if error:
            return error

        error = self.check_isnumeric()
        if error:
            return error

        error = self.check_upper_lower_ch()
        if error:
            return error

        error = self.check_number()
        if error:
            return error

        error = self.check_special_char()
        if error:
            return error

        error = self.check_email()
        if error:
            return error

        error = self.check_name()
        if error:
            return error

    

        return False





if __name__ == "__main__":
    passwd = "mahadeAditmk65765@"

    valid = Validator(passwd=passwd, email="mahadev@gmail.com", name="Aditya Mukhiya", phone="6230658655")

    error = valid.validate()
    print(f"Error==> {error}")
