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
    'static/images/bg2_1.jpg',
    // Add more images as needed
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


const aboutImages = [
    // 'static/images/bottle.jpg',
    'static/images/sport.jpg',
    'static/images/about2.jpg',

];

let abtcurrentIndex = 0;
const aboutImage = document.getElementById('about-image');

function changeAboutImage() {
    abtcurrentIndex = (abtcurrentIndex + 1) % aboutImages.length;
    aboutImage.src = aboutImages[abtcurrentIndex];
}
// Call changeAboutImage when DOM content is loaded
document.addEventListener('DOMContentLoaded', function () {
    changeAboutImage();
});
// Change image every 3 seconds
setInterval(changeAboutImage, 3000);