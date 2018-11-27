function resizeRuler() {
    var width = document.getElementsByTagName('main')[0].getBoundingClientRect().width;
    var separator = document.getElementById("separator").getBoundingClientRect().width;
    if (width <= maxW) {
        let toRemove = maxW - width + separator;
        svgs[1].width.baseVal.value = baseW - toRemove;
        if (parts.classList.contains("hide")) {
            svgs[0].classList.add("hide");
            parts.classList.remove("hide");
            document.querySelector("#ruler span").classList.add("white");
        }
    } else if (!parts.classList.contains("hide")) {
        svgs[0].classList.remove("hide")
        parts.classList.add("hide");
        document.querySelector("#ruler span").classList.remove("white");
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
