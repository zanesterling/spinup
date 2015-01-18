GIFS = {
    rainbowFrog: 'http://zippy.gfycat.com/IndelibleIncomparableDinosaur.gif'
};

$(document).ready(function() {
    var frog = $('<img></img>');
    frog.attr('src', GIFS.rainbowFrog);
    frog.addClass('easter');
    frog.attr('id', 'frog');
    frog.css('position', 'fixed');
    frog.css('bottom', 0);
    $('body').append(frog);
});
