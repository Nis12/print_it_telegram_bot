import os
import uuid

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes


from .converter import IFileConverter
from .file_manager import FileManager
from .logger import log_print_status
from .printer import IPrinter
from .config import PrintBotConfig

ALLOWED_FORMATS = ['.pdf', '.docx', '.doc', '.rtf', '.txt', '.odt']

class BotHandlers:
    def __init__(self, config: PrintBotConfig, fm: FileManager, printer: IPrinter, converter: IFileConverter):
        self.config = config
        self.fm = fm
        self.printer = printer
        self.converter = converter

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user

        if self.config.is_admin(user.id):
            await update.message.reply_text("Hello, admin! 👑")
        elif self.config.is_user_allowed(user.id):
            await update.message.reply_text("Hi! 👋, Send the document for printing.")
        elif self.config.is_user_pending(user.id):
            await update.message.reply_text("Your registration request is under consideration.")
        else:
            kb = [[InlineKeyboardButton("Registration", callback_data="register")]]
            await update.message.reply_text(
                "⛔ There is no access. Please register:",
                reply_markup=InlineKeyboardMarkup(kb)
            )

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("❓ Unknown team. Try /start")

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        if not self.config.is_user_allowed(user.id):
            await update.message.reply_text("⛔ No rights.")
            return

        document = update.message.document
        ext = document.file_name.lower().split('.')[-1]
        if f".{ext}" not in ALLOWED_FORMATS:
            await update.message.reply_text(f"❌ The format is not supported. Available formats: {ALLOWED_FORMATS}")
            return

        path = self.fm.get_safe_path(document.file_name)
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(path)

        file_id = str(uuid.uuid4())
        context.user_data[file_id] = path

        kb = [[
            InlineKeyboardButton("✅ Print", callback_data=f"print_{file_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{file_id}")
        ]]
        await update.message.reply_text("Confirm the print:", reply_markup=InlineKeyboardMarkup(kb))

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data

        if data == "register":
            user = query.from_user
            username = f"@{user.username}" if user.username else f"{user.first_name}"

            self.config.add_pending_user(user.id)

            kb = [
                [
                    InlineKeyboardButton("✅ Accept", callback_data=f"approve_{user.id}"),
                    InlineKeyboardButton("❌ Reject", callback_data=f"reject_{user.id}")
                ]
            ]

            await context.bot.send_message(
                chat_id=self.config.admin_id(),
                text=f"🔔 New registration request:\n{username} (ID: {user.id})",
                reply_markup=InlineKeyboardMarkup(kb)
            )

            await query.edit_message_text("✅ The registration request has been sent. Expect approval.")
            return

        if data.startswith("approve_") or data.startswith("reject_"):
            action, user_id_str = data.split("_", 1)
            user_id = int(user_id_str)

            if query.from_user.id != self.config.admin_id():
                await query.edit_message_text("⛔ Only the admin can perform this action..")
                return

            if action == "approve":
                self.config.approve_user(user_id)
                await query.edit_message_text("✅ The user has been added!")
                try:
                    await context.bot.send_message(chat_id=user_id, text="✅ Your registration has been approved!")
                except:
                    pass
            elif action == "reject":
                self.config.reject_user(user_id)
                await query.edit_message_text("❌ The application was rejected.")
                try:
                    await context.bot.send_message(chat_id=user_id, text="❌ Your registration has been rejected.")
                except:
                    pass
            return

        # --- Обработка кнопок печати ---
        parts = data.split('_', 1)
        if len(parts) != 2:
            await query.edit_message_text("Button data error.")
            return

        action, file_id = parts
        file_path = context.user_data.get(file_id)

        if not file_path or not os.path.exists(file_path):
            await query.edit_message_text("File not found 😔")
            return

        if action == "print":
            if not file_path.lower().endswith('.pdf'):
                pdf_path = self.converter.convert_to_pdf(file_path)
                if pdf_path:
                    file_path = pdf_path
                else:
                    await query.edit_message_text("❌ Couldn't convert the file to PDF.")
                    return

            self.printer.print_file(file_path)
            log_print_status(file_path, "SUCCESS", query.from_user.id)
            await query.edit_message_text("🖨️ The document has been sent for printing!")
        elif action == "cancel":
            try:
                os.remove(file_path)
                await query.edit_message_text("❌ Cancelled.")
            except:
                await query.edit_message_text("❌ Couldn't delete.")
