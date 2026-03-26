"""
邮件发送服务
支持验证码、通知等邮件发送
"""
import random
import string
from datetime import datetime, timedelta, timezone
from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings


class EmailService:
    """邮件服务类"""

    def __init__(self):
        # 验证码缓存（生产环境应使用Redis）
        self._verification_codes = {}
        # 密码重置码缓存
        self._reset_codes = {}

    def generate_code(self, length: int = 6) -> str:
        """生成验证码"""
        return ''.join(random.choices(string.digits, k=length))

    def save_code(self, email: str, code: str, expire_minutes: int = 5) -> None:
        """保存验证码（带过期时间）"""
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        self._verification_codes[email] = {
            'code': code,
            'expire_time': expire_time,
            'used': False
        }

    def verify_code(self, email: str, code: str) -> bool:
        """验证验证码"""
        if email not in self._verification_codes:
            return False

        stored_data = self._verification_codes[email]

        # 检查是否已使用
        if stored_data['used']:
            return False

        # 检查是否过期
        if datetime.now(timezone.utc) > stored_data['expire_time']:
            # 清除过期验证码
            del self._verification_codes[email]
            return False

        # 验证码匹配
        if stored_data['code'] == code:
            # 标记为已使用
            stored_data['used'] = True
            return True

        return False

    async def send_verification_email(
        self,
        email: str,
        code: str
    ) -> bool:
        """发送验证码邮件"""
        try:
            # 邮件内容
            subject = "【AI简历平台】邮箱验证码"
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #333;">邮箱验证</h2>
                    <p>您好，</p>
                    <p>您正在注册AI简历智能生成平台，验证码如下：</p>
                    <div style="background-color: #f0f0f0; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; margin: 20px 0;">
                        {code}
                    </div>
                    <p>验证码有效期为 <strong>5分钟</strong>，请尽快完成验证。</p>
                    <p>如果这不是您的操作，请忽略此邮件。</p>
                    <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
                    <p style="color: #999; font-size: 12px;">
                        此邮件由系统自动发送，请勿直接回复。<br>
                        © 2025 AI简历智能生成平台. All rights reserved.
                    </p>
                </div>
            </body>
            </html>
            """

            # 开发环境：打印到日志
            if getattr(settings, 'DEBUG', False):
                print(f"\n{'='*50}")
                print(f"📧 邮件发送模拟")
                print(f"收件人: {email}")
                print(f"验证码: {code}")
                print(f"有效期: 5分钟")
                print(f"{'='*50}\n")
                return True

            # 生产环境：实际发送邮件
            # TODO: 配置SMTP服务器
            # msg = MIMEMultipart('alternative')
            # msg['Subject'] = subject
            # msg['From'] = settings.SMTP_USER
            # msg['To'] = email
            #
            # html_part = MIMEText(body, 'html')
            # msg.attach(html_part)
            #
            # with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            #     server.starttls()
            #     server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            #     server.send_message(msg)

            return True

        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False

    async def send_notification_email(
        self,
        email: str,
        subject: str,
        content: str
    ) -> bool:
        """发送通知邮件"""
        try:
            # 开发环境：打印到日志
            if getattr(settings, 'DEBUG', False):
                print(f"\n{'='*50}")
                print(f"📧 通知邮件")
                print(f"收件人: {email}")
                print(f"主题: {subject}")
                print(f"内容: {content}")
                print(f"{'='*50}\n")
                return True

            # 生产环境：实际发送邮件
            # TODO: 实现邮件发送
            return True

        except Exception as e:
            print(f"发送邮件失败: {e}")
            return False

    def cleanup_expired_codes(self) -> None:
        """清理过期的验证码"""
        now = datetime.now(timezone.utc)
        expired_emails = [
            email for email, data in self._verification_codes.items()
            if now > data['expire_time']
        ]
        for email in expired_emails:
            del self._verification_codes[email]

    def save_reset_code(self, email: str, code: str, expire_minutes: int = 15) -> None:
        """保存密码重置码（带过期时间）"""
        expire_time = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
        self._reset_codes[email] = {
            'code': code,
            'expire_time': expire_time,
            'used': False
        }

    def verify_reset_code(self, email: str, code: str) -> bool:
        """验证密码重置码"""
        if email not in self._reset_codes:
            return False

        stored_data = self._reset_codes[email]

        # 检查是否已使用
        if stored_data['used']:
            return False

        # 检查是否过期
        if datetime.now(timezone.utc) > stored_data['expire_time']:
            # 清除过期重置码
            del self._reset_codes[email]
            return False

        # 验证码匹配
        if stored_data['code'] == code:
            # 标记为已使用
            stored_data['used'] = True
            return True

        return False

    async def send_password_reset_email(
        self,
        email: str,
        code: str
    ) -> bool:
        """发送密码重置邮件"""
        try:
            # 邮件内容
            subject = "【AI简历平台】密码重置验证码"
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #333;">密码重置</h2>
                    <p>您好，</p>
                    <p>我们收到了您的密码重置请求，验证码如下：</p>
                    <div style="background-color: #f0f0f0; padding: 20px; text-align: center; font-size: 24px; font-weight: bold; letter-spacing: 5px; margin: 20px 0;">
                        {code}
                    </div>
                    <p>验证码有效期为 <strong>15分钟</strong>，请尽快完成密码重置。</p>
                    <p>如果这不是您的操作，请忽略此邮件，您的密码不会被修改。</p>
                    <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
                    <p style="color: #999; font-size: 12px;">
                        此邮件由系统自动发送，请勿直接回复。<br>
                        © 2025 AI简历智能生成平台. All rights reserved.
                    </p>
                </div>
            </body>
            </html>
            """

            # 开发环境：打印到日志
            if getattr(settings, 'DEBUG', False):
                print(f"\n{'='*50}")
                print(f"📧 密码重置邮件")
                print(f"收件人: {email}")
                print(f"重置码: {code}")
                print(f"有效期: 15分钟")
                print(f"{'='*50}\n")
                return True

            # 生产环境：实际发送邮件
            # TODO: 配置SMTP服务器
            return True

        except Exception as e:
            print(f"发送密码重置邮件失败: {e}")
            return False


# 全局实例
email_service = EmailService()
