<script lang="ts">
	import { onMount } from 'svelte';
	import Dashboard from '../components/Dashboard.svelte';

	interface Prediction {
		score: number;
		label: string;
	}

	let videoElement: HTMLVideoElement;
	let predictions: Prediction[] = [];
	let is_user_mode: boolean = true;

	onMount(async () => {
		await getVideoStream();

		// predict every second
		// let intervalId = setInterval(async () => {
		// 	await predict_frame();
		// }, 1000);
		// return () => {
		// 	clearInterval(intervalId);
		// };
	});

	const getDeviceIds = () => {
		// Create an empty array to store the deviceIds
		const deviceIds: string[] = [];

		// Get a list of all available media devices
		navigator.mediaDevices
			.enumerateDevices()
			.then(function (devices) {
				// Iterate through the devices
				devices.forEach(function (device) {
					// Check if the device has a deviceId
					if (device.deviceId) {
						// Add the deviceId to the array
						deviceIds.push(device.deviceId);
					}
				});
			})
			.catch(function (error) {
				console.error('Error enumerating devices:', error);
			});
		return deviceIds;
	};

	let used_idx: number = -1;
	const getVideoStream = async () => {
		const devices = getDeviceIds();
		const used_device = devices[++used_idx % devices.length];
		videoElement.srcObject = await navigator.mediaDevices.getUserMedia({
			video: {
				facingMode: is_user_mode ? 'user' : 'environment',
				// deviceId: used_device,
				width: { ideal: 480 },
				height: { ideal: 480 }
			}
		});
	};

	const captureFrame = async () => {
		if (!videoElement) return;
		const canvas = document.createElement('canvas');
		canvas.width = videoElement.videoWidth;
		canvas.height = videoElement.videoHeight;
		canvas.getContext('2d')?.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

		const image = canvas.toDataURL('image/png');
		return image;
	};

	const predict = async (data_url: string): Promise<Prediction[]> => {
		// Send image data URL
		const response = await fetch(import.meta.env.VITE_PREDICT_URL, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ data_url })
		});
		// Handle response from endpoint
		const result = await response.json();
		return result;
	};

	let isProcessing = false;
	const predict_frame = async () => {
		const image = await captureFrame();
		if (!image || isProcessing) return;
		isProcessing = true;
		const result = await predict(image);
		isProcessing = false;
		predictions = result;
	};
</script>

<div class="w-full h-full flex flex-col justify-center items-center gap-4 px-8">
	<h1 class="text-3xl font-bold">Arty Demo App</h1>

	<div class=" bg-zinc-800 max-w-lg aspect-square rounded flex justify-center items-center">
		<video class=" rounded w-full h-full" playsinline autoplay muted bind:this={videoElement} />
	</div>
	<Dashboard {predictions} />

	<div class=" flex justify-around gap-8">
		<button
			on:click={async () => {
				is_user_mode = !is_user_mode;
				await getVideoStream();
			}}
			class=" px-2 rounded bg-stone-300">Change Camera</button
		>
		<button on:click={predict_frame} class=" px-2 rounded bg-stone-300">Predict</button>
	</div>
</div>
