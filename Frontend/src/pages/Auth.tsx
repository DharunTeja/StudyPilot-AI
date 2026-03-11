import React, { useState } from 'react';
import { useNavigate, Navigate } from 'react-router-dom';
import { Book, Mail, Lock, User, ArrowRight } from 'lucide-react';
import { useAppContext } from '../context/AppContext';
import api from '../api/api';
import { motion } from 'framer-motion';

const Auth = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [formData, setFormData] = useState({ name: '', email: '', password: '' });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login, isAuthenticated } = useAppContext();
    const navigate = useNavigate();

    if (isAuthenticated) {
        return <Navigate to="/dashboard" replace />;
    }

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            const endpoint = isLogin ? '/auth/login' : '/auth/register';
            const payload = isLogin
                ? { email: formData.email, password: formData.password, name: "" }
                : formData;

            const { data } = await api.post(endpoint, payload);

            login(data.user, data.token);
            navigate('/dashboard');
        } catch (err: any) {
            console.error(err);
            setError(
                err.response?.data?.detail ||
                (isLogin ? 'Invalid credentials' : 'Registration failed. Please try again.')
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex text-gray-900 bg-white">
            <div className="w-full lg:w-1/2 flex flex-col justify-center px-8 sm:px-16 md:px-24">
                <div className="max-w-md w-full mx-auto">
                    <div className="flex items-center mb-8">
                        <Book className="w-10 h-10 text-primary-600 mr-3" />
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary-600 to-primary-400">
                            StudyPilot AI
                        </h1>
                    </div>

                    <h2 className="text-3xl font-bold mb-2">
                        {isLogin ? 'Welcome back' : 'Create an account'}
                    </h2>
                    <p className="text-gray-500 mb-8">
                        {isLogin
                            ? 'Enter your details to access your smart study assistant.'
                            : 'Join us and transform your learning experience.'}
                    </p>

                    {error && (
                        <div className="bg-red-50 text-red-600 p-4 rounded-xl mb-6 text-sm border border-red-100 flex items-center">
                            <span className="font-medium mr-2">Error:</span> {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        {!isLogin && (
                            <div>
                                <label className="block text-sm font-medium text-gray-700 mb-1.5">Full Name</label>
                                <div className="relative">
                                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                        <User className="h-5 w-5 text-gray-400" />
                                    </div>
                                    <input
                                        type="text"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        required
                                        className="block w-full pl-10 pr-3 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors bg-gray-50 focus:bg-white"
                                        placeholder="John Doe"
                                    />
                                </div>
                            </div>
                        )}

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1.5">Email Address</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Mail className="h-5 w-5 text-gray-400" />
                                </div>
                                <input
                                    type="email"
                                    name="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                    className="block w-full pl-10 pr-3 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors bg-gray-50 focus:bg-white"
                                    placeholder="you@example.com"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1.5">Password</label>
                            <div className="relative">
                                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                    <Lock className="h-5 w-5 text-gray-400" />
                                </div>
                                <input
                                    type="password"
                                    name="password"
                                    value={formData.password}
                                    onChange={handleChange}
                                    required
                                    className="block w-full pl-10 pr-3 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors bg-gray-50 focus:bg-white"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <button
                            type="submit"
                            disabled={loading}
                            className="w-full flex items-center justify-center btn-primary py-3 rounded-xl mt-6 group bg-primary-600 hover:bg-primary-700 text-white transition-colors"
                        >
                            {loading
                                ? 'Please wait...'
                                : <>{isLogin ? 'Sign In' : 'Sign Up'} <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" /></>
                            }
                        </button>
                    </form>

                    <p className="mt-8 text-center text-sm text-gray-600">
                        {isLogin ? "Don't have an account? " : "Already have an account? "}
                        <button
                            onClick={() => {
                                setIsLogin(!isLogin);
                                setError('');
                            }}
                            className="font-semibold text-primary-600 hover:text-primary-700 transition-colors"
                        >
                            {isLogin ? 'Sign up' : 'Sign in'}
                        </button>
                    </p>
                </div>
            </div>

            <div className="hidden lg:flex w-1/2 bg-primary-50 p-12">
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.5 }}
                    className="w-full h-full bg-primary-600 rounded-3xl p-12 text-white flex flex-col justify-center relative overflow-hidden"
                >
                    <div className="absolute -top-24 -right-24 w-96 h-96 bg-primary-500 rounded-full blur-3xl opacity-50"></div>
                    <div className="absolute -bottom-24 -left-24 w-96 h-96 bg-primary-700 rounded-full blur-3xl opacity-50"></div>

                    <div className="relative z-10">
                        <h2 className="text-4xl font-bold mb-6">Learn Smarter,<br />Not Harder</h2>
                        <p className="text-primary-100 text-lg mb-8 max-w-md">
                            StudyPilot AI transforms your raw study notes, PDFs, and lectures into interactive quizzes, structured summaries, and personalized study plans.
                        </p>

                        <div className="space-y-4">
                            {['AI Summarization', 'Flashcard Generation', 'Adaptive Quizzes'].map((feature, i) => (
                                <div key={i} className="flex items-center text-primary-100">
                                    <div className="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center mr-4">
                                        <Book className="w-4 h-4 text-white" />
                                    </div>
                                    {feature}
                                </div>
                            ))}
                        </div>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default Auth;
