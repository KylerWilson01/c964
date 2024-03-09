<script lang="ts">
    import type { PageData } from './$types';
    import RatingCard from '$lib/RatingCard.svelte';
    import PrivateRoute from '$lib/PrivateRoute.svelte';
    import Chart from '$lib/Chart.svelte';

    export let data: PageData;
</script>

<PrivateRoute>
    <div class="chart-container">
        <Chart
            genres={data.data.map((r) => {
                if (parseInt(r.rating) > 4) return '';
                return r.movie.genres;
            })}
            title="Rated above 4"
            type="bar"
        />

        <Chart
            genres={data.data.map((r) => {
                if (parseInt(r.rating) >= 4) return '';
                return r.movie.genres;
            })}
            title="Rated at or below 4"
            type="bar"
        />
    </div>

    <h3>Movies Rated</h3>
    <ul class="ratings-container">
        {#each data.data as rating}
            <li class="rating-bullet">
                <RatingCard {rating} />
            </li>
        {/each}
    </ul>
</PrivateRoute>

<style lang="scss">
    .chart-container {
        display: flex;
        justify-content: space-around;
    }

    .ratings-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        list-style: none;
        margin: 0;
        padding: 0;
        row-gap: 1em;
        column-gap: 1em;

        .rating-bullet {
            max-width: 200px;
            border: 1px solid #ccc;
            padding: 0.5em;
        }
    }
</style>
