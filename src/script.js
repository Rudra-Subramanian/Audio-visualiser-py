
let full_svg = window.songframes;
let audioplayer = window.myAudio;
const leftext = window.abovetext;
const righttext = window.belowtext;
console.log(audioplayer);
audioplayer.volume = 0.2;
var svgDoc = null;
let button = document.getElementById("framenumber")
var upper_initial_frame = '#ustartframe';
var lower_initial_frame = '#dstartframe';
var current_frame =4020;
var max_frame = 3028;
var min_frame = 0;


document.addEventListener("DOMContentLoaded", () => {
  console.log("DOM fully loaded and parsed");
  // --- Audio Player Controls ---
  const playPauseBtn = document.getElementById('playpause-btn');
  const seekbar = document.getElementById('seekbar');
  const audio = audioplayer;
  seekbar.max = audio.duration;
  seekbar.min = 0;

setInterval(() => {
    
}, 500)

seekbar.addEventListener('input', () => {
    audio.currentTime = seekbar.value;
})

  // Play/Pause button
  playPauseBtn.addEventListener('click', () => {
    if (audio.paused) {
      audio.play();
    } else {
      audio.pause();
    }
  });

  // Update button text on play/pause
  audio.addEventListener('play', () => {
    playPauseBtn.textContent = '\u23F8';
    seekbar.toggleAttribute('disabled');

  });
  audio.addEventListener('pause', () => {
    playPauseBtn.textContent = '\u23F5';
    seekbar.toggleAttribute('disabled');
  });

  // Seekbar interaction


  // Update seekbar as audio plays
  //audio.addEventListener('timeupdate', updateSeekbar);
  //audio.addEventListener('durationchange', updateSeekbar);
  //audio.addEventListener('loadedmetadata', updateSeekbar);

  // Initialize display
  //updateSeekbar();

  fetch('./svgs/down_laurynhill.svg')
  .then(response => response.text())
  .then(svgText => {
    //console.log(svgText);
    // Ensure there is a container for the SVG
    let container = document.getElementById('svgholder-top');
    container.innerHTML = svgText;
    svgDoc = container.querySelector('svg');
    svgDoc.setAttribute('preserveAspectRatio', 'none' );
    svgDoc.setAttribute('viewBox', '0 0 100 500' );
    svgDoc.style.width = '100%';
    svgDoc.style.height = '100%';
    // Example: access frame4



    console.log("topSVG LOADED");
    



  })
  .catch(err => {
    console.error('Error loading SVG:', err);
  });


  fetch('./svgs/up_andre300.svg')
  .then(response => response.text())
  .then(svgText => {
    //console.log(svgText);
    // Ensure there is a container for the SVG
    let lowercontainer = document.getElementById('svgholder-bottom');
    lowercontainer.innerHTML = svgText;
    bottomsvgDoc = lowercontainer.querySelector('svg');
    bottomsvgDoc.setAttribute('preserveAspectRatio', 'none' );
    bottomsvgDoc.setAttribute('viewBox', '20 200 100 293' );
    bottomsvgDoc.style.width = '100%';
    bottomsvgDoc.style.height = '100%';



    console.log("bottomSVG LOADED");
    



  })
  .catch(err => {
    console.error('Error loading SVG:', err);
  });







});

audioplayer.addEventListener("playing", (event) => {
  requestAnimationFrame(update_frame);
});

audioplayer.addEventListener("seeking", (event) => {
  //console.log("Video is seeking a new position.");
  update_frame()
});


function update_frame(){
  if (!audioplayer.paused){
    let duration = audioplayer.duration;
    let currentTime = audioplayer.currentTime;
    let frame = Math.floor((currentTime / duration) * max_frame);
    //console.log("The current frame is" + frame);

    nextframe(frame);
    seekbar.value = audioplayer.currentTime;
    requestAnimationFrame(update_frame);
  }
  else {
      let duration = audioplayer.duration;
      let currentTime = audioplayer.currentTime;
      let frame = Math.floor((currentTime / duration) * max_frame);
      //console.log("The current frame is" + frame);
      seekbar.value = audioplayer.currentTime;
      nextframe(frame);

  }
  
}

function nextframe(frame){
  current_frame = frame
  console.log(current_frame);
  //console.log('morphing to frame ' + current_frame);
  if (current_frame > max_frame){
    current_frame = min_frame
  };
    
  let down_frame_string = `#dframe${current_frame}`;
  let upper_frame_string = `#uframe${current_frame}`;
  gsap.to(lower_initial_frame, { duration: 1/10, morphSVG: down_frame_string });
  gsap.to(upper_initial_frame, { duration: 1/10, morphSVG: upper_frame_string });

  if (current_frame < 10) {
    leftext.textContent = "Press Play"
    righttext.textContent = "to Start"
  }
  if (current_frame >= 10 && current_frame < 11) {
    leftext.textContent = "Big Text Here asd asdfa asdf asd adfa asd How long can this go... how low can this go? that is the question. I really need to see the limit ofthis shit, will it decrease the text size or just change other thigns. I really wonder. Hopefully it just fits it all and doesnt try to make me scroll or ovreflow somewhere"
    righttext.textContent = "Big Text Here asd asdfa asdf asd adfa asd How long can this go... how low can this go? that is the question. I really need to see the limit ofthis shit, will it decrease the text size or just change other thigns. I really wonder. Hopefully it just fits it all and doesnt try to make me scroll or ovreflow somewhere"
  }
  if (current_frame >= 11){
    leftext.textContent = "";
    righttext.textContent = ""
  }

  
  
}







