import type { Movie } from './rating';

export interface Recommendation {
	movie: Movie;
	rating: string;
}

export interface RecommendationResponse {
	success: boolean;
	error: boolean | null;
	data: Recommendation[];
}
