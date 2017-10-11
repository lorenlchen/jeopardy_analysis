# Using Linear Regression to Analyze Jeopardy Game Data

This repository contains code to scrape data from [j-archive](http://www.j-archive.com), clean it, then run a simple linear regression to predict scores using statistics including how often each contestant buzzed in and how often each contestant was correct.

## Requirements

* `scrapy` for running the scraper. Scrapy can be installed via the terminal by running `$ pip install scrapy`. Once initialized, place the scraping file inside of the appropriate folder and run `scrapy crawl jeop_scraper -o jeop_data.json`. This will yield a json file with fields for Season, Game ID, Date, Player Name, Player ID, # Right, # Wrong, # of Daily Doubles, Double Jeopardy Score, [Coryat Score](http://www.j-archive.com/help.php#coryatscore) and Final Score.

* Python 3 for running the analysis. Pandas is used for the dataframe and Scikit-Learn and StatsModels are used for the regression. Matplotlib is used for plotting.

## Scraping

Initialize scrapy by running, `$ scrapy startproject jeopardy`. Once initialized, place the [spider](jeop_scraper.py) inside of the appropriate folder and run `scrapy crawl jeop_scraper -o jeop_data.json`. This will yield a json file with fields for Season, Game ID, Date, Player Name, Player ID, # Right, # Wrong, # of Daily Doubles, Double Jeopardy Score, Coryat Score and Final Score.

## Analysis

From the yielded columns, for each player, we calculated values for total number of buzzes, correct response percentage, their percentile ranks and proportions, and a number of other factors including game rank, appearance number, etc. We ran a regression on Double Jeopardy Score against normalized values for buzzing proportion, Daily Doubles uncovered and both of their interactions with Accuracy. These covariates were chosen after testing several different models using a train-test-split of 70-30. The resulting model had a train and test R^2 value of about 76% with all included coefficients highly significant. Plots of the resulting predictions can be seen in the included Jupyter Notebook.

## Reservations

For high predicted values (above $30,000 Double Jeopardy Score), the model systematically underpredicts the actual data. This effects about 0.5% of the data (31 observations out of the 7758 total). Other terms could possibly be included to more accurately predict these data.

## Extensions

Double Jeopardy Score is often used as a proxy for player ability since it incorporates some amount of strategy, unlike Coryat Score, which ignores all wagers, but eliminates the situational noise from Final Jeopardy Wagers. A natural extension of this model would be to use our Predicted Double Jeopardy Score in a logistic regression that predicts Win Probability. This could then be passed into a Geometric Distribution to predict the length of a win streak using statistics from previous games.

## Acknowledgements

We are particularly indebted to Andy Saunders for creating and maintaining the archive of data at [j-archive](http://www.j-archive.com), from which all of the data used was sourced.
