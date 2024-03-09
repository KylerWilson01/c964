import { type JwtPayload } from 'jwt-decode';

export interface UserResponsePayload extends JwtPayload {
	user_id: number;
}
