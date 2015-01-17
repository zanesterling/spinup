$(document).ready(function(){
    var kv_displays = $('.key-value-display');
    for (var i = 0; i < kv_displays.length; i++) {
        // make display full width
        var display = kv_displays[i];

        // fit canvas sexily
        var svg = $(display).find('svg')[0];
        svg.style.marginLeft =  'auto';
        svg.style.marginRight = 'auto';
    }
});
