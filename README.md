# Python Discord HelperBot
## How to set up

Edit [config.json](config.json).

Here is an explanation of what everything is:

| Variable                  | What it is                                                            |
| ------------------------- | ----------------------------------------------------------------------|
| YOUR_BOT_PREFIX_HERE      | The prefix you want to use for normal commands                        |
| YOUR_BOT_TOKEN_HERE       | The token of your bot                                                 |
| YOUR_BOT_PERMISSIONS_HERE | The permissions integer your bot needs when it gets invited           |
| YOUR_APPLICATION_ID_HERE  | The application ID of your bot                                        |
| OWNERS                    | The user ID of all the bot owners                                     |

In the [blacklist.json](blacklist.json) file you now can add IDs in the list.

## How to start

Before running the bot you will need to install all the requirements:

```bash
pip install -r requirements.txt
python bot.py
```
