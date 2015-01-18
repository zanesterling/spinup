GIFS = {
    rainbowFrog: 'http://zippy.gfycat.com/IndelibleIncomparableDinosaur.gif',
    littleSnoop: 'http://puu.sh/3ObVc.gif',
    explosion: 'http://www.instructables.com/files/orig/FYT/IALR/FEMY342N/FYTIALRFEMY342N.gif'
};

AUDIO = {
    xFiles: '/static/x-files-airhorn.mp3',
    womboCombo: 'http://www.myinstants.com/media/sounds/wombo-combo.mp3',
};

$(document).ready(function() {
    var frogSetup = function() {
        var frog = $('<img></img>');
        frog.attr('src', GIFS.rainbowFrog);
        frog.addClass('frog');
        frog.addClass('easter');
        frog.attr('id', 'frog');
        frog.css('position', 'fixed');
        frog.css('bottom', -300);
        frog.css('opacity', 1);
        $('body').append(frog);

        frog = $('<img></img>');
        frog.attr('src', GIFS.rainbowFrog);
        frog.addClass('frog');
        frog.addClass('easter');
        frog.attr('id', 'frog');
        frog.css('position', 'fixed');
        frog.css('bottom', -300);
        frog.css('right', 0);
        frog.css('opacity', 1);
        $('body').append(frog);

        frog = $('<img></img>');
        frog.attr('src', GIFS.rainbowFrog);
        frog.addClass('frog');
        frog.addClass('easter');
        frog.attr('id', 'frog');
        frog.css('position', 'fixed');
        frog.css('top', -300);
        frog.css('opacity', 1);
        $('body').append(frog);

        frog = $('<img></img>');
        frog.attr('src', GIFS.rainbowFrog);
        frog.addClass('frog');
        frog.addClass('easter');
        frog.attr('id', 'frog');
        frog.css('position', 'fixed');
        frog.css('bottom', 300);
        frog.css('right', 0);
        frog.css('opacity', 1);
        $('body').append(frog);
    };

    var frogYolo = function() {
        var frogs = $('.frog');

        $(frogs[0]).css('opacity', 1);
        $(frogs[0]).animate({
            'opacity': 0,
            'bottom': '+=300',
            'width': '100%'
        }, 2000, function() {
            this.style.bottom = 0;
            this.style.width = 300;
        });

        $(frogs[1]).css('opacity', 1);
        $(frogs[1]).animate({
            'opacity': 0,
            'bottom': '+=300',
            'width': '100%'
        }, 2000, function() {
            this.style.bottom = 0;
            this.style.right = 0;
            this.style.width = 300;
        });

        $(frogs[2]).css('opacity', 1);
        $(frogs[2]).animate({
            'opacity': 0,
            'top': '+=300',
            'width': '100%'
        }, 2000, function() {
            this.style.top = 0;
            this.style.width = 300;
        });

        $(frogs[3]).css('opacity', 1);
        $(frogs[3]).animate({
            'opacity': 0,
            'bottom': '-=300',
            'width': '100%'
        }, 2000, function() {
            this.style.top = 0;
            this.style.right = 0;
            this.style.width = 300;
        });
    }

    function snoopCorners() {
        var snoop = $('<img></img>');
        snoop.attr('src', GIFS.littleSnoop);
        snoop.addClass('easter');
        snoop.css('position', 'fixed');
        snoop.css('bottom', 0);
        $('body').append(snoop);
        setInterval(shakeFunc(snoop), 1000);

        var boom = $('<img></img>');
        boom.attr('src', GIFS.explosion);
        boom.addClass('easter');
        boom.css('position', 'fixed')
        boom.css('bottom', 70);
        boom.css('left', 0);
        boom.width(70);
        boom.height(80);
        $('body').append(boom);
        setInterval(shakeFunc(boom), 1000);

        snoop = $('<img></img>');
        snoop.attr('src', GIFS.littleSnoop);
        snoop.addClass('easter');
        snoop.css('position', 'fixed');
        snoop.css('bottom', 0);
        snoop.css('right', 0);
        $('body').append(snoop);
        setInterval(shakeFunc(snoop), 1000);

        boom = $('<img></img>');
        boom.attr('src', GIFS.explosion);
        boom.addClass('easter');
        boom.css('position', 'fixed')
        boom.css('bottom', 70);
        boom.css('right', -10);
        boom.width(70);
        boom.height(80);
        $('body').append(boom);
        setInterval(shakeFunc(boom), 1000);
    };

    function yellowText() {
        $('p,h3,button').each(function(index, elem) {
            if (Math.random() > 0.4)
                $(elem).css('color', 'yellow')
                    .css('background', 'black');
            if (Math.random() > 0.7)
                $(elem).text('sample text');
        });
    };

    function xFiles() {
        if (Math.random() < 0.8) return;

        var clip = $('<audio></audio>');
        clip.attr('src', AUDIO.xFiles);
        clip.attr('type', 'audio/mpeg');
        clip.attr('autoplay', true)
        clip.text('no support, sorry!');
        $('body').append(clip);
    };

    function shakeFunc(elem) {
        return function() {
            elem.effect("shake");
        }
    };

    function buttonWombo() {
        $('button').each(function(index, elem) {
            $(elem).find('a')
                .attr('href', '');
            //console.log(elem);
        });
    };

    frogSetup();
    frogYolo();
    setInterval(frogYolo, 5000);
    snoopCorners();
    yellowText();
    xFiles();
    buttonWombo();
});
