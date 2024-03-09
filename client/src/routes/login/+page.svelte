<script lang="ts">
    import axios from 'axios';
    import { type UserResponse } from '../../types/user';
    import { jwtDecode } from 'jwt-decode';
    import type { UserResponsePayload } from '../../types/jwt';
    import { user } from '../../stores/user';
    import { goto } from '$app/navigation';

    user.subscribe(async (u) => {
        if (u && u.id) {
            await goto('/');
        }
    });

    const onLogin = async (e: SubmitEvent) => {
        e.preventDefault();
        try {
            if (e.target == null) return;
            const formData = new FormData(e.target as HTMLFormElement);

            const email = formData.get('email') as string;
            const password = formData.get('password') as string;

            const resp = await axios.post<UserResponse>('http://localhost:8000/api/login/', {
                username: email,
                password: password
            });

            const decoded = jwtDecode<UserResponsePayload>(resp.data.access);

            user.update(() => ({
                id: decoded.user_id,
                access_token: resp.data.access,
                refresh_token: resp.data.refresh
            }));
        } catch {
            user.update(() => null);
        }
    };

    const onRegister = async (e: SubmitEvent) => {
        e.preventDefault();
        try {
            if (e.target == null) return;
            const formData = new FormData(e.target as HTMLFormElement);

            const email = formData.get('email') as string;
            const first_name = formData.get('first_name') as string;
            const last_name = formData.get('last_name') as string;
            const password = formData.get('password') as string;

            const resp = await axios.post<UserResponse>('http://localhost:8000/api/login/', {
                username: email,
                password: password,
                first_name: first_name,
                last_name: last_name
            });

            const decoded = jwtDecode<UserResponsePayload>(resp.data.access);

            user.update(() => ({
                id: decoded.user_id,
                access_token: resp.data.access,
                refresh_token: resp.data.refresh
            }));
        } catch {
            user.update(() => null);
        }
    };
</script>

<div>
    <div>
        <p>Login:</p>
        <form on:submit|preventDefault={onLogin}>
            <input type="email" id="email" name="email" value="" placeholder="email" />
            <input type="password" id="password" name="password" value="" placeholder="password" />
            <button>Login</button>
        </form>
    </div>

    <br />

    <p>Register:</p>
    <form on:submit|preventDefault={onRegister}>
        <input type="email" id="email" name="email" value="" placeholder="email" />
        <input type="password" id="password" name="password" value="" placeholder="password" />
        <input type="text" id="first_name" name="name" value="" placeholder="first name" />
        <input type="text" id="last_name" name="name" value="" placeholder="last name" />
        <button>Register</button>
    </form>
</div>
