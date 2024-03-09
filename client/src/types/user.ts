export interface User {
	id: number | null;
	refresh_token: string | null;
	access_token: string | null;
}

export interface UserResponse {
	refresh: string;
	access: string;
}
