# SportsbookScraper
Sportsbook Scraper to find +EV and arbitrage betting opportunities

Uses Python packages selenium and Beautiful Soup

headlessDriver function uses features of selenium to safely navigate to a Sportsbooks site without getting blocked
getMatchups uses the headlessDriver to retrieve all source code and parse through the source code for sports matchups
getPP uses the headlessDriver to retrieve the source code of all sports matchups and parses through it for each player prop and odd

The player names, player props, and odds are then written into an alternate text file in a prettified form.
