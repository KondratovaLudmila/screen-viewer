import time 
import pyotp 
import qrcode

from pathlib import Path


from screen_viewer.settings import OTP_APP_NAME, MEDIA_ROOT


class TOTPHandler:
    APP_NAME = OTP_APP_NAME
    QR_PATH = MEDIA_ROOT

    def get_uri(self, key: str, username: str) -> str:
        
        uri = pyotp.totp.TOTP(key)\
            .provisioning_uri(name=username, 
                              issuer_name=self.APP_NAME) 
        
        return uri

    def get_qrcode(self, key: str, username: str) -> str:
        uri = self.get_uri(key, username)
        path = str(Path(self.QR_PATH, f"{username}_qr.png"))
        qrcode.make(uri).save(path)
        return f"{username}_qr.png"


    def check_otp(self, key: str, password: str) -> bool:
        totp = pyotp.TOTP(key)
        return totp.verify(password)
    

    def clean_up(self, username: str) -> None:
        path = Path(self.QR_PATH, f"{username}_qr.png")
        if path.exists():
            path.unlink()
        
        
totp_handler = TOTPHandler()