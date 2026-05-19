import { FaHeart } from 'react-icons/fa';

export default function Layout({ children }) {
    return (
        <div className="min-h-screen bg-cream">
            <header className="bg-white/80 backdrop-blur-md sticky top-0 z-40 shadow-sm">
                <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
                    <a href="/" className="text-2xl font-bold font-['Playfair_Display'] text-terracotta">
                        Yorùbá Recipes
                    </a>
                    <nav className="hidden md:flex space-x-6 text-sm font-medium text-dark-brown">
                        <a href="#hero" className="hover:text-terracotta transition-colors">Home</a>
                        <a href="#recipes-section" className="hover:text-terracotta transition-colors">Recipes</a>
                        <a href="#categories" className="hover:text-terracotta transition-colors">Categories</a>
                    </nav>
                    <FaHeart className="text-terracotta text-xl md:hidden" />
                </div>
            </header>
            <main>{children}</main>
            <footer className="bg-dark-brown text-cream py-8 text-center text-sm">
                <p>© {new Date().getFullYear()} Yorùbá Recipes. All rights reserved.</p>
                <p className="mt-1 opacity-70">Made with ❤️ for Yoruba cuisine.</p>
            </footer>
        </div>
    );
}