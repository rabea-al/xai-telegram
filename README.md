<p align="center">
  <a href="https://github.com/XpressAI/xircuits/tree/master/xai_components#xircuits-component-library-list">Component Libraries</a> •
  <a href="https://github.com/XpressAI/xircuits/tree/master/project-templates#xircuits-project-templates-list">Project Templates</a>
  <br>
  <a href="https://xircuits.io/">Docs</a> •
  <a href="https://xircuits.io/docs/Installation">Install</a> •
  <a href="https://xircuits.io/docs/category/tutorials">Tutorials</a> •
  <a href="https://xircuits.io/docs/category/developer-guide">Developer Guides</a> •
  <a href="https://github.com/XpressAI/xircuits/blob/master/CONTRIBUTING.md">Contribute</a> •
  <a href="https://www.xpress.ai/blog/">Blog</a> •
  <a href="https://discord.com/invite/vgEg2ZtxCw">Discord</a>
</p>

<p align="center">Xircuits Component Library to interface with Telegram! Create Telegram Bots in minutes.</br>Uses <a href="https://github.com/python-telegram-bot/python-telegram-bot">python-telegram-bot</a> as backend.</p>

---
## Xircuits Component Library for Telegram

This library enables Xircuits to integrate with Telegram, allowing seamless interaction with Telegram bots. It simplifies bot initialization, message handling, and various types of media sharing.


## Preview

https://github.com/user-attachments/assets/2bcef69d-e1c3-4735-80e9-946ab64ebd9f

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Telegram Bot Setup](#telegram-bot-setup)

## Prerequisites

Before you begin, you will need:

1. Python 3.9+
2. Xircuits
3. A Telegram Bot Token

## Installation

To use this component library, ensure you have an existing [Xircuits setup](https://xircuits.io/docs/main/Installation). You can then install this library using:

```bash
xircuits install telegram
```

Or manually:

```bash
# in base Xircuits directory
git clone https://github.com/XpressAI/xai-telegram xai_components/xai_telegram
pip install -r xai_components/xai_telegram/requirements.txt
```

## Telegram Bot Setup

### Creating a New Bot

1. Start a chat with [@BotFather](https://t.me/botfather) on Telegram
2. Use the `/newbot` command
3. Follow the prompts to:
   - Set a name for your bot
   - Choose a username (must end in 'bot')
4. BotFather will provide a token - save this securely

### Bot Token
- Keep this token secure - anyone with the token can control your bot
- export this token or create a .env file with TELEGRAM_BOT_KEY=YOUR_TOKEN.

### Important Notes
- Bot usernames must end in 'bot' (e.g., 'tetris_bot' or 'TetrisBot')
- Usernames are 5-32 characters long
- Only Latin characters, numbers, and underscores are allowed
- Username cannot be changed after creation

## Examples

### TelegramEchoBot
Simple bot that echoes back any message it receives - perfect for understanding the basic bot setup.

### TelegramMessageReplyBot
Demonstrates how to use Xircuits events to create custom message handling and responses.

### TelegramCommandBot
Shows how to implement command-based interactions (e.g., `/start`, `/help`) with argument parsing.

### TelegramReplyMedia
Showcases how to send various media types (images, PDFs, audio, video) in response to messages.

## Coming Soon (TBA)

- Enhanced group chat support (currently optimized for 1-1 chats)
- Media reception capabilities (currently supports sending media only)
- Other cool stuff

## Support & Community
Join our [Discord community](https://discord.gg/vgEg2ZtxCw) for support and discussions.
