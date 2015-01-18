GIFS = {
    rainbowFrog: 'http://zippy.gfycat.com/IndelibleIncomparableDinosaur.gif',
    littleSnoop: 'http://puu.sh/3ObVc.gif',
    explosion: 'http://www.instructables.com/files/orig/FYT/IALR/FEMY342N/FYTIALRFEMY342N.gif'
};

$(document).ready(function() {
    var frogYolo = function() {
        var frog = $('<img></img>');
        frog.attr('src', GIFS.rainbowFrog);
        frog.addClass('easter');
        frog.attr('id', 'frog');
        frog.css('position', 'fixed');
        frog.css('bottom', -300);
        frog.css('opacity', 1);
        $('body').append(frog);

        frog.animate({
            'opacity': 0,
            'bottom': '+=300',
            'width': '100%'
        }, 1000);

        frog = $('<img></img>');
        frog.attr('src', GIFS.rainbowFrog);
        frog.addClass('easter');
        frog.attr('id', 'frog');
        frog.css('position', 'fixed');
        frog.css('bottom', -300);
        frog.css('right', 0);
        frog.css('opacity', 1);
        $('body').append(frog);

        frog.animate({
            'opacity': 0,
            'bottom': '+=300',
            'width': '100%'
        }, 2000);

        frog = $('<img></img>');
        frog.attr('src', GIFS.rainbowFrog);
        frog.addClass('easter');
        frog.attr('id', 'frog');
        frog.css('position', 'fixed');
        frog.css('top', -300);
        frog.css('opacity', 1);
        $('body').append(frog);

        frog.animate({
            'opacity': 0,
            'top': '+=300',
            'width': '100%'
        }, 2000);

        frog = $('<img></img>');
        frog.attr('src', GIFS.rainbowFrog);
        frog.addClass('easter');
        frog.attr('id', 'frog');
        frog.css('position', 'fixed');
        frog.css('bottom', 300);
        frog.css('right', 0);
        frog.css('opacity', 1);
        $('body').append(frog);

        frog.animate({
            'opacity': 0,
            'bottom': '-=300',
            'width': '100%'
        }, 2000);
    }

    function snoopCorners() {
        var snoop = $('<img></img>');
        snoop.attr('src', GIFS.littleSnoop);
        snoop.addClass('easter');
        snoop.css('position', 'fixed');
        snoop.css('bottom', 0);
        $('body').append(snoop);

        var boom = $('<img></img>');
        boom.attr('src', GIFS.explosion);
        boom.addClass('easter');
        boom.css('position', 'fixed')
        boom.css('bottom', 70);
        boom.css('left', 0);
        boom.width(70);
        boom.height(80);
        $('body').append(boom);

        snoop = $('<img></img>');
        snoop.attr('src', GIFS.littleSnoop);
        snoop.addClass('easter');
        snoop.css('position', 'fixed');
        snoop.css('bottom', 0);
        snoop.css('right', 0);
        $('body').append(snoop);

        boom = $('<img></img>');
        boom.attr('src', GIFS.explosion);
        boom.addClass('easter');
        boom.css('position', 'fixed')
        boom.css('bottom', 70);
        boom.css('right', -10);
        boom.width(70);
        boom.height(80);
        $('body').append(boom);
    };

    function yellowText() {
        $('p').each(function(index, elem) {
            $(elem).css('color', 'yellow')
                .css('background', 'black');
        });
    };

    setInterval(frogYolo, 5000);
    frogYolo();
    snoopCorners();
    yellowText();
});

