#### The `serverside` directory is just copied from the original repo for local testing.

#### The `temp` directory consists of small notes helping the development process.

#### The `bot` directory is the main folder for my project.
* In `game.py` is the "main" code which organizes the flow of the game | ⚠**only this file should be run**⚠
* In `connection.py` is the code handling the underlying communication with the server
* In `logic.py` is the important stuff, i.e. code for keeping track of the game and deciding how to act accordingly

#### Other important files are:
* `auth.csv`, here are the player credentials stored. If you want a new persona, simply add a row with the data, the program picks the lowest
* `splashes.txt`, when sending a chat message, the program picks one random line from this file. If empty or missing, placeholder message is sent
* `setup.py`, running this will create the `auth.csv` file template and an empty `splashes.txt` file

## How to get started?
1. run `setup.py`
2. edit `auth.csv` and create a new row with your credentials
3. edit `splashes.txt` if you want
4. edit `game.py` and change the `host` and `port` parameters in the main call at the bottom of the file
5. run `game.py`

If you don't want messages to be broadcasted, you can edit `game.py` and change the `chat=True` parameter in the main call at the bottom of the file.

Every gametick, the program decides randomly if a message is broadcasted. You can control the probability by editing `game.py` and changing the `chatProb` parameter in the main call at the bottom of the file, it has to be a float between 0 and 1 and is 0.1 by default, meaning around every 10 gameticks a message is sent.


## Documentation
https://github.com/freehuntx/gpn-tron/blob/master/PROTOCOL.md
