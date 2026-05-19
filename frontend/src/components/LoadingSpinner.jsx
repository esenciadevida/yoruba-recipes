import { motion } from 'framer-motion';

export default function LoadingSpinner() {
    return (
        <motion.div
            className="flex justify-center py-12"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
        >
            <div className="w-10 h-10 border-4 border-earth border-t-terracotta rounded-full animate-spin" />
        </motion.div>
    );
}