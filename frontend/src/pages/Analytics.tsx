import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Target, TrendingUp, TrendingDown, Clock, Activity, AlertCircle, CheckCircle } from 'lucide-react';
import api from '../api/api';

const Analytics = () => {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                const { data } = await api.get('/progress/stats');
                setStats(data);
            } catch (err) {
                console.error("Failed to fetch analytics", err);
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

    return (
        <div className="max-w-7xl mx-auto pb-12">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Detailed Analytics</h1>
                <p className="text-gray-500">Dive deep into your learning patterns and AI recommendations.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 flex flex-col items-center justify-center text-center relative overflow-hidden"
                >
                    <div className="absolute top-0 right-0 p-4">
                        <TrendingUp className="w-8 h-8 text-green-200" />
                    </div>
                    <h3 className="text-lg font-medium text-gray-500 mb-2">Overall Accuracy</h3>
                    <div className="relative">
                        <svg className="w-32 h-32 transform -rotate-90">
                            <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-gray-100" />
                            <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="8" fill="transparent"
                                strokeDasharray={`${(stats?.average_score || 0) * 3.77} 400`}
                                strokeLinecap="round"
                                className={`${stats?.average_score > 70 ? 'text-primary-500' : stats?.average_score > 40 ? 'text-yellow-500' : 'text-red-500'}`}
                            />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center flex-col">
                            <span className="text-3xl font-bold text-gray-900">{stats?.average_score || 0}%</span>
                        </div>
                    </div>
                    <p className="text-gray-600 mt-4 max-w-xs mx-auto text-sm">Based on your performance across {stats?.total_quizzes} quizzes</p>
                </motion.div>

                <div className="grid grid-cols-1 gap-4">
                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1 }}
                        className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-row items-center"
                    >
                        <div className="w-14 h-14 bg-red-50 text-red-500 rounded-full flex items-center justify-center mr-6 flex-shrink-0">
                            <AlertCircle className="w-7 h-7" />
                        </div>
                        <div className="flex-1">
                            <h3 className="text-base font-medium text-gray-500 mb-1">Topics to Review</h3>
                            {stats?.weak_topics?.length > 0 ? (
                                <div className="flex flex-wrap gap-2">
                                    {stats.weak_topics.map((t: string) => (
                                        <span key={t} className="px-3 py-1 bg-red-100 text-red-700 text-sm rounded-full font-medium">{t}</span>
                                    ))}
                                </div>
                            ) : (
                                <span className="text-gray-900 font-semibold text-lg">None detected yet!</span>
                            )}
                        </div>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2 }}
                        className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 flex flex-row items-center"
                    >
                        <div className="w-14 h-14 bg-green-50 text-green-500 rounded-full flex items-center justify-center mr-6 flex-shrink-0">
                            <CheckCircle className="w-7 h-7" />
                        </div>
                        <div className="flex-1">
                            <h3 className="text-base font-medium text-gray-500 mb-1">Strong Topics</h3>
                            {stats?.strong_topics?.length > 0 ? (
                                <div className="flex flex-wrap gap-2">
                                    {stats.strong_topics.map((t: string) => (
                                        <span key={t} className="px-3 py-1 bg-green-100 text-green-700 text-sm rounded-full font-medium">{t}</span>
                                    ))}
                                </div>
                            ) : (
                                <span className="text-gray-900 font-semibold text-lg">None detected yet!</span>
                            )}
                        </div>
                    </motion.div>
                </div>
            </div>

            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8"
            >
                <h2 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
                    <Activity className="w-6 h-6 mr-2 text-primary-600" />
                    Recent Activity Log
                </h2>

                <div className="space-y-6">
                    {stats?.recent_activities?.length > 0 ? stats.recent_activities.map((act: any, idx: number) => (
                        <div key={idx} className="flex items-start">
                            <div className="flex-shrink-0 mr-4">
                                <div className={`w-10 h-10 rounded-full flex items-center justify-center ${act.activity_type === 'quiz' ? 'bg-purple-100 text-purple-600' : 'bg-blue-100 text-blue-600'}`}>
                                    {act.activity_type === 'quiz' ? <Target className="w-5 h-5" /> : <Clock className="w-5 h-5" />}
                                </div>
                            </div>
                            <div className="flex-1 pt-1 pb-4 border-b border-gray-100">
                                <div className="flex justify-between items-start mb-1">
                                    <h4 className="text-base font-semibold text-gray-900 capitalize">
                                        {act.activity_type.replace('_', ' ')}
                                    </h4>
                                    <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                                        {new Date(act.created_at).toLocaleDateString()} at {new Date(act.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </span>
                                </div>
                                {act.activity_type === 'quiz' ? (
                                    <p className="text-sm text-gray-600">
                                        Scored <strong className={act.score > 0.7 ? "text-green-600" : "text-yellow-600"}>{Math.round(act.score * 100)}%</strong> ({act.correct_answers}/{act.total_questions}) on Material {act.material_id.substring(0, 6)}...
                                    </p>
                                ) : (
                                    <p className="text-sm text-gray-600">
                                        Studied for <strong>{act.time_spent} seconds</strong>.
                                    </p>
                                )}
                            </div>
                        </div>
                    )) : (
                        <p className="text-gray-500 py-4">No recent activity found. Start taking quizzes!</p>
                    )}
                </div>
            </motion.div>
        </div>
    );
};

export default Analytics;
