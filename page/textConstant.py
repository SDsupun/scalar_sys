class TextConst:
    cond="CREATE USER 'scal_user'@'localhost' IDENTIFIED BY 'tH@r@236';"
    def __init__(self, lang_sinhala):
        if lang_sinhala:
            self.login_page_passwd = "Enter Password"

        else:
            self.login_page_passwd = "රහස් පදය"
