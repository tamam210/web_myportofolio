import base64

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://gwuser:GANTI_PASSWORD@127.0.0.1:3306/mycv"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Email pemilik portfolio (kamu)
    contact_email: str = "tamam.niamillah.rpw@gmail.com"

    # Opsional: kirim notifikasi pertanyaan pending ke email kamu.
    # Gmail butuh "App Password" (aktifkan 2-Step Verification dulu).
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""

    # Jangan isi dua-duanya. Pilih salah satu:
    #  - smtp_password      : password mentah (kalau mau, tapi nggak disarankan)
    #  - smtp_password_b64  : password yang udah di-encode base64 (disarankan)
    smtp_password: str = ""
    smtp_password_b64: str = ""

    # Admin halaman /admin. Password JANGAN diisi mentah — isi bcrypt-hash,
    # hash-nya dibikin lewat script: .venv/bin/python create_admin_password.py
    admin_username: str = "admin"
    admin_password_hash: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    @property
    def smtp_password_decoded(self) -> str:
        if self.smtp_password_b64:
            try:
                return base64.b64decode(self.smtp_password_b64).decode("utf-8")
            except Exception:
                return ""
        return self.smtp_password

    @property
    def smtp_enabled(self) -> bool:
        return bool(self.smtp_host and self.smtp_user and self.smtp_password_decoded)


settings = Settings()