import asyncio
import os
import io
from typing import Union
from telegram import InputFile, Update
from telegram.constants import ChatType, ParseMode, MessageEntityType
from xai_components.base import InArg, OutArg, Component, xai_component


@xai_component(color="blue")
class TelegramInputFile(Component):
    """
    Converts a file path or binary data into a telegram.InputFile.

    ##### inPorts:
    - data (Union[str, bytes]): Either a file path (str) or binary data (bytes).

    ##### outPorts:
    - input_file (InputFile): The resulting InputFile object.
    """
    data: InArg[Union[str, bytes]]

    input_file: OutArg[InputFile]

    def execute(self, ctx) -> None:
        data = self.data.value

        # If data is a string and corresponds to an existing file path, open that file.
        if isinstance(data, str) and os.path.exists(data):
            file_obj = open(data, "rb")
            self.input_file.value = InputFile(file_obj)
        # If data is bytes, wrap it with BytesIO.
        elif isinstance(data, bytes):
            file_obj = io.BytesIO(data)
            self.input_file.value = InputFile(file_obj)
        else:
            raise ValueError("Data must be a valid file path or binary data.")


@xai_component(color="green")
class TelegramSendImage(Component):
    """
    Uses app.bot.send_photo to send an image in a Telegram chat.

    ##### inPorts:
    - application (object): Telegram Application object.
    - chat_id (int): The ID of the chat where the image will be sent.
    - input_file (InputFile): Telegram InputFile object containing the image.
    - caption (str): Optional caption for the image.
    - reply_to_message_id (int): Optional message ID to reply to.

    ##### outPorts:
    None
    """
    application: InArg[object]
    chat_id: InArg[int]
    input_file: InArg[InputFile]
    caption: InArg[str]
    reply_to_message_id: InArg[int]

    def execute(self, ctx) -> None:
        app = self.application.value or ctx.get("telegram_app")
        chat_id = self.chat_id.value
        input_file = self.input_file.value
        caption = self.caption.value or None
        reply_to_message_id = self.reply_to_message_id.value

        if not (app and chat_id and input_file):
            raise ValueError("Application, chat_id, and input_file are required.")

        async def send_image():
            try:
                await app.bot.send_photo(
                    chat_id=chat_id,
                    photo=input_file,
                    caption=caption,
                    reply_to_message_id=reply_to_message_id,
                    parse_mode=ParseMode.HTML,
                )
            except Exception as e:
                raise ValueError(f"Failed to send the image: {e}")

        loop = asyncio.get_event_loop()
        loop.create_task(send_image())


@xai_component(color="green")
class TelegramSendPDF(Component):
    """
    Sends a PDF document in a Telegram chat.

    ##### inPorts:
    - application (object): Telegram Application object.
    - chat_id (int): The ID of the chat where the PDF will be sent.
    - input_file (InputFile): Telegram InputFile object containing the PDF.
    - caption (str): Optional caption for the document.
    - reply_to_message_id (int): Optional message ID to reply to.

    ##### outPorts:
    None
    """
    application: InArg[object]
    chat_id: InArg[int]
    input_file: InArg[InputFile]
    caption: InArg[str]
    reply_to_message_id: InArg[int]

    def execute(self, ctx) -> None:
        app = self.application.value or ctx.get("telegram_app")
        chat_id = self.chat_id.value
        input_file = self.input_file.value
        caption = self.caption.value or None
        reply_to_message_id = self.reply_to_message_id.value

        if not (app and chat_id and input_file):
            raise ValueError("Application, chat_id, and input_file are required.")

        async def send_pdf():
            await app.bot.send_document(
                chat_id=chat_id,
                document=input_file,
                caption=caption,
                reply_to_message_id=reply_to_message_id,
                parse_mode=ParseMode.HTML,
            )

        loop = asyncio.get_event_loop()
        loop.create_task(send_pdf())


@xai_component(color="green")
class TelegramSendAudio(Component):
    """
    Sends an audio file in a Telegram chat.

    ##### inPorts:
    - application (object): Telegram Application object.
    - chat_id (int): The ID of the chat where the audio will be sent.
    - input_file (InputFile): Telegram InputFile object containing the audio.
    - caption (str): Optional caption for the audio file.
    - reply_to_message_id (int): Optional message ID to reply to.

    ##### outPorts:
    None
    """
    application: InArg[object]
    chat_id: InArg[int]
    input_file: InArg[InputFile]
    caption: InArg[str]
    reply_to_message_id: InArg[int]

    def execute(self, ctx) -> None:
        app = self.application.value or ctx.get("telegram_app")
        chat_id = self.chat_id.value
        input_file = self.input_file.value
        caption = self.caption.value or None
        reply_to_message_id = self.reply_to_message_id.value

        if not (app and chat_id and input_file):
            raise ValueError("Application, chat_id, and input_file are required.")

        async def send_audio():
            await app.bot.send_audio(
                chat_id=chat_id,
                audio=input_file,
                caption=caption,
                reply_to_message_id=reply_to_message_id,
                parse_mode=ParseMode.HTML,
            )

        loop = asyncio.get_event_loop()
        loop.create_task(send_audio())


@xai_component(color="green")
class TelegramSendVideo(Component):
    """
    Sends a video file in a Telegram chat.

    ##### inPorts:
    - application (object): Telegram Application object.
    - chat_id (int): The ID of the chat where the video will be sent.
    - input_file (InputFile): Telegram InputFile object containing the video.
    - caption (str): Optional caption for the video file.
    - reply_to_message_id (int): Optional message ID to reply to.

    ##### outPorts:
    None
    """
    application: InArg[object]
    chat_id: InArg[int]
    input_file: InArg[InputFile]
    caption: InArg[str]
    reply_to_message_id: InArg[int]

    def execute(self, ctx) -> None:
        app = self.application.value or ctx.get("telegram_app")
        chat_id = self.chat_id.value
        input_file = self.input_file.value
        caption = self.caption.value or None
        reply_to_message_id = self.reply_to_message_id.value

        if not (app and chat_id and input_file):
            raise ValueError("Application, chat_id, and input_file are required.")

        async def send_video():
            await app.bot.send_video(
                chat_id=chat_id,
                video=input_file,
                caption=caption,
                reply_to_message_id=reply_to_message_id,
                parse_mode=ParseMode.HTML,
            )

        loop = asyncio.get_event_loop()
        loop.create_task(send_video())
