# Kongou Desu!
This aim of this project is to create a full database of all ships (>1000T) which had taken part of WW2 and make it viable from a Telegram Bot.
In order to reach this achievement we decided to proced following 3 principal steps.

## First Step: Gathering Data (We are currently working on this step)
In order to gather data, we decided to write some small pieces of Javascript code able to scrape information from Wikipedia.
A first js was written to get from the alphabetical naval list of ships of WW2 the main information and ship's main page link reference, a secret tool that will help us later.
The second js simply takes from each ship main page, the main WikiTable which contains specifics detailed data of the ship.
All this data would be temporarily stored in json files.

## Second Step: Create a DB
TODO

## Third Step: Make the data reachable to users
We created a simply Python Telegram Bot
