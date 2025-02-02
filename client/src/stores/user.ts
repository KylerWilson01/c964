import { writable, type Writable } from 'svelte/store';
import type { User } from '../types/user';

export const user: Writable<User | null> = writable(null);
