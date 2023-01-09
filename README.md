# notion-lottery-slack-bot
> A Slack bot to randomly pick a page from Notion Database.

## Steps
1. Get a Notion Database to pick pages randomly from.
2. Get a Slack bot for users to call to pick random pages from Notion.
3. Put following values as environment variables.
   - [Notion Database's id](https://stackoverflow.com/a/69860478/19524198), 
   - [Notion Token](https://www.notion.so/help/create-integrations-with-the-notion-api), 
   - [Slack Token](https://api.slack.com/apps)
4. Customize Notion pages' properties and messages.
5. To start server
```shell
pip install -r requirements.txt
uvicorn main:app
```