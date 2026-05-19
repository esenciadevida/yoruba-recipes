import api from './axios';

export const getRecipes = async (params) => {
  const response = await api.get('/api/foods/', { params });
  const total = parseInt(response.headers['x-total-count'], 10) || 0;
  return { data: response.data, total };
};
export const getRecipe = (id) => api.get(`/api/foods/${id}`);
export const createRecipe = (data) => api.post('/api/foods/', data);
export const updateRecipe = (id, data) => api.put(`/api/foods/${id}`, data);
export const deleteRecipe = (id) => api.delete(`/api/foods/${id}`);