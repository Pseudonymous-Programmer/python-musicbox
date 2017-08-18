$(document).ready(function() {

var current_playing = "";
var current_audio = undefined;

function choose(l) {
  return l[Math.floor(l.length*Math.random())]
}

function choose_random_song() {
  var keys = [];
  for(key in songs) if(songs.hasOwnProperty(key)) keys.push(key);
  var category = choose(keys);
  var song = choose(songs[category]);
  return category + '/' + song;
}

var on_end_callback = function() {};

var update_current_playing = function() {
  var val = $("#input").val();
  if(val == '') {
    current_playing = choose_random_song();
    on_end_callback = function () {
      current_playing = choose_random_song();
      start_music(current_playing);
    };
  } else if(/^([^/]+)$/.exec(val)) {
    var songs_in_cat = songs[val];
    current_playing = val + '/' + choose(songs_in_cat);
    on_end_callback = function() {
      current_playing = val + '/' + choose(songs_in_cat);
      start_music(current_playing);
    };
  } else current_playing = $('#input').val();
}



function start_music(path) {
  var matches = /(.+)\/(.+)/.exec(path);
  $('#banner').text("Now playing: " + matches[2] + " from " + matches[1]);
  current_audio = new Audio("music/" + path + ".wav");
  current_audio.play();
  current_audio.onended = function() {
    current_audio = undefined;
    $('#banner').text("Done playing: " + matches[2] + " from " + matches[1])
    on_end_callback();
  };
}

$('#play').click(function () {
  if(current_audio) {
    current_audio.onended = function () {};
    current_audio.currentTime = current_audio.duration || 0;
  }
  update_current_playing();
  start_music(current_playing);
});

$('#pause').click(function () {
  if(!current_audio.paused) current_audio.pause();
  else current_audio.play();
});

$('#loop').click(function () {
  current_audio.loop = !current_audio.loop;
});

$('#skip').click(function () {
  current_audio.pause();
  current_audio = undefined;
  on_end_callback();
});

});
