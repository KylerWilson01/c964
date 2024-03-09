<script>
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { user } from '../stores/user';

	onMount(async () => {
		if (!$user) {
			await goto('/login');
		}
	});
</script>

{#if $user}
	<slot />
{/if}
