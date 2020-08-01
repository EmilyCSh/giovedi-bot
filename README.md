# È Giovedì Bot

È Giovedì Bot è un bot in Telegram la cui funzione è informare l'utente, previa domanda e aggiornando un canale dedicato a cadenza quotidiana, se la data odierna corrisponde a giovedì. Ad ogni data interrogazione del bot, l'output dello stesso corrisponderà a "Sì" nel caso in cui la data al momento sia veramente giovedì, "No" in caso contrario.

## Perché?

L'idea di creare questo bot è nata da un meme diffusosi nella community Telegram italiana che consiste nel trovare vari modi per far leggere a quante più persone possibile la frase "è giovedì", sia esso creando gif con questa frase in sovraimpressione oppure in modi più creativi.

## Utilizzo

Il bot è stato scritto in Python 3 utilizzando la libreria [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot). Le seguenti dipendenze sono necessarie per l'esecuzione del bot:

```bash
pip install python-telegram-bot
pip install python-dotenv
```

Se non si volesse eseguire `pip` sul proprio sistema, è sempre possibile installare tali dipendenze dalle repository della propria distro Linux, o utilizzando [pipenv](https://github.com/pypa/pipenv).

È inoltre necessario che nella root del progetto sia presente un file chiamato `secret.env` contenente il TOKEN del bot che si intende utilizzare nonché il nome del canale target rispettando questo formato:

```env
TG_TOKEN = {token rilasciata da Botfather}
CHANNEL = @channelid
```

## Utilizzo con Docker

Se si preferisce usare Docker per il deployment del bot, è possibile creare un container partendo dal `Dockerfile` presente nella repo.

```bash
git clone https://gitlab.com/chic_luke/giovedi-bot
cd giovedi-bot
docker build -t chic_luke/giovedibot:alpha .
docker run --rm [ID]
```

## Utilizzo con pipenv

Per eseguire il bot con `pipenv`:

```bash
pipenv install
pipenv run pip install -r requirements.txt
pipenv run python main.py
```