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
            this.layers[i].update(size, this.step);
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
        this.name = layerElem.id + '-' + layerElem.getAttribute('stroke');
        this.multiplier = 1;
        this.texts = Array.from(layerElem.getElementsByTagName('text')).map(elem => {
            return {
                elem: elem,
                range: elem.dataset.range ? parseOptions(elem.dataset.range) : undefined
            };
        })
        this.translates = Array.from(layerElem.querySelectorAll('[data-translate]')).map(elem => {
            return {
                elem: elem,
                range: parseOptions(elem.dataset.range),
                translate: parseOptions(elem.dataset.translate)
            };
        });
    }

    hide() {
        this.elem.classList.add('hide');
    }

    transform(matrix, multiplier) {
        this.elem.setAttribute('transform', matrix);
        this.elem.classList.remove('hide');
        this.multiplier = multiplier;
    }

    update(width, step) {
        if (this.multiplier !== 1) step += this.multiplier < 1 ? -100 : 100;
        console.log(this.name, 'step', step);
        if (this.texts.length > 0) this.updateTextSize(width, step);
        if (this.translates.length > 0) this.updateTranslate(step);
    }

    updateTextSize(width, step) {
        for (let i = this.texts.length - 1; i > -1; i--) {
            let {elem, range} = this.texts[i];
            if ((range && (step >= range[0] && step <= range[1]))
                || range === undefined) {
                elem.style.fontSize = (width / 1000) * (40 * this.multiplier) + 'px';
            }
        }
    }

    updateTranslate(step) {
        for (let i = this.translates.length - 1; i > -1; i--) {
            let {elem, range, translate} = this.translates[i];
            if (step >= range[0] && step <= range[1]) {
                let ratio = Math.pow((step - range[0]) / (range[1] - range[0]), 3);
                elem.setAttribute('transform',
                    `translate(${ratio * translate[0]},${ratio * translate[1]})`)
            }

        }
    }
}

function parseOptions(str) {
    return str.split(' ').map(value => {
        if (value.includes('.')) return parseFloat(value);
        else return parseInt(value);
    });
}

var svgMap = new SVGMap(document.getElementsByTagName('svg')[0]);
