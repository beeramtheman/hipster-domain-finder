var express = require('express')
var mongoose = require('mongoose');
var jade = require('jade');
var stylus = require('stylus');
var fs = require('fs');

var app = express();
app.set('views', __dirname + '/views');
app.set('view engine', 'jade');

app.use(stylus.middleware({
    src: __dirname + '/public',
    compile: function(str, path) {
        return stylus(str).set('filename', path);
    }
}));
app.use(express.static(__dirname + '/public'));

mongoose.connect('mongodb://localhost/hipsterdomainfinder');
var Domain = mongoose.model('Domain', {
    name: String, ext: String
});

var registrars = fs.readFileSync(__dirname + '/registrars.json', 'utf8');
var tlds = JSON.parse(fs.readFileSync(__dirname + '/tlds.json', 'utf8'));

app.get('/', function(req, res) {
    sendPage(res, 1);
});

app.get('/p', function(req, res) {
    res.redirect('/');
});

app.get('/p/:page', function(req, res) {
    if(req.query.d) {
        // send page with SmartRegistrar box pre-loaded (not JS)
    }
    else {
        sendPage(res, req.params.page);
    }
});

// Filter by TLD
app.get('/tld', function(req, res) {
    res.redirect('/');
});

app.get('/tld/:tld', function(req, res) {
    var tld = req.params.tld;
    sendPage(res, 1, {tld: tld}, '/tld/' + tld);
});

app.get('/tld/:tld/p/:page', function(req, res) {
    var tld = req.params.tld;
    sendPage(res, req.params.page, {tld: tld}, '/tld/' + tld);
});

function sendPage(res, page, query, paginationPrefix) {
    query = query || {};
    paginationPrefix = paginationPrefix || '';

    Domain.find(query).limit(60).skip((page - 1) * 60).sort('length').sort('name')
        .exec(function(err, domains) {
            if(err) domains = [{name: 'database error'}];
            res.render('index', {
                domains: domains,
                registrars: registrars,
                tlds: tlds,
                paginationPrefix: paginationPrefix,
                page: page
            });
        }
    );
}

app.listen(3001);
