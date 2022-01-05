<script>
	export let name;

	let loadTime;
	const fetchServerTime = async () => {
		const response = await (
			await fetch("http://localhost:7777/time")
		).json();
		return response.now;
	};
	const goFetch = () => {
		loadTime = fetchServerTime();
	};
	$: {
		loadTime = fetchServerTime();
	}
</script>

<main>
	<h1>Hello {name}!</h1>
	<p>
		Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to learn
		how to build Svelte apps.
	</p>
	<div>
		<button on:click={goFetch}>Refresh server time</button>
		<div id="servertime">
			{#await loadTime}
				loading ...
			{:then time}
				Server time was:<br />
				<strong>{time}</strong>
			{/await}
		</div>
	</div>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
