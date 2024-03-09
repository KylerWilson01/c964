<script lang="ts">
    import { Chart, type ChartConfiguration, type ChartTypeRegistry } from 'chart.js';
    import 'chart.js/auto';
    import { onMount } from 'svelte';

    export let genres: string[];
    export let title: string;
    export let type: keyof ChartTypeRegistry;

    const genreMap: Map<string, number> = new Map();

    genres.forEach((genre) => {
        if (genre === '') return;
        const gen = genre.split('|');
        gen.forEach((g) => genreMap.set(g, (genreMap.get(g) || 0) + 1));
    });

    const genreData = Array.from(genreMap.entries()).sort((a, b) => b[1] - a[1]);

    let graph: HTMLCanvasElement;
    const data = {
        labels: genreData.map(([key]) => key),
        datasets: [
            {
                label: title,
                data: genreData.map(([_, value]) => value),
                backgroundColor: [
                    'rgba(255, 134,159,0.4)',
                    'rgba(98,  182, 239,0.4)',
                    'rgba(255, 218, 128,0.4)',
                    'rgba(113, 205, 205,0.4)',
                    'rgba(170, 128, 252,0.4)',
                    'rgba(255, 177, 101,0.4)'
                ],
                borderWidth: 2,
                borderColor: [
                    'rgba(255, 134, 159, 1)',
                    'rgba(98,  182, 239, 1)',
                    'rgba(255, 218, 128, 1)',
                    'rgba(113, 205, 205, 1)',
                    'rgba(170, 128, 252, 1)',
                    'rgba(255, 177, 101, 1)'
                ]
            }
        ]
    };

    const config: ChartConfiguration = {
        type: type,
        data: data,
        options: {
            responsive: false,
            maintainAspectRatio: true
        }
    };

    onMount(() => {
        const ctx = graph.getContext('2d');

        if (!ctx) return;
        new Chart(ctx, config);
    });
</script>

<div>
    <canvas bind:this={graph} height={500} width={800} />
</div>
