import api from './axios';

export const login = (username, password) =>
    api.post('/api/auth/login', new URLSearchParams({ username, password }), {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });

export const getMe = () => api.get('/api/auth/me');