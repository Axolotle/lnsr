class SVGMap {
    constructor(element) {
        this.elem = element;
        this.layers = Array.from(element.querySelectorAll('#layers > g')).map(layer => {
            return new Layer(layer);
        });
        this.actualLayer = 6;
        this.steps = 100;
        this.step = 100;

        let elements = this.elem.querySelectorAll(':not(g):not(text)');
        for (let i = elements.length - 1; i > -1; i--) {
            elements[i].setAttribute('vector-effect', 'non-scaling-stroke')
        }

        this.switchLayer(this.actualLayer);
        this.zoom(0);

        var _this = this;
        function animate() {
            _this.zoom(1);
            requestAnimationFrame(animate);
        }
        // IE9, Chrome, Safari, Opera
        window.addEventListener('mousewheel', (e) => {
            requestAnimationFrame(() => {
                this.zoom(-Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail))));
            });
        });
        // Firefox
        window.addEventListener('DOMMouseScroll', (e) => {
            requestAnimationFrame(() => {
                this.zoom(-Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail))));
            });
        });

        window.addEventListener('keypress', e => {
            if (e.key == ' ') {
                let multiplier = [100, 0, -100];
                this.layers.filter(layer => !layer.elem.classList.contains('hide'))
                .forEach(layer => console.log(layer.name, this.step + multiplier.shift()));
            }
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
        let start = (499.5 - stepRatio * 499.5).toFixed(3);
        let size = (stepRatio * 999 + 1).toFixed(3);
        this.elem.setAttribute('viewBox', [start, start, size, size].join(' '));

        for (let i = this.actualLayer - 1; i <= this.actualLayer + 1; i++) {
            this.layers[i].update(size, this.step);
        }
    }

    switchLayer(n) {
        this.layers[n-2].hide();
        this.layers[n-1].transform(0.001, 1000);
        this.layers[n].transform(1, 1);
        this.layers[n+1].transform(1000, 0.001);
        this.layers[n+2].hide();
        document.getElementById('scale').textContent = this.layers[n].elem.dataset.scalename;
    }
}

class Layer {
    constructor(layerElem) {
        this.elem = layerElem;
        this.elem.classList.add('hide');
        this.name = layerElem.dataset.scalename + '-' + layerElem.getAttribute('stroke');
        this.multiplier = 1;
	    this.transformables = Array.from(this.elem.getElementsByClassName('data'));
    }

    hide() {
        this.elem.classList.add('hide');
    }

    transform(scale, multiplier) {
        if (scale !== 1) {
            let pos = 500 - 500 * scale;
            let matrix ='matrix('+scale+' 0 0 '+scale+' '+pos+' '+pos+')'
            this.elem.setAttribute('transform', matrix);
            this.elem.removeAttribute('id');
        } else {
            this.elem.removeAttribute('transform');
            this.elem.setAttribute('id', 'actual');
        }
        this.elem.classList.remove('hide');
        this.multiplier = multiplier;
    }

    update(width, step) {
        if (this.multiplier !== 1) step += this.multiplier < 1 ? -100 : 100;

        this.transformables.forEach(elem => {
            for (let key in elem.dataset) {
                let options = parseOptions(elem.dataset[key]);
                if (key === 'textrange') {
                    this.updateTextSize(elem, options, width, step);
                } else if (key === 'translate') {
                    this.updateTranslate(elem, options, step);
                } else if (key === 'scale') {
                    this.updateScale(elem, options, step);
                } else if (['hide', 'show'].includes(key)) {
                    this.updateDisplay(elem, key, options, step);
                } else {
                    this.updateClass(elem, key, options, step);
                }
            }
        });
    }

    updateTextSize(elem, range, width, step) {
        // range indexes: {0: startStep, 1: endStep}
        if (step >= range[0] && step <= range[1]) {
            elem.style.fontSize = (width / 1000) * (40 * this.multiplier) + 'px';
        }
    }

    updateTranslate(elem, opts, step) {
        // opts indexes: {0: translateX, 1: translateY, 2: startStep, 3: endStep}
        if (step >= opts[2] && step <= opts[3]) {
            let ratio = Math.pow((step - opts[2]) / (opts[3] - opts[2]), 3);
            elem.setAttribute('transform',
                'translate('+(ratio * opts[0]).toFixed(3)+','+(ratio * opts[1]).toFixed(3)+')'
            );
        }
    }

    updateScale(elem, opts, step) {
        // opts indexes: {0: scaleX, 1: scaleY, 2: translateX, 3: translateY, 4: startStep, 5: endStep}
        if (step >= opts[4] && step <= opts[5]) {
            let ratio = Math.pow((step - opts[4]) / (opts[5] - opts[4]), 3);
            ratio = [ratio * opts[0], ratio * opts[1]];
            elem.setAttribute('transform',
                'matrix('+(ratio[0]+1)+' 0 0 '+(ratio[1]+1)+' '+(ratio[0]*opts[2])+' '+(ratio[1]*opts[3])+')'
            );
        }
    }

    updateDisplay(elem, key, range, step) {
        let isHidden = elem.classList.contains('hide');
        let toggle = step >= range[0] && step <= range[1] // is in range
            ? (key === 'show' &&  isHidden) || (key === 'hide' && !isHidden)
            : (key === 'show' && !isHidden) || (key === 'hide' &&  isHidden);
        if (toggle) {
            elem.classList.toggle('hide');
        }
    }

    updateClass(elem, cssClass, range, step) {
        if (step >= range[0] && step <= range[1]) {
            if (!elem.classList.contains(cssClass))
                elem.classList.add(cssClass);
        } else if (elem.classList.contains(cssClass)) {
            elem.classList.remove(cssClass);
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
