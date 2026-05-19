import { useState, useEffect } from 'react';
import Layout from './components/Layout';
import HeroSection from './components/HeroSection';
import CategoryFilter from './components/CategoryFilter';
import RecipeGrid from './components/RecipeGrid';
import RecipeModal from './components/RecipeModal';
import { useFoods } from './hooks/useFoods';
import { motion } from 'framer-motion';

function App() {
  const [selectedFoodId, setSelectedFoodId] = useState(null);
  const { foods, loading, loadingMore, error, filters, updateFilters, loadMore, hasMore } = useFoods();
  const [favorites, setFavorites] = useState(() => {
    const saved = localStorage.getItem('favorites');
    return saved ? JSON.parse(saved) : [];
  });

  useEffect(() => {
    localStorage.setItem('favorites', JSON.stringify(favorites));
  }, [favorites]);

  const handleSearch = (search) => {
    updateFilters({ search });
  };

  const handleCategorySelect = (category) => {
    updateFilters({ category });
  };

  const toggleFavorite = (id) => {
    setFavorites((prev) =>
      prev.includes(id) ? prev.filter((f) => f !== id) : [...prev, id]
    );
  };

  const handleFoodClick = (food) => {
    setSelectedFoodId(food.id);
  };

  return (
    <Layout>
      <HeroSection onSearch={handleSearch} />

      <section id="categories" className="max-w-7xl mx-auto px-4 py-12">
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-3xl md:text-4xl font-['Playfair_Display'] font-bold text-dark-brown text-center mb-8"
        >
          Browse by Category
        </motion.h2>
        <CategoryFilter selected={filters.category} onSelect={handleCategorySelect} />
      </section>

      <section id="recipes-section" className="max-w-7xl mx-auto px-4 py-8">
        <motion.h2
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="text-3xl md:text-4xl font-['Playfair_Display'] font-bold text-dark-brown text-center mb-8"
        >
          Our Recipes
        </motion.h2>
        <RecipeGrid
          foods={foods}
          loading={loading}
          loadingMore={loadingMore}
          error={error}
          onRetry={() => updateFilters({})}
          onFoodClick={handleFoodClick}
          favorites={favorites}
          onToggleFavorite={toggleFavorite}
        />
        {hasMore && foods.length > 0 && (
          <div className="text-center mt-8">
            <button
              onClick={loadMore}
              disabled={loadingMore}
              className="px-8 py-3 bg-earth text-white font-semibold rounded-full shadow hover:bg-earth/90 transition-colors disabled:opacity-50"
            >
              {loadingMore ? 'Loading...' : 'Load More'}
            </button>
          </div>
        )}
      </section>

      <RecipeModal foodId={selectedFoodId} onClose={() => setSelectedFoodId(null)} />
    </Layout>
  );
}

export default App;