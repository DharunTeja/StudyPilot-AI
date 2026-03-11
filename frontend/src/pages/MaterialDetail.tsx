import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { FileText, Wand2, Target, Brain, AlignLeft, Calendar, Loader2, Play } from 'lucide-react';
import api from '../api/api';

const MaterialDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [material, setMaterial] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('summary');
    const [generating, setGenerating] = useState<string | null>(null);

    // Quiz State
    const [currentQuizIdx, setCurrentQuizIdx] = useState(0);
    const [quizScore, setQuizScore] = useState(0);
    const [quizFinished, setQuizFinished] = useState(false);
    const [quizStartTime, setQuizStartTime] = useState<Date | null>(null);

    useEffect(() => {
        fetchMaterial();
    }, [id]);

    const fetchMaterial = async () => {
        try {
            setLoading(true);
            const { data } = await api.get(`/materials/${id}`);
            setMaterial(data);
        } catch (err) {
            console.error(err);
            navigate('/materials');
        } finally {
            setLoading(false);
        }
    };

    const handleGenerate = async (endpoint: string, stateKey: string) => {
        setGenerating(stateKey);
        try {
            await api.post(`/ai/${id}/${endpoint}`);
            await fetchMaterial(); // Refresh data
        } catch (err) {
            alert("Failed to generate content. Please ensure Gemini API is configured.");
        } finally {
            setGenerating(null);
        }
    };

    const handleQuizAnswer = async (isCorrect: boolean) => {
        const newScore = quizScore + (isCorrect ? 1 : 0);
        setQuizScore(newScore);

        if (material.quizzes && currentQuizIdx + 1 < material.quizzes.length) {
            setCurrentQuizIdx(currentQuizIdx + 1);
        } else {
            setQuizFinished(true);
            // Save attempt
            if (quizStartTime) {
                const timeSpent = Math.floor((new Date().getTime() - quizStartTime.getTime()) / 1000);
                await api.post('/progress/quiz-attempt', {
                    material_id: id,
                    score: newScore / material.quizzes.length,
                    total_questions: material.quizzes.length,
                    correct_answers: newScore,
                    time_spent: timeSpent,
                    answers: [] // Simplified for now
                });
            }
        }
    };

    const startQuiz = () => {
        setCurrentQuizIdx(0);
        setQuizScore(0);
        setQuizFinished(false);
        setQuizStartTime(new Date());
    };

    if (loading) {
        return <div className="flex h-full items-center justify-center"><Loader2 className="w-10 h-10 animate-spin text-primary-600" /></div>;
    }

    return (
        <div className="max-w-7xl mx-auto pb-12">
            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8 mb-8">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-100 pb-6 mb-6">
                    <div className="flex items-center">
                        <div className="w-16 h-16 bg-primary-100 text-primary-600 rounded-2xl flex items-center justify-center mr-5 flex-shrink-0">
                            <FileText className="w-8 h-8" />
                        </div>
                        <div>
                            <h1 className="text-2xl md:text-3xl font-bold text-gray-900 mb-1">{material?.title}</h1>
                            <div className="flex items-center text-sm text-gray-500 space-x-4">
                                <span><Calendar className="w-4 h-4 inline mr-1" /> {new Date(material?.created_at).toLocaleDateString()}</span>
                                <span className="bg-gray-100 px-2 py-0.5 rounded-full capitalize">{material?.subject || 'General'}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="flex space-x-1 overflow-x-auto pb-2 scrollbar-hide">
                    {[
                        { id: 'summary', name: 'Summary & Notes', icon: AlignLeft },
                        { id: 'flashcards', name: 'Flashcards', icon: Brain },
                        { id: 'quiz', name: 'Interactive Quiz', icon: Target },
                        { id: 'raw', name: 'Raw Extract', icon: FileText }
                    ].map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`px-5 py-3 rounded-xl font-medium text-sm flex items-center transition-colors whitespace-nowrap ${activeTab === tab.id
                                ? 'bg-primary-600 text-white shadow-sm'
                                : 'bg-white text-gray-600 hover:bg-primary-50 hover:text-primary-700'
                                }`}
                        >
                            <tab.icon className="w-4 h-4 mr-2" />
                            {tab.name}
                        </button>
                    ))}
                </div>
            </div>

            <AnimatePresence mode="wait">
                {activeTab === 'summary' && (
                    <motion.div key="summary" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        <div className="lg:col-span-2 space-y-8">
                            {material.summary ? (
                                <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 prose prose-primary max-w-none [&>h2]:text-primary-700 [&>h3]:text-gray-800">
                                    <h2 className="text-2xl font-bold mb-6 flex items-center text-primary-800 border-b pb-4">
                                        <Wand2 className="w-6 h-6 mr-3 text-primary-500" />
                                        AI Summary
                                    </h2>
                                    <div className="text-gray-700 whitespace-pre-wrap leading-relaxed">{material.summary}</div>
                                </div>
                            ) : (
                                <div className="bg-white rounded-2xl p-12 shadow-sm border border-dashed border-gray-300 text-center">
                                    <Wand2 className="w-16 h-16 text-primary-200 mx-auto mb-4" />
                                    <h3 className="text-xl font-bold text-gray-800 mb-2">No Summary Generated</h3>
                                    <p className="text-gray-500 mb-6 max-w-md mx-auto">Click below to let StudyPilot's AI generate a comprehensive summary of this material.</p>
                                    <button onClick={() => handleGenerate('summarize', 'summary')} disabled={generating === 'summary'} className="btn-primary w-48">
                                        {generating === 'summary' ? <Loader2 className="w-5 h-5 mx-auto animate-spin" /> : 'Generate Summary'}
                                    </button>
                                </div>
                            )}
                        </div>
                        <div>
                            <div className="bg-gradient-to-b from-blue-50 to-white rounded-2xl p-6 shadow-sm border border-blue-100">
                                <h3 className="text-lg font-bold text-blue-900 mb-4 flex items-center">
                                    <Brain className="w-5 h-5 mr-2 text-blue-500" /> Key Concepts
                                </h3>
                                {material.key_concepts ? (
                                    <ul className="space-y-3">
                                        {material.key_concepts.map((kc: any, i: number) => (
                                            <li key={i} className="bg-white p-3 rounded-lg shadow-sm border border-blue-50 text-sm">
                                                <strong className="text-blue-700 block mb-1">{kc.concept || kc.term || `Concept ${i + 1}`}</strong>
                                                <span className="text-gray-600">{kc.explanation || kc.definition || kc}</span>
                                            </li>
                                        ))}
                                    </ul>
                                ) : (
                                    <p className="text-sm text-gray-500 italic">Generate a summary first to extract key concepts automatically.</p>
                                )}
                            </div>
                        </div>
                    </motion.div>
                )}

                {activeTab === 'flashcards' && (
                    <motion.div key="flashcards" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                        {!material.flashcards ? (
                            <div className="bg-white rounded-2xl p-12 shadow-sm border border-dashed border-gray-300 text-center max-w-2xl mx-auto">
                                <Brain className="w-16 h-16 text-primary-200 mx-auto mb-4" />
                                <h3 className="text-xl font-bold text-gray-800 mb-2">No Flashcards Available</h3>
                                <p className="text-gray-500 mb-6 max-w-md mx-auto">Generate smart flashcards instantly to help you memorize key facts from this material with spaced repetition.</p>
                                <button onClick={() => handleGenerate('flashcards', 'flashcards')} disabled={generating === 'flashcards'} className="btn-primary w-56">
                                    {generating === 'flashcards' ? <Loader2 className="w-5 h-5 mx-auto animate-spin" /> : 'Generate Flashcards'}
                                </button>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {material.flashcards.map((fc: any, i: number) => (
                                    <div key={i} className="group perspective-1000 h-64 w-full cursor-pointer">
                                        <div className="relative w-full h-full transition-transform duration-500 preserve-3d group-hover:rotate-y-180">
                                            {/* Front */}
                                            <div className="absolute w-full h-full bg-white rounded-2xl shadow-sm border border-gray-200 p-6 flex flex-col justify-center items-center text-center backface-hidden">
                                                <p className="text-sm text-primary-500 font-bold mb-4 uppercase tracking-wider">Flashcard {i + 1}</p>
                                                <h3 className="text-xl font-bold text-gray-900">{fc.front}</h3>
                                                <p className="absolute bottom-4 text-xs text-gray-400">Hover to flip ⤵️</p>
                                            </div>
                                            {/* Back */}
                                            <div className="absolute w-full h-full bg-primary-600 rounded-2xl shadow-lg border border-primary-500 p-6 flex flex-col justify-center items-center text-center backface-hidden rotate-y-180 text-white">
                                                <p className="text-lg font-medium leading-relaxed">{fc.back}</p>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </motion.div>
                )}

                {activeTab === 'quiz' && (
                    <motion.div key="quiz" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                        {!material.quizzes ? (
                            <div className="bg-white rounded-2xl p-12 shadow-sm border border-dashed border-gray-300 text-center max-w-2xl mx-auto">
                                <Target className="w-16 h-16 text-primary-200 mx-auto mb-4" />
                                <h3 className="text-xl font-bold text-gray-800 mb-2">Ready for a Quiz?</h3>
                                <p className="text-gray-500 mb-6 max-w-md mx-auto">Test your knowledge! We will generate questions strictly based on the content of this material.</p>
                                <button onClick={() => handleGenerate('quiz', 'quiz')} disabled={generating === 'quiz'} className="btn-primary w-48">
                                    {generating === 'quiz' ? <Loader2 className="w-5 h-5 mx-auto animate-spin" /> : 'Generate Quiz'}
                                </button>
                            </div>
                        ) : (
                            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 max-w-4xl mx-auto">
                                {!quizStartTime && !quizFinished ? (
                                    <div className="text-center py-12">
                                        <div className="w-20 h-20 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-6">
                                            <Play className="w-10 h-10 text-primary-600 ml-1" />
                                        </div>
                                        <h2 className="text-3xl font-bold text-gray-900 mb-4">{material.quizzes.length} Questions Ready</h2>
                                        <p className="text-gray-500 mb-8 max-w-md mx-auto">This quiz covers the material content. Your score will be recorded to your learning analytics dashboard.</p>
                                        <button onClick={startQuiz} className="btn-primary px-8 py-3 text-lg w-full md:w-auto">Start Quiz Now</button>
                                    </div>
                                ) : quizFinished ? (
                                    <div className="text-center py-12">
                                        <div className="w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-6 bg-gradient-to-tr from-green-400 to-primary-500 text-white shadow-lg">
                                            <Target className="w-12 h-12" />
                                        </div>
                                        <h2 className="text-3xl font-bold text-gray-900 mb-2">Quiz Completed!</h2>
                                        <p className="text-xl text-gray-600 mb-8">You scored <strong className="text-gray-900">{quizScore} / {material.quizzes.length}</strong> ({(quizScore / material.quizzes.length * 100).toFixed(0)}%)</p>
                                        <div className="flex justify-center gap-4">
                                            <button onClick={startQuiz} className="btn-secondary">Retake Quiz</button>
                                            <button onClick={() => setActiveTab('summary')} className="btn-primary">Review Material</button>
                                        </div>
                                    </div>
                                ) : (
                                    <div className="relative">
                                        <div className="flex justify-between items-center mb-8">
                                            <span className="text-sm font-semibold text-primary-600 tracking-wider uppercase">Question {currentQuizIdx + 1} of {material.quizzes.length}</span>
                                            <span className="text-sm font-bold bg-gray-100 px-3 py-1 rounded-full text-gray-700">Score: {quizScore}</span>
                                        </div>

                                        <div className="w-full bg-gray-100 h-2 rounded-full mb-8 overflow-hidden">
                                            <motion.div
                                                className="bg-primary-500 h-full rounded-full"
                                                initial={{ width: 0 }}
                                                animate={{ width: `${((currentQuizIdx) / material.quizzes.length) * 100}%` }}
                                            />
                                        </div>

                                        <h3 className="text-2xl font-bold text-gray-900 mb-8 leading-relaxed">
                                            {material.quizzes[currentQuizIdx].question}
                                        </h3>

                                        {material.quizzes[currentQuizIdx].type === 'mcq' || material.quizzes[currentQuizIdx].options ? (
                                            <div className="grid grid-cols-1 gap-4">
                                                {material.quizzes[currentQuizIdx].options.map((opt: string, i: number) => (
                                                    <button
                                                        key={i}
                                                        onClick={() => handleQuizAnswer(opt === material.quizzes[currentQuizIdx].correct_answer)}
                                                        className="text-left w-full p-5 rounded-xl border-2 border-gray-100 hover:border-primary-400 hover:bg-primary-50 transition-all font-medium text-gray-700 hover:text-primary-800 shadow-sm"
                                                    >
                                                        <span className="inline-block w-8 h-8 bg-white border border-gray-200 rounded-lg text-center leading-7 mr-3 text-gray-400 group-hover:border-primary-300 group-hover:text-primary-600">
                                                            {String.fromCharCode(65 + i)}
                                                        </span>
                                                        {opt}
                                                    </button>
                                                ))}
                                            </div>
                                        ) : (
                                            <div className="grid grid-cols-2 gap-4">
                                                <button onClick={() => handleQuizAnswer(material.quizzes[currentQuizIdx].correct_answer === "True")} className="p-6 text-center border-2 rounded-xl text-lg font-bold text-gray-700 hover:bg-green-50 hover:text-green-700 hover:border-green-300 transition-colors">True</button>
                                                <button onClick={() => handleQuizAnswer(material.quizzes[currentQuizIdx].correct_answer === "False")} className="p-6 text-center border-2 rounded-xl text-lg font-bold text-gray-700 hover:bg-red-50 hover:text-red-700 hover:border-red-300 transition-colors">False</button>
                                            </div>
                                        )}
                                    </div>
                                )}
                            </div>
                        )}
                    </motion.div>
                )}

                {activeTab === 'raw' && (
                    <motion.div key="raw" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                        <div className="bg-gray-900 rounded-2xl p-6 shadow-sm overflow-hidden text-gray-300 font-mono text-sm max-h-[800px] overflow-y-auto w-full relative">
                            <div className="absolute top-0 right-0 bg-gray-800 text-xs px-3 py-1 text-gray-400 rounded-bl-lg">Read-Only View</div>
                            <div className="whitespace-pre-wrap">{material.content}</div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default MaterialDetail;
