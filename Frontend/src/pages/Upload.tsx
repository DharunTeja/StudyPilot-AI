import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, FileText, Image as ImageIcon, X, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import api from '../api/api';

const Upload = () => {
    const [file, setFile] = useState<File | null>(null);
    const [text, setText] = useState('');
    const [title, setTitle] = useState('');
    const [subject, setSubject] = useState('');
    const [uploadType, setUploadType] = useState<'file' | 'text'>('file');
    const [isDragging, setIsDragging] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const fileInputRef = useRef<HTMLInputElement>(null);
    const navigate = useNavigate();

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            handleFileSelection(e.target.files[0]);
        }
    };

    const handleFileSelection = (selectedFile: File) => {
        const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/webp', 'text/plain'];
        if (!validTypes.includes(selectedFile.type)) {
            setError('Invalid file type. Please upload a PDF, Image, or TXT file.');
            return;
        }

        setFile(selectedFile);
        if (!title) {
            setTitle(selectedFile.name.split('.')[0]);
        }
        setError('');
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim()) {
            setError('Please provide a title for this material.');
            return;
        }

        if (uploadType === 'file' && !file) {
            setError('Please select a file to upload.');
            return;
        }

        if (uploadType === 'text' && !text.trim()) {
            setError('Please enter some text content.');
            return;
        }

        setLoading(true);
        setError('');

        try {
            const formData = new FormData();
            formData.append('title', title);
            formData.append('subject', subject || 'General');

            if (uploadType === 'file' && file) {
                formData.append('file', file);
            } else if (uploadType === 'text') {
                formData.append('content', text);
            }

            const { data } = await api.post('/materials/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            navigate(`/materials/${data.material.id}`);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to upload material. Please try again.');
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto pb-12">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-gray-900 mb-2">Upload Material</h1>
                <p className="text-gray-500">Add new documents, notes, or images and let StudyPilot AI process them.</p>
            </div>

            {error && (
                <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded-r-lg">
                    <p className="text-red-700">{error}</p>
                </div>
            )}

            <div className="bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                <div className="flex border-b border-gray-100">
                    <button
                        type="button"
                        onClick={() => setUploadType('file')}
                        className={`flex-1 py-4 px-6 text-sm flex justify-center items-center font-medium transition-colors ${uploadType === 'file'
                                ? 'text-primary-700 bg-primary-50/50 border-b-2 border-primary-600'
                                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                            }`}
                    >
                        <FileText className="w-4 h-4 mr-2" />
                        File Upload (PDF/Image)
                    </button>
                    <button
                        type="button"
                        onClick={() => setUploadType('text')}
                        className={`flex-1 py-4 px-6 text-sm flex justify-center items-center font-medium transition-colors ${uploadType === 'text'
                                ? 'text-primary-700 bg-primary-50/50 border-b-2 border-primary-600'
                                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                            }`}
                    >
                        <ImageIcon className="w-4 h-4 mr-2" />
                        Paste Text
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="p-6 md:p-8">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1.5">Material Title *</label>
                            <input
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                placeholder="e.g. Chapter 4: Cellular Respiration"
                                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                                required
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1.5">Subject (Optional)</label>
                            <input
                                type="text"
                                value={subject}
                                onChange={(e) => setSubject(e.target.value)}
                                placeholder="e.g. Biology 101"
                                className="w-full px-4 py-2.5 rounded-xl border border-gray-200 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                            />
                        </div>
                    </div>

                    <AnimatePresence mode="wait">
                        {uploadType === 'file' ? (
                            <motion.div
                                key="file"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.2 }}
                            >
                                {!file ? (
                                    <div
                                        className={`border-2 border-dashed rounded-2xl p-12 text-center transition-all ${isDragging
                                                ? 'border-primary-500 bg-primary-50 scale-[1.02]'
                                                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
                                            }`}
                                        onDragOver={handleDragOver}
                                        onDragLeave={handleDragLeave}
                                        onDrop={handleDrop}
                                        onClick={() => fileInputRef.current?.click()}
                                    >
                                        <input
                                            type="file"
                                            className="hidden"
                                            ref={fileInputRef}
                                            onChange={handleFileChange}
                                            accept=".pdf,.png,.jpg,.jpeg,.webp,.txt"
                                        />
                                        <UploadCloud className={`mx-auto h-12 w-12 mb-4 ${isDragging ? 'text-primary-500' : 'text-gray-400'}`} />
                                        <h3 className="text-lg font-medium text-gray-900 mb-1">Click or drag file to this area to upload</h3>
                                        <p className="text-sm text-gray-500 mb-4">Support for a single or bulk upload. Strictly prohibit from uploading company data or other band files</p>
                                        <p className="text-xs font-semibold text-gray-400 bg-gray-100 px-3 py-1 rounded-full inline-block">
                                            Supported: PDF, JPG, PNG, TXT
                                        </p>
                                    </div>
                                ) : (
                                    <div className="border border-gray-200 rounded-2xl p-6 bg-gray-50 flex items-center justify-between">
                                        <div className="flex items-center">
                                            <div className="w-12 h-12 bg-white rounded-xl flex items-center justify-center text-primary-600 shadow-sm border border-gray-100 mr-4">
                                                {file.type.includes('pdf') ? <FileText className="w-6 h-6" /> : <ImageIcon className="w-6 h-6" />}
                                            </div>
                                            <div>
                                                <p className="font-medium text-gray-900 truncate max-w-xs md:max-w-md">{file.name}</p>
                                                <p className="text-sm text-gray-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                            </div>
                                        </div>
                                        <button
                                            type="button"
                                            onClick={(e) => { e.stopPropagation(); setFile(null); }}
                                            className="p-2 text-gray-400 hover:text-red-500 hover:bg-white rounded-full transition-colors"
                                        >
                                            <X className="w-5 h-5" />
                                        </button>
                                    </div>
                                )}
                            </motion.div>
                        ) : (
                            <motion.div
                                key="text"
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.2 }}
                            >
                                <label className="block text-sm font-medium text-gray-700 mb-1.5">Raw Text Content</label>
                                <textarea
                                    value={text}
                                    onChange={(e) => setText(e.target.value)}
                                    placeholder="Paste your lecture notes, article, or text here..."
                                    className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors h-64 resize-none"
                                    required={uploadType === 'text'}
                                />
                            </motion.div>
                        )}
                    </AnimatePresence>

                    <div className="mt-8 pt-6 border-t border-gray-100 flex justify-end">
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-6 py-2.5 rounded-xl text-white font-medium bg-primary-600 hover:bg-primary-700 transition-colors shadow-sm focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-70 disabled:cursor-not-allowed flex items-center"
                        >
                            {loading ? (
                                <>
                                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                                    Generating AI Magic...
                                </>
                            ) : (
                                'Upload & Process'
                            )}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default Upload;
