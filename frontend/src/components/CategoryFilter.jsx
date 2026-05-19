import { motion } from 'framer-motion';
import { CATEGORY_MAP } from '../utils/constants';

export default function CategoryFilter({ selected, onSelect }) {
    const categories = Object.entries(CATEGORY_MAP);

    return (
        <div className="flex overflow-x-auto gap-3 pb-2 no-scrollbar">
            <motion.button
                whileTap={{ scale: 0.95 }}
                onClick={() => onSelect('')}
                className={`px-5 py-2 rounded-full font-medium text-sm whitespace-nowrap transition-colors ${selected === '' ? 'bg-terracotta text-white shadow-lg' : 'bg-white/80 backdrop-blur-sm text-dark-brown hover:bg-earth/20'
                    }`}
            >
                All
            </motion.button>
            {categories.map(([key, { label, icon: Icon }]) => (
                <motion.button
                    key={key}
                    whileTap={{ scale: 0.95 }}
                    onClick={() => onSelect(key)}
                    className={`px-5 py-2 rounded-full font-medium text-sm whitespace-nowrap flex items-center gap-2 transition-colors ${selected === key ? 'bg-terracotta text-white shadow-lg' : 'bg-white/80 backdrop-blur-sm text-dark-brown hover:bg-earth/20'
                        }`}
                >
                    <Icon className="text-base" />
                    {label}
                </motion.button>
            ))}
        </div>
    );
}