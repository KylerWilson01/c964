export interface Movie {
	movieId: number;
	title: string;
	genres: string;
}

export interface Rating {
	id: number;
	userId: number;
	movie: Movie;
	rating: string;
	timestamp: number;
}

export interface RatingResponse {
	success: boolean;
	error: boolean | null;
	data: Rating[];
}
