if ( ! Detector.webgl ) Detector.addGetWebGLMessage();

			var container, stats;
			var camera, scene, renderer, controls;

			var models;

			var clock = new THREE.Clock();

			init(function() {
				animate();
			});


			function init(callback) {

				container = document.getElementById( 'container' );

				//camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 2000 );
				camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 2000 );
				camera.position.set( 0, 0, -20 );

				scene = new THREE.Scene();

				// collada

				var loader = new THREE.ColladaLoader(callback);
				loader.options.convertUpAxis = true;
				loader.load( 'voxelContainer.dae', function ( collada ) {

					var object = collada.scene;

					object.scale.set( 0.1, 0.1, 0.1);
					object.position.set( 0, -4.1, 0 );

					var obj2 = object.clone();
					//x, z, y
					obj2.position.set(0,4.1,0);

					scene.add( object, obj2 );
					models = [object, obj2];
					callback();

				} );

				//

				var gridHelper = new THREE.GridHelper( 10, 20 );
				scene.add( gridHelper );

				//

				var ambientLight = new THREE.AmbientLight( 0xcccccc );
				scene.add( ambientLight );

				var directionalLight = new THREE.DirectionalLight( 0xffffff );
				directionalLight.position.set( 0, 1, -1 ).normalize();
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

				for (var i = 0; i < models.length; i++) {
					models[i].position.x += delta*2;
				}

				requestAnimationFrame( animate );

				render();

				//stats.update();

			}

			function render() {

				renderer.render( scene, camera );

			}
