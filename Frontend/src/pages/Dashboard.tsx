import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { BookOpen, Flame, Trophy, Clock, ArrowRight, BrainCircuit } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../api/api';
import { useAppContext } from '../context/AppContext';

interface Stats {
    total_materials: number;
    total_quizzes: number;
    average_score: number;
    total_study_time: number;
    study_streak: number;
    weak_topics: string[];
    strong_topics: string[];
    recommendations: string[];
    recent_activities: any[];
}

const Dashboard = () => {
    const { user } = useAppContext();
    const navigate = useNavigate();
    const [stats, setStats] = useState<Stats | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const { data } = await api.get('/progress/stats');
                setStats(data);
            } catch (err) {
                console.error("Failed to fetch stats", err);
            } finally {
                setLoading(false);
            }
        };
        fetchStats();
    }, []);

    if (loading) {
        return (
            <div className="flex justify-center items-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    const StatCard = ({ title, value, icon: Icon, colorClass, delay }: any) => (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay }}
            className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100 flex items-center hover:shadow-md transition-shadow"
        >
            <div className={`p-4 rounded-xl ${colorClass} mr-5`}>
                <Icon className="w-6 h-6" />
            </div>
            <div>
                <h3 className="text-gray-500 text-sm font-medium mb-1">{title}</h3>
                <p className="text-2xl font-bold text-gray-900">{value}</p>
            </div>
        </motion.div>
    );

    return (
        <div className="max-w-7xl mx-auto space-y-8 pb-12">
            <div className="flex justify-between items-end">
                <div>
                    <motion.h1
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="text-3xl font-bold text-gray-900 mb-2"
                    >
                        Welcome back, {user?.name?.split(' ')[0] || 'Scholar'}! 👋
                    </motion.h1>
                    <p className="text-gray-500">Here's an overview of your learning journey today.</p>
                </div>
                <Link
                    to="/upload"
                    className="bg-primary-600 hover:bg-primary-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors shadow-sm shadow-primary-200 flex items-center"
                >
                    <BookOpen className="w-5 h-5 mr-2" />
                    New Material
                </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatCard
                    title="Current Streak"
                    value={`${stats?.study_streak || 0} Days`}
                    icon={Flame}
                    colorClass="bg-orange-100 text-orange-600"
                    delay={0.1}
                />
                <StatCard
                    title="Materials Uploaded"
                    value={stats?.total_materials || 0}
                    icon={BookOpen}
                    colorClass="bg-blue-100 text-blue-600"
                    delay={0.2}
                />
                <StatCard
                    title="Avg Quiz Score"
                    value={`${stats?.average_score || 0}%`}
                    icon={Trophy}
                    colorClass="bg-yellow-100 text-yellow-600"
                    delay={0.3}
                />
                <StatCard
                    title="Study Time (Mins)"
                    value={stats?.total_study_time || 0}
                    icon={Clock}
                    colorClass="bg-primary-100 text-primary-600"
                    delay={0.4}
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                    className="col-span-1 lg:col-span-2 bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8"
                >
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-xl font-bold text-gray-900 flex items-center">
                            <BrainCircuit className="w-6 h-6 mr-2 text-primary-600" />
                            AI Recommendations
                        </h2>
                    </div>

                    {stats?.recommendations && stats.recommendations.length > 0 ? (
                        <ul className="space-y-4">
                            {stats.recommendations.map((rec, i) => (
                                <li key={i} className="flex items-start bg-gray-50 p-4 rounded-xl">
                                    <div className="bg-primary-100 w-8 h-8 rounded-full flex items-center justify-center text-primary-700 font-bold mr-4 flex-shrink-0">
                                        {i + 1}
                                    </div>
                                    <p className="text-gray-700 pt-1 text-sm md:text-base">{rec}</p>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <div className="text-center py-10">
                            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                                <BrainCircuit className="w-8 h-8 text-gray-400" />
                            </div>
                            <h3 className="text-lg font-medium text-gray-900 mb-2">Not enough data yet</h3>
                            <p className="text-gray-500 max-w-sm mx-auto">
                                Upload more materials and take quizzes for our AI engine to generate personalized study recommendations!
                            </p>
                        </div>
                    )}
                </motion.div>

                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.6 }}
                    className="col-span-1 bg-gradient-to-b from-primary-600 to-primary-800 rounded-2xl shadow-sm p-8 text-white relative overflow-hidden flex flex-col justify-center"
                >
                    <div className="absolute top-0 right-0 w-32 h-32 bg-white opacity-5 rounded-full -mr-10 -mt-10"></div>
                    <div className="absolute bottom-0 left-0 w-40 h-40 bg-white opacity-5 rounded-full -ml-10 -mb-10"></div>

                    <div className="relative z-10">
                        <h2 className="text-2xl font-bold mb-3">Ready to learn?</h2>
                        <p className="text-primary-100 mb-8">
                            Transform your raw notes into interactive quizzes and summaries in seconds.
                        </p>
                        <button
                            onClick={() => navigate('/upload')}
                            className="w-full bg-white text-primary-700 font-bold py-3 rounded-xl hover:bg-primary-50 transition-colors shadow-lg flex items-center justify-center group"
                        >
                            Start Uploading
                            <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
                        </button>
                    </div>
                </motion.div>
            </div>
        </div>
    );
};

export default Dashboard;
