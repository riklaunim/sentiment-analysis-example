This example code uses `textblob` to do sentiment analysis on TripAdvisor reviews - assigning a numerical value of
polarity (negative - positive) and subjectivity - from fact to opinions.

Viewing example results
-----------------------
Results for three hotels are in the `results` folder.

Running examples
----------------
Create a virtualenv and install the dependencies:
```angular2
pip install -r requirements.txt
python setup.py test  # tests should pass
```
You can execute the `run.py` file to regenerate the data. If you want to use it for your own data then you will
either have to provide a json file in expected format or alter data structures in this example. Supported JSON looks
like so:

```angular2
{"data": [
   {
      "id":"some id",
      "attributes":{
         "text":"text here",
         "rating": rating here
      }
   },
   ...
]}

```



Testing
-------
Tests are in the `tests` folder and run via pytest:

```angular2
python setup.py test
```
