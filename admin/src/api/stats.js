import api from './axios';
export const getStats = () => api.get('/api/stats/');