# Math assistant

### Description

This is a telegram bot that solves math problems. You can send either a text or a picture with a problem.

All the images will be at first translated to `LaTeX` format. The interpreted version/initial text version is then sent to a classifier.

In case this type of problem can be solved by `Wolfram`, Wolfram Alpha's API is used. The bot sends pictures with a step-byt step solution if possible, the answer otherwise.

All the problems that can't be solved my Wolfram are sent to `GPT-4` and it solves(at least tries) them.

### How to use

First of all, you have to create a folder `env` with the following files with the corresponding variables:
* bot.env (standard telegram api credentials): \
    `BOT_NAME` \
    `TOKEN` \
    `API_ID` \
    `API_HASH`
* mathpix.env (obtained on mathpix.com): \
    `MATHPIX_APP_ID` \
    `MATHPIX_APP_KEY`
* openai.env (standard openai credentials): \
    `OPENAI_API_KEY`
* wolfram.env (wolfram alpha credentials, use the version for step-by step solutions): \
    `WOLFRAM_APP_ID`

To actually run the bot execute the following command:

```bash
docker compose -f docker-compose-dev.yml up -d
```
