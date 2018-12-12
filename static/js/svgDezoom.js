class SVGMap {
    constructor(element) {
        this.element = element;
        this.layers = element.querySelectorAll('#layers > g');
        this.actualLayer = 3;
        this.steps = 100;
        this.step = 100;

        for (let layer of this.layers) {
            layer.classList.add('hide');
        }
        this.switchLayer(this.actualLayer);
        this.zoom(0);

        // IE9, Chrome, Safari, Opera
        window.addEventListener('mousewheel', (e) => {
            this.zoom(-Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail))))
        });
        // Firefox
        window.addEventListener('DOMMouseScroll', (e) => {
            this.zoom(-Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail))))
        });

    }

    zoom(delta) {
        this.step += delta;
        if (this.step <= 0 || this.step >= this.steps) {
            this.step = delta === -1 ? this.steps - 1 : 0;
            this.actualLayer += delta;
            this.switchLayer(this.actualLayer);
        }
        let actualStep = this.step / this.steps;
        let x = 499.5 - (Math.pow(actualStep, 3) * 499.5);
        let y = Math.pow(actualStep, 3) * 999 + 1;
        this.element.setAttribute('viewBox', [x, x, y, y].join(' '));

    }

    switchLayer(n) {
        this.layers[n-2].classList.add('hide');
        this.layers[n-1].setAttribute('transform',
            'matrix(0.001 0 0 0.001 499.5 499.5)');
        this.layers[n-1].classList.remove('hide');
        this.layers[n].setAttribute('transform', '');
        this.layers[n].classList.remove('hide');
        this.layers[n+1].setAttribute('transform',
            'matrix(1000 0 0 1000 -499500 -499500)');
        this.layers[n+1].classList.remove('hide');
        this.layers[n+2].classList.add('hide');
        // "matrix(1000000 0 0 1000000 -499999500 -499999500)"

    }
}

var svgMap = new SVGMap(document.getElementsByTagName('svg')[0]);
