import axios from 'axios';
import type { PageLoad } from './$types';
import { type RatingResponse } from '../types/rating';
import { user } from '../stores/user';
import { get } from 'svelte/store';

export const load: PageLoad = async () => {
    const val = get(user);

    if (!val) {
        return { success: false, error: true, data: [] };
    }

    const response = await axios.get<RatingResponse>('http://localhost:8000/api/ratings/', {
        params: {
            userId: val.id
        }
    });

    const data = {
        ...response.data,
        data: response.data.data.sort((a, b) => parseInt(b.rating) - parseInt(a.rating))
    };

    return data;
};
