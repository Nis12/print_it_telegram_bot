from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from .config import PrintBotConfig
from .file_manager import FileManager
from .printer import CupsPrinter
from .converter import LibreOfficeConverter
from .handlers import BotHandlers

_TOKEN = "___"

def main():
    print("Start bot...")
    config = PrintBotConfig()
    fm = FileManager("../.printbot/files", 14)
    printer = CupsPrinter(config.get_printer_name())
    converter = LibreOfficeConverter("../.printbot/files")

    handlers = BotHandlers(config, fm, printer, converter)

    app = Application.builder().token(_TOKEN).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(MessageHandler(filters.Document.ALL, handlers.handle_document))
    app.add_handler(CallbackQueryHandler(handlers.button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()