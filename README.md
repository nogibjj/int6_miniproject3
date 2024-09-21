# int6_miniproject2
[![CI](https://github.com/nogibjj/int6_miniproject2/actions/workflows/ci.yml/badge.svg)](https://github.com/nogibjj/int6_miniproject2/actions/workflows/ci.yml)

This repo contains work for mini-project 2. It sets up an environment on codespaces and uses Github Actions to run a Makefile for the following: `make install`, `make test`, `make format`, `make lint`. It loads in a dataset (from Kaggle) that contains information on Spotify sound tracks and performs some basic exploratory data analysis.

Some important components:

* `Makefile`

* `Dockerfile`

* A base set of libraries for devops and web

* `githubactions` 

## Purpose of project
The purpose of this project is to practice using our previous mini-project 1 as a workflow template for data analysis. The file main.py contains four main functions: 
* `read_data()`: reads in our data as a pandas dataframe
* `calc_stats(df)`: calculates summary statistics including mean, meadian, and standard deviation
* `create_viz(df)`: creates sample plots using the data
* `create_report(csv)`: generates a pdf report of the data including basic summary stats and plots

These functions are tested in test_main.py. To make sure github actions is working properly, I use a Makefile to test various parts of my code.

## Preparation
1. Open codespaces 
2. Wait for container to be built and virtual environment to be activated with requirements.txt installed 

## Check format and test errors 
1. Format code `make format`
2. Lint code `make lint`
3. Test code `make test`

<img width="600" alt="passing test cases image" src=resources/pass_test.png>


## Outputs
Summary statistics and data visualizations can be displayed by running `python test_main.py` calling `calc_stats(df)`

<img width="600" alt="showing summary stats image" src=resources/working_stats.png>


Data visualizations are saved to a `resources` folder by running `python test_main.py` calling `create_viz(df)`

<img width="600" alt="showing plots image" src=resources/working_plots.png>


PDF report is created by running `python test_main.py` calling `create_report(csv)`

<img width="600" alt="showing report image" src=resources/working_report.png>
