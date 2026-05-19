import { motion } from 'framer-motion';
import RecipeCard from './RecipeCard';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';

export default function RecipeGrid({ foods, loading, loadingMore, error, onRetry, onFoodClick, favorites, onToggleFavorite }) {
    if (error) {
        return <ErrorMessage message={error} retry={onRetry} />;
    }

    if (loading && foods.length === 0) {
        return <LoadingSpinner />;
    }

    if (!loading && foods.length === 0) {
        return (
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center py-16 text-earth text-lg"
            >
                No recipes found. Try a different search or filter.
            </motion.div>
        );
    }

    return (
        <>
            <motion.div
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
                initial="hidden"
                animate="visible"
                variants={{
                    hidden: { opacity: 0 },
                    visible: {
                        opacity: 1,
                        transition: { staggerChildren: 0.1 },
                    },
                }}
            >
                {foods.map((food) => (
                    <motion.div
                        key={food.id}
                        variants={{
                            hidden: { opacity: 0, y: 20 },
                            visible: { opacity: 1, y: 0 },
                        }}
                    >
                        <RecipeCard
                            food={food}
                            onClick={onFoodClick}
                            isFavorite={favorites.includes(food.id)}
                            onToggleFavorite={onToggleFavorite}
                        />
                    </motion.div>
                ))}
            </motion.div>
            {loadingMore && <LoadingSpinner />}
        </>
    );
}