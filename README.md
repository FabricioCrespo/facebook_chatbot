# demo-bot

Simple chatbot written in Python 3.7.

## Local Dev Setup

1. Install requirements.txt by running `pip install -r requirements.txt`
2. Install Spacy models:

- English
  ```
  python3 -m spacy download en_core_web_md
  python3 -m spacy link en_core_web_md en
  ```

- Spanish:
  `python -m spacy download es_core_news_md`
  `python3 -m spacy link es_core_news_md es`

- To start the bot, run:
```
rasa run -m models --enable-api --cors "*" --debug & rasa run actions

```
- To run with credentials to make test on Facebook:
```
rasa run -m models --enable-api --cors "*" --debug --credentials credentials.yml & rasa run actions
```
To train the bot, run:
`rasa train`

This starts the server at http://localhost:5005

If you are deploying the bot to another platform (such as Facebook messenger), add `--credentials credentials.yml` after `--debug` and fill in the necessary credentials.

curl --request POST \
  --url http://localhost:5005/webhooks/rest/webhook \
  --header 'content-type: application/json' \
  --data '{"sender": "sender_id", "message": "hi"}'