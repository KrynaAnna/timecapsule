// Function to expand textarea
function autoExpandTextarea() {
  const textarea = document.getElementById('text');
  textarea.style.height = '30vh';
  textarea.style.height = textarea.scrollHeight + 'px';

  const content = document.getElementsByClassName('second-container');
  content.style.height = '100vh';
  content.style.height = content.scrollHeight + '18px'
}


// Add an event listener to the 'scroll' event on the window
window.addEventListener('wheel', handleScroll);
// Function to handle the scroll event
function handleScroll(event) {
  event.preventDefault();
    const scrollDirection = event.deltaY > 0 ? 1 : -1;
    const scrollAmount = window.innerHeight * scrollDirection;
    window.scrollBy(0, scrollAmount);
}


// Automatically decrease the number from 1050 to 1025 with a step of 2
window.addEventListener('DOMContentLoaded', function () {
  const numberDiv = document.getElementById('number');
  const Div = document.getElementById('fiveth-container');

  Div.addEventListener('mouseover', function () {
    function decreaseNumber() {
      let currentNumber = parseInt(numberDiv.innerText);

      if (currentNumber < 1090) {
        currentNumber += 2;
        numberDiv.innerText = currentNumber.toString();
        setTimeout(decreaseNumber, 100); // Repeat the process every 1000 milliseconds
      }
    }
    decreaseNumber();
  });
});


// Audio
let aud = document.getElementById("myAudio");
let active = "False"

function playAud() {
    let aud = document.getElementById("myAudio");
    if (!aud) {
      console.error("Audio element not found.");
      return;
    }

    if (aud.paused) {
      aud.play();
    } else {
      aud.pause();
    }
  }

