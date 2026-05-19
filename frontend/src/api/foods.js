import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 10000,
});

export const getFoods = async ({ category, difficulty, tag, skip = 0, limit = 100 } = {}) => {
    const params = {};
    if (category) params.category = category;
    if (difficulty) params.difficulty = difficulty;
    if (tag) params.tag = tag;
    params.skip = skip;
    params.limit = limit;

    const response = await api.get('/api/foods/', { params });
    return response.data;
};

export const getFoodById = async (id) => {
    const response = await api.get(`/api/foods/${id}`);
    return response.data;
};