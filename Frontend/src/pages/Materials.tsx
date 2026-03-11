import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Book, FileText, Calendar, ArrowRight, Trash2 } from 'lucide-react';
import api from '../api/api';

const Materials = () => {
    const [materials, setMaterials] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMaterials = async () => {
            try {
                const { data } = await api.get('/materials');
                setMaterials(data.materials);
            } catch (err) {
                console.error("Failed to fetch materials", err);
            } finally {
                setLoading(false);
            }
        };
        fetchMaterials();
    }, []);

    const handleDelete = async (e: React.MouseEvent, id: string) => {
        e.preventDefault();
        e.stopPropagation();
        if (window.confirm('Are you sure you want to delete this material?')) {
            try {
                await api.delete(`/materials/${id}`);
                setMaterials(materials.filter(m => m.id !== id));
            } catch (err) {
                console.error("Failed to delete", err);
            }
        }
    };

    if (loading) {
        return (
            <div className="flex justify-center items-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            </div>
        );
    }

    return (
        <div className="max-w-7xl mx-auto space-y-8 pb-12">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
                <div>
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">My Materials</h1>
                    <p className="text-gray-500">Access all your processed study documents and generated AI quizzes.</p>
                </div>
                <Link
                    to="/upload"
                    className="bg-primary-600 hover:bg-primary-700 text-white px-5 py-2.5 rounded-xl font-medium transition-colors shadow-sm flex items-center"
                >
                    <Book className="w-5 h-5 mr-2" />
                    Add New
                </Link>
            </div>

            {materials.length === 0 ? (
                <div className="bg-white rounded-2xl border border-dashed border-gray-300 p-12 text-center">
                    <Book className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                    <h3 className="text-xl font-bold text-gray-700 mb-2">No materials found</h3>
                    <p className="text-gray-500 mb-6 max-w-md mx-auto">Upload your first PDF or set of notes to start generating AI study resources!</p>
                    <Link to="/upload" className="btn-primary inline-flex items-center">
                        Go to Upload <ArrowRight className="w-4 h-4 ml-2" />
                    </Link>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                    {materials.map((material, index) => (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.1 }}
                            key={material.id}
                        >
                            <Link
                                to={`/materials/${material.id}`}
                                className="block bg-white rounded-2xl border border-gray-200 p-6 hover:shadow-lg transition-all hover:border-primary-300 group h-full flex flex-col relative"
                            >
                                <button
                                    onClick={(e) => handleDelete(e, material.id)}
                                    className="absolute top-4 right-4 text-gray-400 hover:text-red-500 bg-white p-1.5 rounded-md opacity-0 group-hover:opacity-100 transition-opacity z-10"
                                >
                                    <Trash2 className="w-5 h-5" />
                                </button>

                                <div className="flex items-center mb-4 pr-8">
                                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center mr-4 ${material.file_type === 'pdf' ? 'bg-red-100 text-red-600' :
                                            material.file_type === 'text' ? 'bg-blue-100 text-blue-600' : 'bg-green-100 text-green-600'
                                        }`}>
                                        <FileText className="w-6 h-6" />
                                    </div>
                                    <div className="flex-1 min-w-0">
                                        <h3 className="text-lg font-bold text-gray-900 truncate" title={material.title}>{material.title}</h3>
                                        <p className="text-sm text-primary-600 font-medium">{material.subject || 'General'}</p>
                                    </div>
                                </div>

                                <p className="text-gray-600 text-sm mb-6 flex-1 line-clamp-3">
                                    {material.content_preview}
                                </p>

                                <div className="flex items-center justify-between text-xs font-medium pt-4 border-t border-gray-100">
                                    <div className="flex items-center text-gray-500">
                                        <Calendar className="w-4 h-4 mr-1.5" />
                                        {new Date(material.created_at).toLocaleDateString()}
                                    </div>

                                    <div className="flex space-x-2">
                                        {material.has_summary && <span className="bg-purple-100 text-purple-700 px-2.5 py-1 rounded-full">S</span>}
                                        {material.has_quizzes && <span className="bg-orange-100 text-orange-700 px-2.5 py-1 rounded-full">Q</span>}
                                        {material.has_flashcards && <span className="bg-teal-100 text-teal-700 px-2.5 py-1 rounded-full">F</span>}
                                    </div>
                                </div>
                            </Link>
                        </motion.div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Materials;
