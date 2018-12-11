function dezoom(e) {
    let delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
    let svg = document.getElementsByTagName('svg')[0];
    zoomRatio *= 1.05;
    let addX = delta * zoomRatio;
    let addY = (delta * zoomRatio * -1) * 2;
    if (x + addX < 0) {
        x = 499.5;
        y = 1;
        zoomRatio = 0.1;
        addX = addX / 1000;
        addY = addY / 1000;
        layers[layerNumber].classList.add('hide');
        layers[layerNumber+1].setAttribute('transform', "matrix(0.001 0 0 0.001 499.5 499.5)")
        layers[layerNumber+2].setAttribute('transform', "")
        layers[layerNumber+3].classList.remove('hide');
        layers[layerNumber+3].setAttribute('transform', "matrix(1000 0 0 1000 -499500 -499500)")
        layerNumber++;
    }
    x += addX;
    y += addY;
    console.log(x, y);
    svg.setAttribute("viewBox", [x, x, y, y].join(' '))
}

var zoom_lvl = 1;
var x = 499.5;
var y = 1;
var zoomRatio = 0.1;
var layers = document.querySelectorAll('svg g');
var layerNumber = 0;

window.addEventListener("mousewheel", dezoom); // IE9, Chrome, Safari, Opera
window.addEventListener("DOMMouseScroll", dezoom); // Firefox
