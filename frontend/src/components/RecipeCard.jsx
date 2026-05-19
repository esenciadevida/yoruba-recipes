import { motion } from 'framer-motion';
import { FaHeart, FaRegHeart } from 'react-icons/fa';
import { useState } from 'react';

const categoryColors = {
    soup: 'bg-leaf/20 text-leaf',
    swallow: 'bg-earth/20 text-earth',
    base: 'bg-gold/20 text-dark-brown',
    side: 'bg-terracotta/20 text-terracotta',
};

export default function RecipeCard({ food, onClick, isFavorite, onToggleFavorite }) {
    const [imgError, setImgError] = useState(true);

    // Placeholder image based on category
    const getPlaceholderEmoji = () => {
        const map = { soup: '🥘', swallow: '🍚', base: '🍲', side: '🍤' };
        return map[food.category] || '🍽️';
    };

    return (
        <motion.div
            whileHover={{ y: -6, boxShadow: '0 20px 30px -10px rgba(0,0,0,0.15)' }}
            className="bg-white rounded-2xl overflow-hidden shadow-md cursor-pointer group"
            onClick={() => onClick(food)}
            layout
        >
            <div className="h-48 bg-cream relative overflow-hidden">
                {imgError ? (
                    <div className="w-full h-full flex items-center justify-center text-6xl bg-gradient-to-br from-cream to-earth/20">
                        {getPlaceholderEmoji()}
                    </div>
                ) : (
                    <img
                        src={food.image_url || `https://source.unsplash.com/400x300/?yoruba,food&sig=${food.id}`}
                        alt={food.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                        onError={() => setImgError(true)}
                    />
                )}
                <div className="absolute top-3 right-3">
                    <button
                        onClick={(e) => {
                            e.stopPropagation();
                            onToggleFavorite(food.id);
                        }}
                        className="p-2 bg-white/80 backdrop-blur-sm rounded-full shadow-md hover:bg-white transition-colors"
                    >
                        {isFavorite ? (
                            <FaHeart className="text-terracotta" />
                        ) : (
                            <FaRegHeart className="text-dark-brown/60" />
                        )}
                    </button>
                </div>
                <div className="absolute bottom-3 left-3">
                    <span
                        className={`px-3 py-1 rounded-full text-xs font-semibold backdrop-blur-sm ${categoryColors[food.category] || 'bg-gray-100 text-gray-600'
                            }`}
                    >
                        {food.category}
                    </span>
                </div>
            </div>
            <div className="p-4">
                <h3 className="font-bold text-dark-brown text-lg truncate">{food.name}</h3>
                <p className="text-earth text-sm mt-1">{food.local_name}</p>
                <div className="flex justify-between items-center mt-3 text-sm text-gray-500">
                    <span>🔥 {food.calories} kcal</span>
                    <span className="capitalize">📊 {food.difficulty}</span>
                </div>
            </div>
        </motion.div>
    );
}