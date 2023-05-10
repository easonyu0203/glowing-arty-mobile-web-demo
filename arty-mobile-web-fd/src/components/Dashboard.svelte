<script lang="ts">
	interface Prediction {
		score: number;
		label: string;
	}
	export let predictions: Prediction[] = [];

	const getColor = (score: number) => {
		if (score > 0.8) {
			return 'bg-green-400';
		} else if (score > 0.6) {
			return 'bg-green-300';
		} else if (score > 0.4) {
			return 'bg-yellow-300';
		} else if (score > 0.2) {
			return 'bg-orange-400';
		} else {
			return 'bg-red-400';
		}
	};
</script>

<div class="w-full max-w-xl">
	<ul class="w-full flex flex-col">
		{#each predictions as prediction}
			<li class="w-full flex items-center my-1 gap-2">
				<span class="w-1/3">{prediction.label}</span>
				<div class="relative w-1/2 h-3 bg-gray-300 rounded-full">
					<div
						class={`absolute top-0 left-0 ${getColor(prediction.score)} rounded-full h-full`}
						style={`width: ${prediction.score * 100}%`}
					/>
				</div>
				<span>{prediction.score.toFixed(2)}</span>
			</li>
		{/each}
	</ul>
</div>
