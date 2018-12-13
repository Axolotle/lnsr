class SVGMap {
    constructor(element) {
        this.elem = element;
        this.layers = Array.from(element.querySelectorAll('#layers > g')).map(layer => {
            return new Layer(layer);
        });
        this.actualLayer = 5;
        this.steps = 100;
        this.step = 100;

        let elements = this.elem.querySelectorAll(':not(g):not(text)');
        for (let i = elements.length - 1; i > -1; i--) {
            elements[i].setAttribute('vector-effect', 'non-scaling-stroke')
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
            this.step = delta === -1 ? this.steps : 1;
            this.actualLayer += delta;
            this.switchLayer(this.actualLayer);
        }

        let stepRatio = Math.pow(this.step / this.steps, 3);
        let start = 499.5 - stepRatio * 499.5;
        let size = stepRatio * 999 + 1;
        this.elem.setAttribute('viewBox', [start, start, size, size].join(' '));

        for (let i = this.actualLayer - 1; i <= this.actualLayer + 1; i++) {
            this.layers[i].updateTextSize(size);
        }
    }

    switchLayer(n) {
        this.layers[n-2].hide();
        this.layers[n-1].transform('matrix(0.001 0 0 0.001 499.5 499.5)', 1000);
        this.layers[n].transform('', 1);
        this.layers[n+1].transform('matrix(1000 0 0 1000 -499500 -499500)', 0.001);
        this.layers[n+2].hide();
    }
}

class Layer {
    constructor(layerElem) {
        this.elem = layerElem;
        this.elem.classList.add('hide');
        this.multiplier = 1;
        this.texts = Array.from(layerElem.getElementsByTagName('text'));
    }

    hide() {
        this.elem.classList.add('hide');
    }

    transform(matrix, multiplier) {
        this.elem.setAttribute('transform', matrix);
        this.elem.classList.remove('hide');
        this.multiplier = multiplier;
    }

    updateTextSize(width) {
        for (let text of this.texts) {
            text.style.fontSize = (width / 1000) * (40 * this.multiplier) + 'px'
        }
    }
}

var svgMap = new SVGMap(document.getElementsByTagName('svg')[0]);
