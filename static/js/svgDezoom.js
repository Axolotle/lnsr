class SVGMap {
    constructor(element) {
        this.elem = element;
        this.layers = Array.from(element.querySelectorAll('#layers > g')).map(layer => {
            return new Layer(layer);
        });
        this.actualLayer = 1;

        this.speed = 300000;
        this.scale = 1;
        this.baseSize = 299.792458;
        this.zoomValue = 0;

        this.switchLayers(0);
        this.render(this.baseSize);

        window.addEventListener('wheel', (e) => {
            if (e.deltaY < 0) {
                this.zoom(1);
            } else {
                this.zoom(-1);
            }
        });

        window.addEventListener('keypress', e => {
            if (e.key != ' ') return;
            let multiplier = 0;
            this.layers.filter(layer => !layer.elem.classList.contains('hide'))
            .forEach(layer => console.log(layer.name, Math.round(this.width + 1000 * multiplier++)));
        });

        // requestAnimationFrame(this.animate.bind(this));
    }

    set viewBox(args) {
        this.elem.setAttribute('viewBox', [args[0], args[0], args[1], args[1]].join(' '));
    }

    get width() {
        return parseFloat(this.elem.getAttribute('viewBox').split(' ')[2]);
    }

    zoom(direction) {
        this.zoomValue += -direction * 5;
        let size = this.baseSize * Math.exp(this.zoomValue/100) * this.scale;
        if (size > 1000 || size < 1) {
            size *= this.switchLayers(direction);
        }
        this.render(size);
    }

    animate(timestamp) {
        let extraDistance = timestamp * this.speed;
        let size = (this.baseSize + this.baseSize * extraDistance) * this.scale;
        if (size > 1000) {
            size *= this.switchLayers(-1);
        }
        this.render(size);
        requestAnimationFrame(this.animate.bind(this));
    }

    switchLayers(direction) {
        this.actualLayer -= direction;
        let n = this.actualLayer;
        if (this.layers[n-2]) this.layers[n-2].hide();
        if (this.layers[n-1]) this.layers[n-1].transform(0.001, 1000);
        if (this.layers[n])   this.layers[n].transform(1, 1);
        if (this.layers[n+1]) this.layers[n+1].transform(1000, 0.001);
        if (this.layers[n+2]) this.layers[n+2].hide();

        document.getElementById('scale').textContent = this.layers[n].elem.dataset.scalename;

        if (direction != 0) {
            let multiplier = direction == -1 ? 0.001 : 1000;
            this.scale *= multiplier;
            return multiplier;
        }
    }

    render(size) {
        this.viewBox = [-size / 2, size];
        let multiplier = 0;
        for (let i = this.actualLayer - 1; i <= this.actualLayer + 1; i++) {
            this.layers[i].update(size, Math.round(size + 1000 * multiplier++));
        }
    }
}

class Layer {
    constructor(layerElem) {
        this.elem = layerElem;
        this.hide();
        this.name = layerElem.dataset.scalename + '-' + layerElem.getAttribute('stroke');
        this.multiplier = 1;
	    this.transformables = Array.from(this.elem.getElementsByClassName('data'));
    }

    hide() {
        this.elem.classList.add('hide');
    }

    transform(scale, multiplier) {
        if (scale !== 1) {
            let pos = 0 * scale;
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
                if (key == 'textrange') {
                    this.updateTextSize(elem, options, width, step);
                } else if (key == 'translate') {
                    this.updateTranslate(elem, options, step);
                } else if (key == 'scale') {
                    this.updateScale(elem, options, step);
                } else if (['hide', 'show'].includes(key)) {
                    this.updateDisplay(elem, key, options, step);
                } else if (key == 'fade') {
                    this.updateFading(elem, options, step);
                } else {
                    this.updateClass(elem, key, options, step);
                }
            }
        });
    }

    updateTextSize(elem, range, width, step) {
        // range indexes: {0: startStep, 1: endStep}
        if (step >= range[0] && step <= range[1]) {
            if (elem.tagName === 'foreignObject') {
                for (var i = 0; i < elem.children.length; i++) {
                    elem.children[i].style.fontSize = (width / 1000) * (40 * this.multiplier) + 'px';
                }
            } else {
                elem.style.fontSize = (width / 1000) * (40 * this.multiplier) + 'px';
            }
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

    updateFading(elem, opts, step) {
        if (step >= opts[1] && step <= opts[2]) {
            let opacity = Math.pow((step - opts[1]) / (opts[2] - opts[1]), 3);
            elem.style.opacity = opts[0] === 0 ? 1 - opacity : opacity;
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
