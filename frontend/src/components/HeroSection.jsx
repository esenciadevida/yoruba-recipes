import { motion } from 'framer-motion';
import SearchBar from './SearchBar';

export default function HeroSection({ onSearch }) {
    return (
        <section className="relative min-h-[70vh] flex items-center justify-center overflow-hidden bg-gradient-to-br from-cream via-earth/20 to-terracotta/10">
            {/* Decorative background shapes */}
            <div className="absolute top-10 left-10 w-72 h-72 bg-gold/20 rounded-full blur-3xl" />
            <div className="absolute bottom-10 right-10 w-96 h-96 bg-terracotta/20 rounded-full blur-3xl" />

            <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, ease: 'easeOut' }}
                className="relative z-10 text-center px-4 max-w-3xl"
            >
                <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold font-['Playfair_Display'] text-dark-brown leading-tight">
                    Discover the <span className="text-terracotta">Rich</span> Flavors of Yoruba Cuisine
                </h1>
                <p className="mt-6 text-lg md:text-xl text-earth/90 max-w-2xl mx-auto">
                    A curated collection of authentic Yoruba recipes, from timeless soups to modern street‑food favourites.
                </p>
                <div className="mt-8">
                    <SearchBar value="" onChange={onSearch} />
                </div>
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => document.getElementById('recipes-section')?.scrollIntoView({ behavior: 'smooth' })}
                    className="mt-6 px-8 py-3 bg-terracotta text-white font-semibold rounded-full shadow-lg hover:bg-terracotta/90 transition-colors"
                >
                    Explore Recipes
                </motion.button>
            </motion.div>
        </section>
    );
}