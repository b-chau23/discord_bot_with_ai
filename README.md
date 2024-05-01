# Discord bot that interacts with AI models
Uses OpenAI and Antrhopic APIs to communicate with users through Discord
## Overview
- Commands allow users to interact with AI models like ChatGPT-4 and Claude-3
- Discord bot replies to command with the output from corresponding model
- Output from models are also written into corresponding text files
- Output that is too long for a Discord message (2000+ characters) are written to a text file and sent to the user
- Image models are able to be used

## Issues
- Sometimes unable to parse text that contains quotation marks (unsure why nor which ones, have not looked into it)
- Previous context is not saved, so conversations are not possible (it would also become very expensive in terms of $)
