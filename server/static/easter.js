IMAGES = {
    mountainDew: 'http://www.caffeineinformer.com/wp-content/caffeine/mountain-dew.jpg',
    hitmarker: 'http://i.imgur.com/l9Im97W.jpg',
    illuminati: 'http://www.edmsauce.com/wp-content/uploads/2014/12/illuminati.jpg',
    gaben: 'http://www.bestgifever.com/data/images/2012/08/gaben.gif',
    doritos: 'http://www.fritolay.com/images/default-source/blue-bag-image/doritos-nacho-cheese.png?sfvrsn=2',
};

GIFS = {
    rainbowFrog: 'http://zippy.gfycat.com/IndelibleIncomparableDinosaur.gif',
    littleSnoop: 'http://puu.sh/3ObVc.gif',
    explosion: 'http://www.instructables.com/files/orig/FYT/IALR/FEMY342N/FYTIALRFEMY342N.gif'
};

AUDIO = {
    xFiles: '/static/x-files-airhorn.mp3',
    womboCombo: 'http://www.myinstants.com/media/sounds/wombo-combo.mp3',
    ohBabyTriple: 'http://soundboard.panictank.net/Oh%20Baby%20A%20Triple.mp3',
    hitmarker: '/static/HITMARKER.wav'
};

$(document).ready(function() {
    var clickSplosionCounter = 0;
    var buttonClicks = 0;
    var color = 'red';

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


    var RUNNING_MUSIC = false;
    function xFiles() {
        if (Math.random() < 0.8 || RUNNING_MUSIC) return;

        RUNNING_MUSIC = true;
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
        var triple = $('<audio></audio>');
        triple.attr('src', AUDIO.ohBabyTriple);
        triple.attr('type', 'audio.mpeg');
        triple.attr('id', 'wombo-combo');
        $('body').append(triple);

        var wombo = $('<audio></audio>');
        wombo.attr('src', AUDIO.womboCombo);
        wombo.attr('type', 'audio.mpeg');
        wombo.attr('id', 'wombo-combo');
        $('body').append(wombo);

        $('button').click(function() {
            buttonClicks++;
            if (buttonClicks % 3 == 0) {
                triple[0].play();
            }

            if (buttonClicks % 5 == 0) {
                wombo[0].play();
            }

            rotateDiv(this, 30 * buttonClicks);
            return false;
        });
    };

    function rotateDiv(div, deg) {
        $(div).css({'-webkit-transform': 'rotate('+deg+'deg)',
                    '-moz-transform': 'rotate('+deg+'deg)',
                    '-ms-transform': 'rotate('+deg+'deg)',
                    'transform': 'rotate('+deg+'deg)'});
        return $(div);
    }

    function dewNav() {
        var dew = $('<img></img>');
        dew.attr('src', IMAGES.mountainDew);
        dew.css('position', 'absolute');
        dew.css('top', 0);
        dew.css('left', 0);
        dew.css('width', '100');
        dew.css('height', '135%');
        $('body').append(dew);

        var dew = $('<img></img>');
        dew.attr('src', IMAGES.mountainDew);
        dew.css('position', 'absolute');
        dew.css('top', 0);
        dew.css('right', 0);
        dew.css('width', '100');
        dew.css('height', '135%');
        $('body').append(dew);

        var dew = $('<img></img>');
        dew.attr('src', IMAGES.mountainDew);
        dew.css('position', 'absolute');
        rotateDiv(dew, 90);
        dew.css('top', '-82%');
        dew.css('left', '45%');
        dew.css('width', '100');
        dew.css('height', '184%');
        $('body').append(dew);
    }

    function toggleBackground() {
        var green = 'rgb(0, 128, 0)';
        var red = 'rgb(255, 0, 0)';
        if ($('body').css('background-color') == red) {
            $('body').css('background-color', green);
        } else if ($('body').css('background-color') == green) {
            $('body').css('background-color', red);
        }
    }

    function hitmark(e) {
        var marker = $('<img></img>');
        marker.attr('src', IMAGES.hitmarker);
        marker.css('position', 'absolute');
        var xoffset = (Math.random() * 30) - 15;
        var yoffset = (Math.random() * 30) - 15;
        marker.css('left', e.clientX - 25 + xoffset);
        marker.css('top', e.clientY - 25 + yoffset);

        var sound = $('<audio></audio>');
        sound.attr('src', AUDIO.hitmarker);
        sound.attr('type', 'audio.wav');
        sound.attr('class', 'hitmark');

        $('body').append(marker);
        $('body').append(sound);

        marker.animate( {
            'opacity': 0
        },
            {
            done: function() {
                marker.remove();
                sound.remove();
            }
        }, 50)
        sound[0].play();

        $('body').trigger('startRumble');
        setTimeout(function() {
            $('body').trigger('stopRumble');
        }, 100);

        clickSplosionCounter++;
        if (clickSplosionCounter == 6) {
            clickSplosionCounter = 0;

            // splode sound
            var splode = $('<audio></audio>');
            splode.attr('src', '/static/explosion.mp3');
            splode.attr('type', 'audio/mpeg');
            $('body').append(splode);
            splode[0].play();

            // splode splode
            var boom = $('<img></img>');
            boom.attr('src', GIFS.explosion);
            boom.css('position', 'absolute');
            boom.css('left', e.clientX - 75);
            boom.css('top',  e.clientY - 75);
            $('body').append(boom);

            boom.animate({
                'opacity': 0
            }, 1000, function() {
                splode.remove();
                boom.trigger('stopRumble');
                boom.remove();
            });
        }
    }

    function skrillz() {
        if (RUNNING_MUSIC) return;
        RUNNING_MUSIC = true;

        var ytlink = $('<iframe width="854" height="510" src="//www.youtube.com/embed/WSeNSzJ2-Jw?autoplay=1" frameborder="0" allowfullscreen></iframe>');
        ytlink.addClass('easter');
        ytlink.css('display', 'none');


        $('body').append(ytlink);
    }

    function illuminati() {
        var illuminati = $('<img></img>');
        illuminati.attr('src', IMAGES.illuminati);
        illuminati.css('position', 'fixed');
        illuminati.css('width', '100%');
        illuminati.css('height', '100%');
        illuminati.css('top', '0');
        illuminati.css('left', '0');
        illuminati.css('z-index', '-99999');
        illuminati.css('opacity', 0);

        $('body').append(illuminati);

        illuminati.animate({
            'opacity': 0.1
        }, 120000);

    }

    function gabenIsWatching() {
        var gaben = $('<img></img>');
        gaben.attr('src', IMAGES.gaben);
        gaben.css('position', 'fixed');
        gaben.css('top', 110);
        gaben.css('right', 100);
        $('body').append(gaben);

        // gaben's holy shrine
        for (var i = 0; i < 6; i++) {
            var drts = $('<img></img>');
            drts.attr('src', IMAGES.doritos);
            drts.css('position', 'fixed');
            drts.css('top', 110 + i * 40);
            drts.css('right', 330);
            drts.css('width', 30);
            $('body').append(drts);
        }
        for (var i = 0; i < 6; i++) {
            var drts = $('<img></img>');
            drts.attr('src', IMAGES.doritos);
            drts.css('position', 'fixed');
            drts.css('top', 110 + i * 40);
            drts.css('right', 100);
            drts.css('width', 30);
            $('body').append(drts);
        }
        for (var i = 0; i < 7; i++) {
            var drts = $('<img></img>');
            rotateDiv(drts, 90);
            drts.attr('src', IMAGES.doritos);
            drts.css('position', 'fixed');
            drts.css('top', 100);
            drts.css('right', 95 + i * 40);
            drts.css('width', 30);
            $('body').append(drts);
        }
        for (var i = 0; i < 7; i++) {
            var drts = $('<img></img>');
            rotateDiv(drts, 90);
            drts.attr('src', IMAGES.doritos);
            drts.css('position', 'fixed');
            drts.css('top', 330);
            drts.css('right', 95 + i * 40);
            drts.css('width', 30);
            $('body').append(drts);
        }
    }

    function wow() {
        var wally = $('<iframe width="420" height="315" src="//www.youtube.com/embed/FzjtPtOH-Hg?autoplay=1" frameborder="0" allowfullscreen></iframe>');
        wally.css('position', 'absolute');
        wally.css('bottom', -1000);
        wally.css('left', '25%');

        wally.animate({
            'bottom': 200
        }, 5000, function() {

            wally.animate({
                'bottom': 6000,
            }, 4000);
        });
        $('body').append(wally);

    }

    dewNav();
    setTimeout(function() {
        frogSetup();
        frogYolo();
        setInterval(frogYolo, 5000);
    }, 5000);
    snoopCorners();
    yellowText();
    xFiles();
    buttonWombo();
    skrillz();
    illuminati();
    $('body').jrumble();
    $(document).click(hitmark);
    $('body').css('background', 'red');
    setInterval(toggleBackground, 1100);
    gabenIsWatching();
    wow();
});
