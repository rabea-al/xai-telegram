from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component, secret

@xai_component(color="blue")
class TelegramInitApp(Component):
    """
    Initializes a Telegram Application using python-telegram-bot.

    ##### inPorts:
    - telegram_token (str): The Bot API token from BotFather.

    ##### outPorts:
    - application (object): The initialized Telegram Application object.
    """
    telegram_token: InCompArg[secret]
    application: OutArg[any]

    def execute(self, ctx) -> None:
        # Import inside execute() if it's only used here
        from telegram.ext import ApplicationBuilder
        
        token = self.telegram_token.value
        if not token:
            raise ValueError("No Telegram token provided!")
        
        app = ApplicationBuilder().token(token).build()
        self.application.value = app


@xai_component(color="blue")
class TelegramAddEchoHandler(Component):
    """
    Adds an echo handler that echoes all text messages back to the user,
    except those that start with '/' (commands).

    ##### inPorts:
    - application (object): The Telegram Application object (from InitTelegramApp).

    ##### outPorts:
    - application (object): The updated Telegram Application with the echo handler attached.
    """
    application: InCompArg[any]
    application_out: OutArg[any]

    def execute(self, ctx) -> None:
        from telegram import Update
        from telegram.ext import MessageHandler, filters, ContextTypes

        async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Simply echo all incoming text messages."""
            if update.message and update.message.text:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=update.message.text
                )

        app = self.application.value
        # Create a filter that grabs all text messages except commands (i.e., no leading '/')
        echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
        app.add_handler(echo_handler)
        
        # Pass the updated app forward
        self.application_out.value = app


@xai_component(color="blue")
class TelegramRunApp(Component):
    """
    Runs the Telegram Application in polling mode.
    This call is blocking until the user stops the execution.

    ##### inPorts:
    - application (object): The Telegram Application (with any handlers attached).
    """
    application: InCompArg[any]

    def execute(self, ctx) -> None:
        app = self.application.value
        if not app:
            raise ValueError("No Telegram Application provided!")
        
        # This is a blocking call, so Xircuits execution will pause here until you stop the bot.
        app.run_polling()
