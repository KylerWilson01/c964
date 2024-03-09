<script lang="ts">
    import Chart from '$lib/Chart.svelte';
    import PrivateRoute from '$lib/PrivateRoute.svelte';
    import RecommendationCard from '$lib/RecommendationCard.svelte';
    import axios from 'axios';
    import type { RecommendationResponse } from '../../types/recommendation';
    import { get } from 'svelte/store';
    import { user } from '../../stores/user';

    var u = get(user);

    const recommendations = async () => {
        if (!u || !u.id) {
            return { success: false, error: true, data: [] } as RecommendationResponse;
        }

        const resp = await axios.get<RecommendationResponse>(
            'http://localhost:8000/api/recommendations/',
            {
                params: {
                    userId: u.id
                }
            }
        );

        return resp.data;
    };
</script>

<PrivateRoute>
    <h2>Rate Recommendations</h2>

    {#await recommendations()}
        <div>Getting recommendations</div>
    {:then data}
        <Chart
            genres={data.data.map((r) => r.movie.genres)}
            title="Recommended amount"
            type="polarArea"
        />

        <ul>
            {#each data.data as recommendation}
                <li><RecommendationCard {recommendation} /></li>
            {/each}
        </ul>
    {/await}
</PrivateRoute>
