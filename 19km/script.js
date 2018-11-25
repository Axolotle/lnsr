function init() {
	display = document.getElementById('display');

	var loader = new THREE.ColladaLoader();
	loader.options.convertUpAxis = true;
	loader.load( 'voxelContainer.dae', function (collada) {
		var container = collada.scene;
		container.scale.set(0.1, 0.1, 0.1);

		containers = [
			[container, container.clone()],
			[container.clone(), container.clone()],
			[container.clone(), container.clone()]
		];

		containers.move = function (x) {
			for (let i = 0; i < this.length; i++) {
				for (let j = 0; j < this[i].length; j++) {
					this[i][j].position.x += x;
				}
			}
		};

		containers.reset = function () {
			var containersPos = [
				[[  0, -4.1, 0], [  0, 4.1, 0]],
				[[-19, -4.1, 0], [-19, 4.1, 0]],
				[[-38, -4.1, 0], [-38, 4.1, 0]]
			]

			for (let i = 0; i < this.length; i++) {
				for (let j = 0; j < this[i].length; j++) {
					containers[i][j].position.set(...containersPos[i][j]);
				}
			}
		}

		for (let i = 0; i < containers.length; i++) {
			for (let j = 0; j < containers[i].length; j++) {
				scene.add(containers[i][j]);
			}
		}
		setupAnim();
	} );


	scene = new THREE.Scene();

	camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 2000);
	camera.position.set(0, 0, -15);
	camera.lookAt(scene.position);

	renderer = new THREE.WebGLRenderer();
	renderer.setPixelRatio(window.devicePixelRatio);
	renderer.setSize(window.innerWidth, window.innerHeight);
	display.appendChild(renderer.domElement);

	var ambientLight = new THREE.AmbientLight(0xFFFFFF);//0xcccccc
	scene.add(ambientLight);

	var directionalLight = new THREE.DirectionalLight(0xffffff);
	directionalLight.position.set(0, 5, -1).normalize();
	scene.add(directionalLight);

	// var gridHelper = new THREE.GridHelper( 19, 20 );
	// scene.add( gridHelper );

	// controls = new THREE.OrbitControls( camera, renderer.domElement );

	window.addEventListener('resize', onWindowResize, false);

}

async function setupAnim() {
		n = 1;
		distance = 0;

		containers.reset();
		renderer.render(scene, camera);
		clock = new THREE.Clock();

		numberElem.textContent = 'container n°' + n + '/3194';
		distanceElem.textContent = '0 m';

		await sleep(2000);
		animate();
}

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
}

async function animate() {
	var raf = requestAnimationFrame(animate);
	time = clock.elapsedTime;
	var delta = clock.getDelta();
	var actualPos = containers[0][0].position.x;
	var step = delta * meterIn3D;

	distance += step;
	numberElem.textContent = 'container n°' + n + '/3194';
	distanceElem.textContent = (distance / meterIn3D).toFixed(3) + ' m';

	// cancel the animation after last container
	if (actualPos >= 57) {
		cancelAnimationFrame(raf);
		await sleep(2000);
		setupAnim();
	}
	// increment container's number at first and last container
	else if ((n === maxN - 1 && actualPos >= 38) || (n == 1 && actualPos >= 19)) {
		console.log('distance', (distance / meterIn3D), actualPos, time);
		n++;
	}
	// reset second container's position
	else if (n < maxN && actualPos >= 38) {
		containers.move(-19);
		n++;
	}
	containers.move(step);

	renderer.render(scene, camera);
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}


// animation speed is 1 m/s (3.6 km/h)
// convert meter to 3D units to define 1 3Dunit/s
var widthMeter = 6.058;
var width3D = 19;
var meterIn3D = width3D / widthMeter;
var maxN = 4;

if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

var display;
var camera, scene, renderer, controls;

var containers;

var clock, time;

var distance, n;

var numberElem = document.getElementById('containersNumber');
var distanceElem = document.getElementById('totalDistance');


init(animate);
