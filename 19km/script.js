if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

var container, stats;
var camera, scene, renderer, controls;

var models, models2, models3;

var clock = new THREE.Clock();

var tim = Date.now();
var distance = 0;
var n = 3;

var div = document.getElementById("data");
var div2 = document.getElementById("dataCont");


init(function() {
	animate();
});


function init(callback) {

	container = document.getElementById( 'container' );

	//camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 2000 );
	camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 2000 );
	camera.position.set( 0, 0, -15 );

	scene = new THREE.Scene();
	camera.lookAt(scene.position);


	// collada

	var loader = new THREE.ColladaLoader(callback);
	loader.options.convertUpAxis = true;
	loader.load( 'voxelContainer.dae', function ( collada ) {
		var object = collada.scene;

		object.scale.set( 0.1, 0.1, 0.1);
		object.position.set( 0, -4.1, 0 );

		// for (var a = 0; a < 20; a++) {
		// 	for (var b = 0; b < 15; b++) {
		// 		var g = object.clone();
		// 		g.position.y = 8.2 * b - 4.1;
		// 		g.position.z = 7.7 * a;
		// 		scene.add(g);
		// 	}
		// }

		var obj2 = object.clone();
		//x, z, y
		obj2.position.set(0,4.1,0);
		var obj3 = object.clone();
		obj3.position.set(-19,-4.1,0);
		var obj4 = obj3.clone();
		obj4.position.set(-19,4.1,0);

		var obj5 = obj2.clone();
		obj5.position.set(-38,-4.1,0);
		var obj6 = obj5.clone();
		obj6.position.set(-38,4.1,0);

		scene.add( object, obj2, obj3, obj4, obj5, obj6);
		models = [object, obj2];
		models2 = [obj3, obj4];
		models3 = [obj5, obj6];


		callback();

	} );

	//

	var gridHelper = new THREE.GridHelper( 19, 20 );
	scene.add( gridHelper );

	//

	var ambientLight = new THREE.AmbientLight( 0xFFFFFF );//0xcccccc
	scene.add( ambientLight );

	var directionalLight = new THREE.DirectionalLight( 0xffffff );
	directionalLight.position.set( 0, 5, -1 ).normalize();
	scene.add( directionalLight );

	//

	renderer = new THREE.WebGLRenderer();
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth, window.innerHeight );
	container.appendChild( renderer.domElement );

	//

	controls = new THREE.OrbitControls( camera, renderer.domElement );

	//

	//stats = new Stats();
	//container.appendChild( stats.dom );

	//

	window.addEventListener( 'resize', onWindowResize, false );

}

function onWindowResize() {

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize( window.innerWidth, window.innerHeight );

}

function animate() {
	var delta = clock.getDelta();

	distance += delta*3.14159;
	var s = Date.now();
	let dis = (distance*10*31.8842105)/1000;
	div2.innerHTML = "container n°" + n + "/3194"
	div.innerHTML = (Math.round(dis*1000)/1000).toFixed(3) + " m";

	if (models[0].position.x >= 38) {
		for (var i = 0; i < models.length; i++) {
			models[i].position.x = 19;
			models2[i].position.x = 0;
			models3[i].position.x = -19;
		}
		console.log(dis,n, dis/6.058, dis/n);

		n++;
		tim = Date.now();
	}
	else {
		for (var i = 0; i < models.length; i++) {
			models[i].position.x += delta*3.14159;
			models2[i].position.x += delta*3.14159;
			models3[i].position.x += delta*3.14159;
		}
	}


	requestAnimationFrame( animate );

	render();

	//stats.update();

}

function render() {

	renderer.render( scene, camera );

}
