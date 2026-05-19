import { useEffect, useState } from 'react';
import { getStats } from '../api/stats';
import { FiBookOpen, FiGrid, FiTrendingUp } from 'react-icons/fi';
import { motion } from 'framer-motion';

export default function Dashboard() {
    const [stats, setStats] = useState({ total_recipes: 0, total_categories: 0 });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        getStats()
            .then((res) => setStats(res.data))
            .catch(() => { })
            .finally(() => setLoading(false));
    }, []);

    const cards = [
        {
            title: 'Total Recipes',
            value: stats.total_recipes,
            icon: FiBookOpen,
            gradient: 'from-terracotta to-orange-400',
            iconBg: 'bg-white/20',
        },
        {
            title: 'Categories',
            value: stats.total_categories,
            icon: FiGrid,
            gradient: 'from-deep-green to-leaf',
            iconBg: 'bg-white/20',
        },
    ];

    return (
        <div>
            <motion.h1
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-2xl font-bold text-dark-brown mb-8"
            >
                Dashboard Overview
            </motion.h1>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {cards.map((card, i) => (
                    <motion.div
                        key={card.title}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: i * 0.1 }}
                        className={`rounded-2xl bg-gradient-to-br ${card.gradient} p-6 text-white shadow-xl shadow-terracotta/20`}
                    >
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-white/80 text-sm font-medium">{card.title}</p>
                                <p className="text-4xl font-bold mt-1">
                                    {loading ? '...' : card.value}
                                </p>
                            </div>
                            <div className={`p-4 rounded-xl ${card.iconBg}`}>
                                <card.icon className="text-3xl text-white" />
                            </div>
                        </div>
                    </motion.div>
                ))}
            </div>
        </div>
    );
}