import { useState, useEffect } from 'react';
import { getFoodById } from '../api/foods';

export function useFoodDetail(id) {
    const [food, setFood] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!id) {
            setFood(null);
            return;
        }
        setLoading(true);
        getFoodById(id)
            .then((data) => {
                setFood(data);
                setError(null);
            })
            .catch((err) => setError(err.response?.data?.detail || err.message))
            .finally(() => setLoading(false));
    }, [id]);

    return { food, loading, error };
}