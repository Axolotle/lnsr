function resizeRuler() {
    let width = document.getElementsByTagName('main')[0].getBoundingClientRect().width;
    let separator = document.getElementById("separator").getBoundingClientRect().width;
    if (width <= maxW) {
        let toRemove = maxW - width + separator;
        svgs[1].width.baseVal.value = baseW - toRemove;
        if (parts.classList.contains("hide")) {
            svgs[0].classList.add("hide");
            parts.classList.remove("hide");
            document.querySelector("#ruler span").classList.add("correction");
        }
    } else if (!parts.classList.contains("hide")) {
        svgs[0].classList.remove("hide")
        parts.classList.add("hide");
        document.querySelector("#ruler span").classList.remove("correction");
    }
}

function displayEquivalentMesure(e) {
    let dataset = e.target.dataset.equivalent.split("//");
    let previous = e.target.innerHTML;
    e.target.innerHTML = dataset.shift();
    e.target.dataset.equivalent = [...dataset, previous].join("//");
}

function changeFont(e) {
    let main = document.getElementById('content');
    if (main.classList.contains('pxph')) {
        main.classList.replace('pxph', 'hack');
        e.target.classList.replace('hack', 'pxph');
    } else {
        main.classList.replace('hack', 'pxph');
        e.target.classList.replace('pxph', 'hack');
    }
}

var maxW = 1161;
var svgs = document.querySelectorAll("#ruler svg");
var parts = document.getElementById("ruler-parts");
for (let svg of svgs) {
    svg.width.baseVal.value *= 1.025;
    svg.height.baseVal.value *= 1.025;
}
var baseW = svgs[1].width.baseVal.value;

window.onresize = resizeRuler;
resizeRuler();

for (let elem of document.getElementsByClassName('distance')) {
    elem.onclick = displayEquivalentMesure;
}

document.getElementById('font-change').onclick = changeFont;

document.getElementById('ruler').onclick = () => {
    return fetch('rulerRequest', {
        method: "POST"
    }).then(response => {
        return response.json();
    }).then(data => {
        console.log(data);
        document.getElementById('download').classList.remove('hide');
    });
};
