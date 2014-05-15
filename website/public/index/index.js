var registrars = JSON.parse(document.getElementById('registrars').innerHTML);

function viewDomain() {
    var domain = this.href.split('#')[1];
    var tld = domain.split('.')[1];

    $('.info .domain').text(domain);
    randomTweet();

    for(reg in registrars) {
        if(registrars[reg].tlds.indexOf(tld) > -1) {
            var link = registrars[reg].link.replace('{{d}}', domain);
            $('.reg.' + reg).addClass('true');
            $('.reg.' + reg).attr('href', link);
            $('.reg.' + reg).attr('target', '_blank');
        }
        else {
            $('.reg.' + reg).removeClass('true');
            $('.reg.' + reg).attr('href', 'javascript:void(0)');
            $('.reg.' + reg).attr('target', '_self');
        }
    }

    $('.info').css({display: 'block'});
    $('.info-bg').css({display: 'block'});

    setTimeout(function() {
        $('.info').css({opacity: 1});
        $('.info-bg').css({opacity: 0.3});
    }, 0);
}

$('.row a').each(function() {
    this.href = this.href.replace('?d=', '#');
    this.onclick = viewDomain;
});

$('.info-bg').click(function() {
    $('.info').css({display: 'none'});
    $('.info-bg').css({display: 'none'});
    setTimeout(function() {
        $('.info').css({opacity: 0});
        $('.info-bg').css({opacity: 0});
    }, 0);
});

var tweetNum = 0;
function randomTweet() {
    var domain = $('.info .title').text();
    var tweets = [
        'Considering buying {{d}}.',
        "Can't believe {{d}} isn't taken yet.",
        'Domain of the year -> {{d}}.',
        'Buying {{d}} for... things.',
        'Best domain ever purchased: {{d}}.',
    ];
    tweetNum++;
    if(tweetNum >= tweets.length) tweetNum = 0;
    $('.info .tweet .text').val(tweets[tweetNum].replace('{{d}}', domain));
}

$('.new-tweet').click(function() {
    randomTweet();
});
