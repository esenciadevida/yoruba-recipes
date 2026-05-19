import { NavLink } from 'react-router-dom';
import { FiHome, FiBookOpen, FiGrid, FiLogOut, FiMenu, FiX } from 'react-icons/fi';
import { useAuth } from '../../context/AuthContext';
import { useState } from 'react';

const links = [
    { to: '/', icon: FiHome, label: 'Dashboard' },
    { to: '/recipes', icon: FiBookOpen, label: 'Recipes' },
    { to: '/categories', icon: FiGrid, label: 'Categories' },
];

export default function Sidebar() {
    const { logout } = useAuth();
    const [mobileOpen, setMobileOpen] = useState(false);

    return (
        <>
            {/* Mobile toggle */}
            <button
                className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-dark-brown text-white rounded-md"
                onClick={() => setMobileOpen(!mobileOpen)}
            >
                {mobileOpen ? <FiX className="text-xl" /> : <FiMenu className="text-xl" />}
            </button>

            {/* Overlay */}
            {mobileOpen && (
                <div
                    className="lg:hidden fixed inset-0 z-30 bg-black/50 backdrop-blur-sm"
                    onClick={() => setMobileOpen(false)}
                />
            )}

            <aside
                className={`fixed top-0 left-0 z-40 h-full w-64 bg-dark-brown text-white transform transition-transform duration-300 lg:translate-x-0 ${mobileOpen ? 'translate-x-0' : '-translate-x-full'
                    } lg:static lg:z-0`}
            >
                <div className="h-16 flex items-center px-6 border-b border-white/10">
                    <span className="text-xl font-bold text-gold">Yorùbá Admin</span>
                </div>
                <nav className="flex flex-col flex-1 mt-6 px-3">
                    <div className="space-y-1 flex-1">
                        {links.map((link) => (
                            <NavLink
                                key={link.to}
                                to={link.to}
                                end={link.to === '/'}
                                onClick={() => setMobileOpen(false)}
                                className={({ isActive }) =>
                                    `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all duration-200 ${isActive
                                        ? 'bg-terracotta text-white shadow-lg shadow-terracotta/30'
                                        : 'text-gray-300 hover:bg-white/10 hover:text-white'
                                    }`
                                }
                            >
                                <link.icon className="text-lg" />
                                {link.label}
                            </NavLink>
                        ))}
                    </div>
                    {/* Logout at the bottom */}
                    <button
                        onClick={logout}
                        className="flex items-center gap-3 w-full px-4 py-3 text-sm text-gray-300 hover:bg-white/10 rounded-lg transition-colors mt-4 mb-6"
                    >
                        <FiLogOut className="text-lg" />
                        Logout
                    </button>
                </nav>
            </aside>
        </>
    );
}