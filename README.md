# iq

iq can be used to parse ISC game data and save in Quackle gcg format.

### Usage

Requires Python3 and Chrome browser. This should work in other browsers that have dev tools.

- Open Chrome developer tools (Cmd-Option-I)
- Go to Network tab, then WS (websockets)
- Now log in to https://isc.ro
- You should see a `MAINSERVER` request in dev tools, click it
- Load a game you wish to export `examine history avruga 0`
- In the Data pane you find the request `EXAMINE HISTORY...`, right click and Copy
- Save the copied data to a file

### Running from command line

`python3 iq.py <inputfile> > <outputfile>`

