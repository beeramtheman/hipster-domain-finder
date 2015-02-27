# Hipster Domain Finder 2.0

![screenshot][screenshot]

## What

Find short & sweet single word domain hacks with Hipster Domain Finder at
[HipsterDomainFinder.com][hdf]. All domains listed should be available for
registration.

## Development

### General ###

Requirements for HDF are Python 3 and MongoDB. Python modules that must be
installed are:

- requests
- pymongo
- bottle

HDF is ready to be used locally out of the box. Just run
[populate_db.py][populate_db] to populate the database with 100 domain hacks.
Note this is for testing purposes only and the domains will be marked as
available without any verification. In production use [update.py][update] as
described below.

### Domains

[update.py][update] calculates all possible domain hacks from words in
[words.txt][words] and inserts/updates their availability with [Domainr's
API][domainr] (API key must be set in [config.ini][config]). HDF's official
website runs [update.py][update] with Cron every 24 hours.

[words.txt][words] is supposedly the 50,000 most common english words on the
internet, though I can't remember where I got it. Adding/changing words is as
simple as changing [words.txt][words].

### Website ###

HDF's official website is intentionally very simple inside and out.
[website.py][website] handles routing and serving dynamic/static content. HTML
is in [views][views] and CSS is in [static][static]. Colour scheme is based on
[praxicalidocious][praxicalidocious]'s [Winter Wolves palette][palette].

[hdf]: http://www.hipsterdomainfinder.com
[screenshot]: screenshot.png
[domainr]: https://github.com/domainr/api
[populate_db]: populate_db.py
[update]: update.py
[words]: words.txt
[config]: config.ini
[website]: website.py
[views]: views
[static]: static
[praxicalidocious]: http://www.colourlovers.com/lover/praxicalidocious
[palette]: http://www.colourlovers.com/palette/3636384/Winter_Wolves
