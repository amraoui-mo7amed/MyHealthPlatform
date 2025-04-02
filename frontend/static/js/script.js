// to get current year
function getYear() {
    var currentDate = new Date();
    var currentYear = currentDate.getFullYear();
    if (document.querySelector("#displayYear")) {
        document.querySelector("#displayYear").innerHTML = currentYear;

    }
}

getYear();



/** google_map js **/

function myMap() {
    var mapProp = {
        center: new google.maps.LatLng(40.712775, -74.005973),
        zoom: 18,
    };
    var map = new google.maps.Map(document.getElementById("googleMap"), mapProp);
}

const heroArea = document.querySelector('.hero_area');
const images = [
    'static/images/animated_bg2.jpg',  // Add your other image paths here
    // 'static/images/bg2_1.jpg',
     'static/images/header_1.jpg',
    //  'static/images/header_2.jpg',
     'static/images/header_3.jpg',

];

let currentIndex = 0;

function changeBackground() {
    const nextIndex = (currentIndex + 1) % images.length;
    const nextImage = new Image();
    nextImage.src = images[nextIndex];

    nextImage.onload = () => {
        // Fade out current image
        heroArea.style.transition = 'opacity 1s';
        heroArea.style.opacity = 0;

        setTimeout(() => {
            // Change the background image
            heroArea.style.backgroundImage = `url(${images[nextIndex]})`;
            currentIndex = nextIndex;

            // Fade in new image
            heroArea.style.opacity = 1;
        }, 50);
    };
}

// Start the cycle
setInterval(changeBackground, 3000);

// Call changeBackground when DOM content is loaded
document.addEventListener('DOMContentLoaded', function () {
    changeBackground();
});


// about canvas animation 

// Select the canvas and set its dimensions
const canvas = document.getElementById('about-canvas');
const ctx = canvas.getContext('2d');

// Set canvas dimensions to be square
const canvasSize = Math.min(window.innerWidth * 0.8, window.innerHeight * 0.8); // Ensure the canvas fits the screen
canvas.width = canvasSize;
canvas.height = canvasSize;

// Array of image URLs
const aboutImages = [
    'static/images/sport.jpg',
    // 'static/images/about2.jpg',
    'static/images/about.jpg',
];

// Load all images dynamically
const imageAssets = [];
let loadedImages = 0;

aboutImages.forEach((url) => {
    const img = new Image();
    img.src = url;
    img.onload = () => {
        loadedImages++;
        if (loadedImages === aboutImages.length) startAnimationSequence();
    };
    imageAssets.push(img);
});

// Number of vertical pieces
const numPieces = 5;

// Start the animation sequence
function startAnimationSequence() {
    let currentImageIndex = 0;

    function animateNextImage() {
        const outgoingImage = imageAssets[currentImageIndex];
        currentImageIndex = (currentImageIndex + 1) % imageAssets.length; // Loop back to the first image
        const incomingImage = imageAssets[currentImageIndex];

        // Animate transition between outgoing and incoming images
        animateTransition(outgoingImage, incomingImage, animateNextImage);
    }

    animateNextImage(); // Start the infinite loop
}

// Animate transition between two images
function animateTransition(outgoingImage, incomingImage, onComplete) {
    // Scale both images to fit the square canvas
    const scaleOutgoing = canvasSize / Math.max(outgoingImage.width, outgoingImage.height);
    const scaledWidthOutgoing = outgoingImage.width * scaleOutgoing;
    const scaledHeightOutgoing = outgoingImage.height * scaleOutgoing;

    const scaleIncoming = canvasSize / Math.max(incomingImage.width, incomingImage.height);
    const scaledWidthIncoming = incomingImage.width * scaleIncoming;
    const scaledHeightIncoming = incomingImage.height * scaleIncoming;

    // Calculate the width of each piece
    const pieceWidthOutgoing = scaledWidthOutgoing / numPieces;
    const pieceWidthIncoming = scaledWidthIncoming / numPieces;

    // Animation variables for incoming image
    const positionsIncoming = Array(numPieces).fill(-scaledHeightIncoming); // Start above the canvas
    const speedsIncoming = Array(numPieces).fill(10); // Increased speed (from 5 to 10)
    const isFallingIncoming = Array(numPieces).fill(false); // Tracks if a piece is falling

    let lastTime = 0;

    function animate(time) {
        const deltaTime = time - lastTime;
        lastTime = time;

        // Clear the canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Draw outgoing image (fully visible)
        ctx.drawImage(
            outgoingImage,
            0, 0, outgoingImage.width, outgoingImage.height, // Source rectangle
            (canvas.width - scaledWidthOutgoing) / 2, (canvas.height - scaledHeightOutgoing) / 2, scaledWidthOutgoing, scaledHeightOutgoing // Destination rectangle
        );

        // Draw incoming image pieces
        for (let i = 0; i < numPieces; i++) {
            if (isFallingIncoming[i]) {
                positionsIncoming[i] += speedsIncoming[i] * (deltaTime / 16); // Normalize speed

                // Stop falling when the piece reaches its final position
                if (positionsIncoming[i] >= 0) {
                    positionsIncoming[i] = 0;
                    isFallingIncoming[i] = false;

                    // Start the next piece falling
                    if (i + 1 < numPieces) {
                        isFallingIncoming[i + 1] = true;
                    } else if (i === numPieces - 1) {
                        // All pieces have fallen in, trigger the callback
                        onComplete && onComplete();
                    }
                }
            }

            // Draw the piece
            const sourceX = (i * incomingImage.width) / numPieces; // Horizontal position in the source image
            const destX = (i * scaledWidthIncoming) / numPieces + (canvas.width - scaledWidthIncoming) / 2; // Centered on the canvas
            const destY = positionsIncoming[i] + (canvas.height - scaledHeightIncoming) / 2; // Centered vertically
            ctx.drawImage(
                incomingImage,
                sourceX, 0, incomingImage.width / numPieces, incomingImage.height, // Source rectangle
                destX, destY, pieceWidthIncoming, scaledHeightIncoming // Destination rectangle
            );
        }

        // Start the first piece falling for the incoming image
        if (!isFallingIncoming.some(Boolean)) {
            isFallingIncoming[0] = true;
        }

        // Continue the animation until all pieces have fallen into place
        if (positionsIncoming.some(pos => pos < 0)) {
            requestAnimationFrame(animate);
        }
    }

    // Start the animation loop
    requestAnimationFrame(animate);
}