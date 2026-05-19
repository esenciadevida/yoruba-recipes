import { motion, AnimatePresence } from 'framer-motion';
import { useFoodDetail } from '../hooks/useFoodDetail';
import LoadingSpinner from './LoadingSpinner';
import ErrorMessage from './ErrorMessage';
import { FaTimes, FaClock, FaFire, FaLeaf } from 'react-icons/fa';

export default function RecipeModal({ foodId, onClose }) {
    const { food, loading, error } = useFoodDetail(foodId);

    return (
        <AnimatePresence>
            {foodId && (
                <motion.div
                    className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                >
                    <motion.div
                        className="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto relative"
                        initial={{ scale: 0.9, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.9, opacity: 0 }}
                        onClick={(e) => e.stopPropagation()}
                    >
                        <button
                            onClick={onClose}
                            className="absolute top-4 right-4 p-2 bg-white/80 backdrop-blur-sm rounded-full shadow hover:bg-white transition-colors z-10"
                        >
                            <FaTimes className="text-dark-brown" />
                        </button>

                        {loading && <LoadingSpinner />}
                        {error && <ErrorMessage message={error} retry={() => window.location.reload()} />}

                        {food && (
                            <div>
                                <div className="h-64 bg-gradient-to-br from-cream to-earth/20 flex items-center justify-center text-8xl">
                                    🍲
                                </div>
                                <div className="p-6">
                                    <h2 className="text-3xl font-bold font-['Playfair_Display'] text-dark-brown">{food.name}</h2>
                                    <p className="text-xl text-earth mt-1">{food.local_name}</p>
                                    <p className="text-sm text-gray-500 mt-1">{food.origin}</p>

                                    <div className="flex flex-wrap gap-2 mt-4">
                                        {food.tags.map((tag) => (
                                            <span key={tag} className="px-3 py-1 bg-cream rounded-full text-xs font-medium text-dark-brown">
                                                #{tag}
                                            </span>
                                        ))}
                                    </div>

                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-6">
                                        <div className="bg-leaf/10 p-3 rounded-lg text-center">
                                            <FaFire className="mx-auto text-leaf mb-1" />
                                            <span className="text-sm font-bold text-dark-brown">{food.calories}</span>
                                            <p className="text-xs text-gray-500">Calories</p>
                                        </div>
                                        <div className="bg-terracotta/10 p-3 rounded-lg text-center">
                                            <FaClock className="mx-auto text-terracotta mb-1" />
                                            <span className="text-sm font-bold text-dark-brown">{food.protein}g</span>
                                            <p className="text-xs text-gray-500">Protein</p>
                                        </div>
                                        <div className="bg-gold/10 p-3 rounded-lg text-center">
                                            <FaLeaf className="mx-auto text-gold mb-1" />
                                            <span className="text-sm font-bold text-dark-brown">{food.fiber}g</span>
                                            <p className="text-xs text-gray-500">Fiber</p>
                                        </div>
                                        <div className="bg-earth/10 p-3 rounded-lg text-center">
                                            <span className="text-lg font-bold text-dark-brown">{food.glycemic_index}</span>
                                            <p className="text-xs text-gray-500">GI</p>
                                        </div>
                                    </div>

                                    <div className="mt-6">
                                        <h3 className="text-xl font-semibold text-dark-brown">Ingredients</h3>
                                        <ul className="mt-2 space-y-1">
                                            {food.ingredients.map((ing, i) => (
                                                <li key={i} className="flex justify-between text-sm py-1 border-b border-gray-100 last:border-0">
                                                    <span>{ing.name}</span>
                                                    <span className="font-medium">{ing.quantity}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>

                                    <div className="mt-6">
                                        <h3 className="text-xl font-semibold text-dark-brown">Health Benefits</h3>
                                        <ul className="mt-2 list-disc list-inside text-sm text-gray-700">
                                            {food.health_benefits.map((b, i) => (
                                                <li key={i}>{b}</li>
                                            ))}
                                        </ul>
                                    </div>

                                    <div className="mt-6 flex items-center gap-4 text-sm text-gray-500">
                                        <span className="capitalize">Difficulty: <strong>{food.difficulty}</strong></span>
                                        <span>Portion: <strong>{food.recommended_portion}</strong></span>
                                    </div>
                                </div>
                            </div>
                        )}
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
}