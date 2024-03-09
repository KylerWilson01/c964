<script lang="ts">
    import axios from 'axios';
    import type { Recommendation } from '../types/recommendation';
    import { user } from '../stores/user';
    import { get } from 'svelte/store';

    export let recommendation: Recommendation;
    let disabled = false;

    const onChecked = async (
        e: MouseEvent & {
            currentTarget: EventTarget & HTMLButtonElement;
        }
    ) => {
        try {
            const userInfo = get(user);

            if (!userInfo) {
                return;
            }

            await axios.post('http://localhost:8000/api/ratings/save/', {
                movieId: recommendation.movie.movieId,
                rating: parseInt(e.currentTarget.value),
                userId: userInfo.id
            });
            disabled = true;
        } catch {
            disabled = false;
        }
    };

    const buttons = [1, 2, 3, 4, 5];
</script>

<div>
    <h3>{recommendation.movie.title}</h3>
    <p>Genres: {recommendation.movie.genres.split('|').join(', ')}</p>

    {#each buttons as value}
        <button
            on:click={(e) => {
                onChecked(e);
            }}
            {disabled}
            {value}>{value}</button
        >
    {/each}
</div>
