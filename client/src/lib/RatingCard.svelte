<script lang="ts">
    import type { Rating } from '../types/rating';

    export let rating: Rating;
</script>

<div>
    <p>Title: {rating.movie.title}</p>
    <p>Rating: {parseInt(rating.rating)}</p>
    <p>Genres: {rating.movie.genres.split('|').join(', ')}</p>
</div>
