# nus-temperature-declaration

A quick little python script I wrote this morning to help with my temperature declaration at NUS.

![Screenshot of using the temperature script](./screenshot.png)

## Usage

The python package `beautifulsoup4` needs to be installed beforehand; you can install it using `pip3 install beautifulsoup4`.

To declare your temperature, run `python3 temperature.py <temperature>`.

To check your temperature, run `python3 temperature.py -c`.

## Setup (optional)

If you don't want to enter your username and password every time, you can store it in a text file.

Copy `config-example.txt` to `config.txt`, replacing the username and password fields accordingly.

Note: with a few additional steps, this can be modified to automate the temperature declaration process entirely using cron jobs. Please don't do that! It kind of defeats the purpose of temperature declarations in the first place.
