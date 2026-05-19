import { useState, useEffect, useCallback } from 'react';
import { getFoods } from '../api/foods';

export function useFoods() {
    const [foods, setFoods] = useState([]);
    const [loading, setLoading] = useState(true);
    const [loadingMore, setLoadingMore] = useState(false);
    const [error, setError] = useState(null);
    const [filters, setFilters] = useState({
        category: '',
        difficulty: '',
        search: '',
        skip: 0,
        limit: 20,
    });
    const [hasMore, setHasMore] = useState(true);

    // Fetch foods for the current filters (replace list)
    const fetchFoods = useCallback(async (options = {}) => {
        const { append = false } = options;
        if (append) {
            setLoadingMore(true);
        } else {
            setLoading(true);
        }
        setError(null);

        try {
            const data = await getFoods({
                category: filters.category || undefined,
                difficulty: filters.difficulty || undefined,
                skip: filters.skip,
                limit: filters.limit,
            });

            // Client‑side search filter
            let filtered = data;
            if (filters.search) {
                const searchLower = filters.search.toLowerCase();
                filtered = data.filter(
                    (f) =>
                        f.name.toLowerCase().includes(searchLower) ||
                        f.local_name.toLowerCase().includes(searchLower)
                );
            }

            // If appending, merge with previous foods
            setFoods((prev) => (append ? [...prev, ...filtered] : filtered));

            // Determine if more pages exist
            if (filtered.length < filters.limit) {
                setHasMore(false);
            } else {
                setHasMore(true);
            }
        } catch (err) {
            setError(err.response?.data?.detail || err.message);
        } finally {
            setLoading(false);
            setLoadingMore(false);
        }
    }, [filters]);

    // Refetch whenever filters change (except skip)
    useEffect(() => {
        fetchFoods({ append: false });
    }, [filters.category, filters.difficulty, filters.search]);

    // When filters.reset triggers a new category/search, reset skip and reload
    const updateFilters = (newFilters) => {
        setFilters((prev) => ({ ...prev, ...newFilters, skip: 0 }));
        setHasMore(true);
    };

    const loadMore = () => {
        if (!hasMore || loadingMore) return;
        const newSkip = filters.skip + filters.limit;
        setFilters((prev) => ({ ...prev, skip: newSkip }));
        // The skip change will trigger fetchFoods in a separate useEffect,
        // but we need to call fetchFoods with append: true.
        // Instead, we'll handle it in a useEffect that watches skip.
    };

    // Watch for skip changes (for loadMore)
    useEffect(() => {
        // Only run if skip > 0 (initial load is already handled)
        if (filters.skip > 0) {
            fetchFoods({ append: true });
        }
    }, [filters.skip]);

    return { foods, loading, loadingMore, error, filters, updateFilters, loadMore, hasMore };
}