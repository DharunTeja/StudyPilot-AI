import React from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { BookOpen, Home, PieChart, LogOut, Upload, Menu, X, Book } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import { motion, AnimatePresence } from 'framer-motion';

const Layout = () => {
    const { user, logout } = useAppContext();
    const navigate = useNavigate();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

    const handleLogout = () => {
        logout();
        navigate('/auth');
    };

    const navItems = [
        { name: 'Dashboard', icon: Home, path: '/dashboard' },
        { name: 'Materials', icon: BookOpen, path: '/materials' },
        { name: 'Upload', icon: Upload, path: '/upload' },
        { name: 'Analytics', icon: PieChart, path: '/analytics' },
    ];

    return (
        <div className="flex h-screen bg-gray-50 overflow-hidden">
            <aside className="hidden md:flex flex-col w-64 bg-white border-r border-gray-200">
                <div className="flex items-center justify-center h-16 border-b border-gray-200 px-6">
                    <Book className="w-8 h-8 text-primary-600 mr-2" />
                    <span className="text-xl font-bold text-gray-800">StudyPilot AI</span>
                </div>

                <nav className="flex-1 overflow-y-auto py-4">
                    <ul className="space-y-1 px-3">
                        {navItems.map((item) => (
                            <li key={item.name}>
                                <NavLink
                                    to={item.path}
                                    className={({ isActive }) =>
                                        `flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${isActive
                                            ? 'bg-primary-50 text-primary-700'
                                            : 'text-gray-700 hover:bg-gray-100'
                                        }`
                                    }
                                >
                                    <item.icon className="w-5 h-5 mr-3 flex-shrink-0" />
                                    {item.name}
                                </NavLink>
                            </li>
                        ))}
                    </ul>
                </nav>

                <div className="p-4 border-t border-gray-200">
                    <div className="flex items-center mb-4 px-3">
                        <div className="w-8 h-8 rounded-full bg-primary-100 text-primary-700 flex items-center justify-center font-bold mr-3 flex-shrink-0">
                            {user?.name?.charAt(0) || 'U'}
                        </div>
                        <div className="overflow-hidden">
                            <p className="text-sm font-medium text-gray-900 truncate">{user?.name || 'User'}</p>
                            <p className="text-xs text-gray-500 truncate">{user?.email}</p>
                        </div>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="flex items-center w-full px-3 py-2 text-sm font-medium text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                    >
                        <LogOut className="w-5 h-5 mr-3 flex-shrink-0" />
                        Logout
                    </button>
                </div>
            </aside>

            <div className="flex-1 flex flex-col min-w-0">
                <header className="md:hidden flex items-center justify-between h-16 px-4 bg-white border-b border-gray-200">
                    <div className="flex items-center">
                        <Book className="w-6 h-6 text-primary-600 mr-2" />
                        <span className="text-lg font-bold text-gray-800">StudyPilot AI</span>
                    </div>
                    <button
                        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                        className="p-2 text-gray-500 hover:text-gray-700 focus:outline-none"
                    >
                        {isMobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                    </button>
                </header>

                <AnimatePresence>
                    {isMobileMenuOpen && (
                        <motion.div
                            initial={{ x: '-100%' }}
                            animate={{ x: 0 }}
                            exit={{ x: '-100%' }}
                            transition={{ type: 'tween', duration: 0.3 }}
                            className="fixed inset-0 z-40 flex md:hidden"
                        >
                            <div className="fixed inset-0 bg-black/20" onClick={() => setIsMobileMenuOpen(false)}></div>
                            <aside className="relative flex flex-col w-64 max-w-xs bg-white h-full shadow-xl">
                                <div className="flex items-center justify-between h-16 px-6 border-b border-gray-200">
                                    <span className="text-xl font-bold text-gray-800">Menu</span>
                                    <button onClick={() => setIsMobileMenuOpen(false)}>
                                        <X className="w-6 h-6 text-gray-500" />
                                    </button>
                                </div>
                                <nav className="flex-1 py-4 overflow-y-auto">
                                    <ul className="space-y-1 px-3">
                                        {navItems.map((item) => (
                                            <li key={item.name}>
                                                <NavLink
                                                    to={item.path}
                                                    onClick={() => setIsMobileMenuOpen(false)}
                                                    className={({ isActive }) =>
                                                        `flex items-center px-3 py-2.5 text-sm font-medium rounded-lg transition-colors ${isActive
                                                            ? 'bg-primary-50 text-primary-700'
                                                            : 'text-gray-700 hover:bg-gray-100'
                                                        }`
                                                    }
                                                >
                                                    <item.icon className="w-5 h-5 mr-3" />
                                                    {item.name}
                                                </NavLink>
                                            </li>
                                        ))}
                                    </ul>
                                </nav>
                                <div className="p-4 border-t border-gray-200">
                                    <button
                                        onClick={handleLogout}
                                        className="flex items-center w-full px-3 py-2 text-sm font-medium text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                                    >
                                        <LogOut className="w-5 h-5 mr-3" />
                                        Logout
                                    </button>
                                </div>
                            </aside>
                        </motion.div>
                    )}
                </AnimatePresence>

                <main className="flex-1 overflow-auto bg-gray-50 p-4 md:p-8">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default Layout;
