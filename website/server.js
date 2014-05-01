var express = require('express')
var mongoose = require('mongoose');
var jade = require('jade');
var stylus = require('stylus');

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

app.get('/', function(req, res) {
    sendPage(res, 1);
});

app.get('/p', function(req, res) {
    res.redirect('/');
});

app.get('/p/:page', function(req, res) {
    sendPage(res, req.params.page);
});

function sendPage(res, page) {
    Domain.find().limit(60).skip((page - 1) * 60).sort('length').sort('name')
        .exec(function(err, domains) {
            if(err) domains = [{name: 'databse error'}];
            res.render('index', {
                domains: domains,
                page: page
            });
        }
    );
}

app.get('/box', function(req, res) {
    res.render('box', {});
});

app.listen(1337);
