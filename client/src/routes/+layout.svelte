<script lang="ts">
    import { onMount } from 'svelte';
    import { user } from '../stores/user';
    import axios from 'axios';
    import { jwtDecode } from 'jwt-decode';
    import type { UserResponsePayload } from '../types/jwt';
    import { get } from 'svelte/store';
    import { goto } from '$app/navigation';

    let u = get(user);

    user.subscribe((user) => {
        u = user;
    });

    const logout = async () => {
        user.update(() => null);
        await goto('/login');
    };

    onMount(async () => {
        try {
            const localRefresh = localStorage.getItem('refresh');

            if (localRefresh !== null) {
                const resp = await axios.post<{ access: string }>(
                    'http://localhost:8000/api/token/refresh/',
                    {
                        refresh: localStorage.getItem('refresh')
                    }
                );

                user.update(() => ({
                    id: jwtDecode<UserResponsePayload>(resp.data.access).user_id,
                    access_token: resp.data.access,
                    refresh_token: localRefresh
                }));
            }
        } catch (error) {
            console.log(error);
        }

        user.subscribe((value) => {
            if (value && value.refresh_token) {
                localStorage.setItem('refresh', value.refresh_token.toString());
            } else {
                localStorage.removeItem('refresh');
            }
        });
    });
</script>

<div class="nav">
    <div>
        <a href="/">Home</a>
        <a href="/rate">Recommendations</a>
        {#if u !== null && u.id !== null}
            <button
                on:click={(e) => {
                    e.preventDefault();
                    logout();
                }}>logout</button
            >
        {:else}
            <a href="/login">Login</a>
        {/if}
    </div>
    {#if u !== null && u.id !== null}
        <p>User Id: {u.id}</p>
    {/if}
</div>

<h1>Recommender App</h1>

<slot />

<style lang="scss">
    .nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0;
        margin: 0;
    }
</style>
