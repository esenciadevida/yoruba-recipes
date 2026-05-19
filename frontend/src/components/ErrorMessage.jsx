import { motion } from 'framer-motion';
import { BiErrorCircle } from 'react-icons/bi';

export default function ErrorMessage({ message, retry }) {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-red-50 border border-red-200 text-red-800 px-6 py-4 rounded-lg flex items-center gap-3 max-w-md mx-auto my-8"
        >
            <BiErrorCircle className="text-2xl" />
            <span>{message || 'Something went wrong.'}</span>
            {retry && (
                <button onClick={retry} className="ml-auto font-medium underline">
                    Retry
                </button>
            )}
        </motion.div>
    );
}