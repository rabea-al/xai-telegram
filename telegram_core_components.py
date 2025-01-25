from xai_components.base import InArg, OutArg, InCompArg, Component, xai_component, secret, SubGraphExecutor

import asyncio
from telegram import Update
from telegram.constants import ChatType, ParseMode
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes


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
        from telegram.ext import ApplicationBuilder
        
        token = self.telegram_token.value
        if not token:
            raise ValueError("No Telegram token provided!")
        
        app = ApplicationBuilder().token(token).build()
        self.application.value = app
        
        # Store the application in the context for global access
        ctx['telegram_app'] = app


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

        async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
            """Simply echo all incoming text messages."""
            if update.message and update.message.text:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, 
                    text=update.message.text
                )

        app = self.application.value or ctx.get('telegram_app')  # Retrieve from ctx if not provided
        if not app:
            raise ValueError("Telegram Application not found in input or context!")
        
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
    application: InArg[any]

    def execute(self, ctx) -> None:
        app = self.application.value or ctx.get('telegram_app')  # Retrieve from ctx if not provided
        if not app:
            raise ValueError("Telegram Application not found in input or context!")
        
        # This is a blocking call, so Xircuits execution will pause here until you stop the bot.
        app.run_polling()


@xai_component(color="blue")
class TelegramAddMessageEvent(Component):
    """
    A unified component that handles text messages under two modes:

    1) require_bot_mention = True (Default):
       - In private chats, all text is handled (no mention needed).
       - In group chats, only messages @mentioning the bot are handled.
    2) require_bot_mention = False:
       - In all chats (group or private), all text messages are handled.

    You must supply `bot_username` if you enable mentions, e.g. 'MyBotUsername'.
    Leading '@' is optional.

    #### inPorts:
    - application (object): Telegram Application (from TelegramInitApp).
    - event_name (str): Xircuits event name to fire.
    - require_bot_mention (bool): Default True. If True, only handle messages if
      private chat OR the user mentions the bot. If False, handle all text messages.
    - bot_username (str): The bot's username, e.g. "MyBotUsername" (optional if
      require_bot_mention=False, required if True).

    #### outPorts:
    - application_out (object): Updated Telegram application with the message handler.

    """

    application: InArg[object]
    event_name: InArg[str]
    require_bot_mention: InArg[bool]
    bot_username: InArg[str]

    application_out: OutArg[object]

    def execute(self, ctx) -> None:
        app = self.application.value or ctx.get('telegram_app')
        if not app:
            raise ValueError("Telegram Application not found in input or context!")

        event_name = (self.event_name.value or "").strip()
        if not event_name:
            raise ValueError("event_name is required to trigger subgraphs.")

        require_mention = self.require_bot_mention.value
        if require_mention is None:
            require_mention = True

        # Build the filter
        if require_mention:
            # Must have the bot username
            username = self.bot_username.value
            if not username:
                raise ValueError(
                    "bot_username is required when require_bot_mention is True."
                )
            # Mention filter
            mention_filter = filters.Mention(username)
            # Combine mention in group OR private chat
            combined_filter = (mention_filter | filters.ChatType.PRIVATE) & filters.TEXT
        else:
            # Respond to all text in any chat
            combined_filter = filters.TEXT

        async def _callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
            if update.message and update.message.text:
                payload = {
                    "update": update,
                    "chat_id": update.effective_chat.id,
                    "user_id": update.effective_user.id if update.effective_user else None,
                    "text": update.message.text,
                    "is_command": update.message.text.startswith('/'),
                }
                # Trigger the event in Xircuits
                listeners = ctx.get('events', {}).get(event_name, [])
                for listener in listeners:
                    listener.payload.value = payload
                    SubGraphExecutor(listener).do(ctx)

        handler = MessageHandler(combined_filter, _callback)
        app.add_handler(handler)
        self.application_out.value = app

@xai_component(color="green")
class TelegramAddCommandEvent(Component):
    """
    Registers a Telegram command handler that will fire an event in the Xircuits context
    whenever the command is received.

    ##### inPorts:
    - application (object): The Telegram Application object
    - command_name (str): The command (without slash), e.g. "start"
    - event_name (str): The event name to fire in Xircuits, e.g. "my_command_event"

    ##### outPorts:
    - application_out (object): The updated Telegram Application
    """
    application: InArg[object]
    command_name: InArg[str]
    event_name: InArg[str]
    application_out: OutArg[object]

    def execute(self, ctx) -> None:
        app = self.application.value or ctx.get('telegram_app')  # Retrieve from ctx if not provided
        if not app:
            raise ValueError("Telegram Application not found in input or context!")

        cmd = self.command_name.value.strip()
        evt = self.event_name.value.strip()

        if not (cmd and evt):
            raise ValueError("command_name and event_name are required.")

        async def command_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
            # This is called each time user does /<cmd>.
            message_text = " ".join(context.args) if context.args else ""
            chat_id = update.effective_chat.id
            user_id = update.effective_user.id if update.effective_user else None

            payload = {
                "command_name": cmd,
                "message_text": message_text,
                "chat_id": chat_id,
                "user_id": user_id,
                "update": update,
            }
            listeners = ctx.get('events', {}).get(evt, [])
            for listener in listeners:
                listener.payload.value = payload
                SubGraphExecutor(listener).do(ctx)

        handler = CommandHandler(cmd, command_callback)
        app.add_handler(handler)
        self.application_out.value = app

@xai_component
class TelegramParsePayload(Component):
    """
    Unpacks the standard Telegram payload fields from an event payload dictionary.
    This component now handles both normal messages ("text") and command messages
    ("message_text"), pulling whichever is present.

    ##### inPorts:
    - event_payload (dict): A dictionary containing keys like:
        {
          "text": str,           # For normal messages
          "message_text": str,   # For commands
          "command_name": str,
          "chat_id": int,
          "user_id": int,
          "update": <telegram.Update>
          ...
        }

    ##### outPorts:
    - chat_id (int): The chat ID where the message was sent.
    - user_id (int): The user's Telegram ID.
    - message_text (str): The user's message text or command arguments (whichever is present).
    - update_obj (object): The entire Update object (telegram.Update).
    - command_name (str): The command name (if provided in payload).
    - first_name (str): The first_name from update.effective_user (if available).

    ##### Usage:
    1. Wire the `event_payload` from an event-based component (e.g. TelegramAddMessageEvent or
       TelegramAddCommandEvent) into `TelegramParsePayload`.
    2. Use the outPorts (chat_id, message_text, etc.) in subsequent components.
    """

    event_payload: InArg[dict]

    chat_id: OutArg[int]
    user_id: OutArg[int]
    message_text: OutArg[str]
    update_obj: OutArg[object]
    command_name: OutArg[str]
    first_name: OutArg[str]

    def execute(self, ctx) -> None:
        payload = self.event_payload.value or {}
        self.chat_id.value = payload.get("chat_id")
        self.user_id.value = payload.get("user_id")

        # Handle both normal messages ("text") and commands ("message_text")
        msg_text = payload.get("message_text")
        if not msg_text:
            msg_text = payload.get("text")

        self.message_text.value = msg_text
        self.update_obj.value = payload.get("update")
        self.command_name.value = payload.get("command_name")

        # Optionally derive `first_name` from the update if user data is available
        first_name = ""
        update = payload.get("update")
        if update and update.effective_user:
            first_name = update.effective_user.first_name or ""
        self.first_name.value = first_name


@xai_component(color="green")
class TelegramReplyToMessageEvent(Component):
    """
    Sends a reply in a Telegram chat, quoting the original message from an event payload.

    ##### inPorts:
    - application (object): Telegram Application object
    - event_payload (dict): The payload containing info such as 'update', 'chat_id', etc.
    - reply_text (str): The text you want to send as a reply

    ##### outPorts:
    None
    """
    application: InArg[object]
    event_payload: InArg[dict]
    reply_text: InArg[str]

    def execute(self, ctx) -> None:
        app = self.application.value or ctx.get('telegram_app')  # Retrieve from ctx if not provided
        payload = self.event_payload.value
        reply_text = self.reply_text.value

        if not app:
            raise ValueError("Telegram Application not found in input or context!")
        if not payload:
            raise ValueError("No event_payload provided, can't reply.")

        update = payload.get('update')
        if not update:
            raise ValueError("No 'update' in event_payload, cannot reply.")

        chat_id = update.effective_chat.id
        message_id = update.effective_message.message_id
        
        async def _send_reply():
            await app.bot.send_message(
                chat_id=chat_id,
                text=reply_text,
                parse_mode=ParseMode.HTML,
                reply_to_message_id=message_id  # This quotes the original
            )

        loop = asyncio.get_event_loop()
        loop.create_task(_send_reply())
