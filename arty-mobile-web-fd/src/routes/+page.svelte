<script lang="ts">
	import { onMount } from 'svelte';
	import Dashboard from '../components/Dashboard.svelte';

	interface Prediction {
		score: number;
		label: string;
	}

	let videoElement: HTMLVideoElement;
	let predictions: Prediction[] = [];

	onMount(async () => {
		await getVideoStream();

		let intervalId = setInterval(async () => {
			await predict_frame();
		}, 1000);

		return () => {
			clearInterval(intervalId);
		};
	});

	const getVideoStream = async () => {
		videoElement.srcObject = await navigator.mediaDevices.getUserMedia({
			video: {
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
		const response = await fetch('http://' + import.meta.env.VITE_PREDICT_URL, {
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
		<video class=" rounded w-full h-full" autoplay muted bind:this={videoElement} />
	</div>

	<!-- <button on:click={predict_frame} class=" rounded text-3xl bg-orange-600">Predict</button> -->

	<Dashboard {predictions} />
</div>
