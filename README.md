Salt's parser.
Receives the commands sent by the server, parses them and sends them parsed to the server.

### Setup

Install all the required dependencies by running
```
$ pip install -r requirements.txt
```
at the root of the project.

NLTK requires a tokenizer to function.
A tokenizer can be downloaded from the python interpreter.
Launch the python interpreter (usually, by typing python or python3 in the command prompt / the shell).
Once you invoked the interpreter, type:
```
$ import nltk
$ nltk.download('punkt')
```


Now the Analyzer can finally be launched by running the main.py script.
```
$ python main.py
```
However, please note that an instance of the database containing the command words must be running in the background for the Analyzer to function.

The Analyzer must be restarted everytime a new extension is installed.
