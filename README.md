Salt's parser.
Receives the commands sent by the server, parses them and sends them parsed to the server.

### Setup

Install all the required dependencies by running
```
$ pip install -r requirements.txt
```
at the root of the project.

The Analyzer can be launched by running
```
$ python main.py
```
However, please note that an instance of the database containing the command words must be running in the background for the Analyzer to function.

The Analyzer must be restarted everytime a new extension is installed.