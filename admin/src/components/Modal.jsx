import { useEffect, useRef } from 'react';
import { FiX } from 'react-icons/fi';
import { motion, AnimatePresence } from 'framer-motion';

export default function Modal({ children, onClose }) {
    const overlayRef = useRef();

    useEffect(() => {
        const handleEscape = (e) => { if (e.key === 'Escape') onClose(); };
        document.addEventListener('keydown', handleEscape);
        document.body.style.overflow = 'hidden';
        return () => {
            document.removeEventListener('keydown', handleEscape);
            document.body.style.overflow = '';
        };
    }, [onClose]);

    const handleOverlayClick = (e) => {
        if (e.target === overlayRef.current) onClose();
    };

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                ref={overlayRef}
                onClick={handleOverlayClick}
                className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4"
            >
                <motion.div
                    initial={{ scale: 0.95, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    exit={{ scale: 0.95, opacity: 0 }}
                    className="bg-white rounded-2xl shadow-2xl w-full max-w-lg relative overflow-y-auto max-h-[90vh]"
                >
                    <button onClick={onClose} className="absolute top-4 right-4 p-1 text-gray-400 hover:text-gray-600 z-10">
                        <FiX className="text-xl" />
                    </button>
                    {children}
                </motion.div>
            </motion.div>
        </AnimatePresence>
    );
}