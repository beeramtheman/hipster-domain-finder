# Hipster Domain Finder

### Hipster Domain Finder is no longer active!
### Anyone may fork this repo and host it themselves.

Find OG domain hacks with [Hipster Domain
Finder](http://www.hipsterdomainfinder.com).

[HN Discussion](https://news.ycombinator.com/item?id=7707100)


## Installation

#### Querying domains and building database

- Make sure you're running python2.7 (requirement of xmlrpclib)
- Run:
```
easy_install xmlrpclib
pip install pymongo
```

#### Web server

- Run: 
```
npm install
```

## Running

#### Querying domains and building database

- Obtain a corporate production API key from gandi (used during the XML RPC methods)
- Run:
```
python check.py --key=<API-key>
```

#### Web server

- Run:
```
node website/server.js
```
