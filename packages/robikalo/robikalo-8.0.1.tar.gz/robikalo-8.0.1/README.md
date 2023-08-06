
## robikalo

> easy, fast and elegant library for making rubika self bots

``` python
from robikalo import Bot, Socket
from robikalo.filters import filters

bot = Bot("MyApp")
app = Socket(bot.auth)

@app.handler(filters.PV)
def hello(message):
    message.reply("Hello from Rubikalib!")
```

**robikalo** is an easy, fast and unofficial [rubika](https://rubika.ir) self bot library.
It enables you to easily interact with the main Telegram API through a user account (custom client) using Python.

### Key Features

- **Ready**: Install robikalo with pip and start building your applications right away.
- **Easy**: Makes the rubika API simple and intuitive, while still allowing advanced usages.
- **Elegant**: Low-level details are abstracted and re-presented in a more convenient way.
- **Fast**: Boosted up by aiohttp instead of requests.
- **Powerful**: Full access to Rubika's API to execute any official client action and more.

### Installing

``` bash
pip3 install robikalo
```

### Thanks For (A-Z)
- Dark Code
- Mr.binder
- Sajjad Dehghani
- Sajjad Soleymani
- Saleh (maven)
- Shayan Ghosi
- And you :)

