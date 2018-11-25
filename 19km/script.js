function init(callback) {
	display = document.getElementById( 'display' );

	var loader = new THREE.ColladaLoader(callback);
	loader.options.convertUpAxis = true;
	loader.load( 'voxelContainer.dae', function ( collada ) {
		var container = collada.scene;
		container.scale.set(0.1, 0.1, 0.1);

		containers = [
			[container, container.clone()],
			[container.clone(), container.clone()],
			[container.clone(), container.clone()]
		]

		containers.move = function (x) {
			for (let i = 0; i < this.length; i++) {
				for (let j = 0; j < this[i].length; j++) {
					this[i][j].position.x += x;
				}
			}
		};
		containers.resetPosition = function () {
			for (let i = 0; i < this[0].length; i++) {
				this[0][i].position.x = 19;
				this[1][i].position.x = 0;
				this[2][i].position.x = -19;
			}
		};

		var containersPos = [
			[[  0, -4.1, 0], [  0, 4.1, 0]],
			[[-19, -4.1, 0], [-19, 4.1, 0]],
			[[-38, -4.1, 0], [-38, 4.1, 0]]
		]

		for (let i = 0; i < containers.length; i++) {
			for (let j = 0; j < containers[i].length; j++) {
				containers[i][j].position.set(...containersPos[i][j]);
				scene.add(containers[i][j]);
			}
		}

		callback();

	} );

	camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 2000 );
	camera.position.set( 0, 0, -15 );

	scene = new THREE.Scene();
	camera.lookAt(scene.position);

	renderer = new THREE.WebGLRenderer();
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	display.appendChild( renderer.domElement );

	var ambientLight = new THREE.AmbientLight( 0xFFFFFF );//0xcccccc
	scene.add( ambientLight );

	var directionalLight = new THREE.DirectionalLight( 0xffffff );
	directionalLight.position.set( 0, 5, -1 ).normalize();
	scene.add( directionalLight );

	// var gridHelper = new THREE.GridHelper( 19, 20 );
	// scene.add( gridHelper );

	// controls = new THREE.OrbitControls( camera, renderer.domElement );

	window.addEventListener( 'resize', onWindowResize, false );

}

function onWindowResize() {
	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
	var delta = clock.getDelta();

	distance += delta*3.14159;
	let dis = (distance*10*31.8842105)/1000;
	div2.innerHTML = "container n°" + n + "/3194"
	div.innerHTML = (Math.round(dis*1000)/1000).toFixed(3) + " m";

	if (containers[0][0].position.x >= 38) {
		containers.resetPosition();
		console.log(dis, n, dis/6.058, dis/n);

		n++;
		tim = Date.now();
	}
	else {
		containers.move(delta * 3.14159);
	}

	requestAnimationFrame(animate);

	renderer.render(scene, camera);
}


if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

var display;
var camera, scene, renderer, controls;

var containers;

var clock = new THREE.Clock();

var tim = Date.now();
var distance = 0;
var n = 1;

var div = document.getElementById("data");
var div2 = document.getElementById("dataCont");


init(animate);
