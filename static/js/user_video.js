

var videoElements = document.querySelectorAll('.video-js');

videoElements.forEach(function(videoElem) {
    var player = videojs(videoElem);
    player.on('contextmenu', function(e) {
        e.preventDefault();
    });
});
