# Telegram bot to control expenses

This is simple telegram bot application which allows you to write your
daily expenses and then to get statatistic about them.

The bot has two simple functions: collect expenses data and provide statistic
report in desired period.

## Expenses data collection

Right after start of the bot you can initiate chat with it with /start command.
Bot will propose to add expense. When you add expense your chast need to provide
info about cost and description of expense. That's it.

## Statistic information

With command /statistic you can ask the bot to provide information about 
your expenses in desired period. Just type month, month and year, date or
period with date from and date to to get statistic information and then type
of report: expenses list or expenses grouped by categories. List of categories
bot uses: transport, food, health, education, communal payments, leisure,
clothes, home, other.

**IMPORTANT** The bot uses chat gpt for categorization. Every day it's 
determinate category for each expenses provided by bot users if expense
is not related to any category. To have this feature enabled it's needed
to specify open AI API key in .env file and time of each day categorization task
as described below.

## Installation

If you would like to start your own instance of the bot you can use this 
short manual.

### Prerequisites

It's requered to have postgresql database for data collection

### Enviroment variables

First you will need to create .env file in the root of project folder and
place enviroments' variable:

    POSTGRES_DB=<database name>
    POSTGRES_USER=<database user>
    POSTGRES_PASSWORD=<database password>
    DB_HOST=<database host>
    DB_PORT=<database port>
    API_TOKEN=<Token to your telegram bot>
    DB_ECHO=<Key to echo sql requests>
    TIMEZONE=<timezone>
    OPEN_AI_KEY=<Open AI key>
    CATEGORIZATION_TIME=<time of categorization task>

OPEN_AI_KEY and CATEGORIZATION_TIME are not necessary enviroments' variables
but they are needed if you want bot to categorize your expenses one time in 
a day.

### Run in production

You can start the bot with docker command after creation of .env file

    docker-compose up --build -d


### Run in development

Before you start the bot you need to install python packages in your enviroment:

    pip install -r requirements.txt

Then apply database migrations

    alembic upgrade head

Install fixtures

    python manage.py loaddataall

And then run main.py file

    python main.py

That's it
