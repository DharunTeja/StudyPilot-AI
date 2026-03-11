import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Auth from './pages/Auth';
import { useAppContext } from './context/AppContext';

import Dashboard from './pages/Dashboard';
import Materials from './pages/Materials';
import MaterialDetail from './pages/MaterialDetail';
import Upload from './pages/Upload';
import Analytics from './pages/Analytics';

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
    const { isAuthenticated, isLoading } = useAppContext();

    if (isLoading) return <div className="flex h-screen items-center justify-center">Loading...</div>;
    if (!isAuthenticated) return <Navigate to="/auth" replace />;

    return <>{children}</>;
};

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/auth" element={<Auth />} />

                <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
                    <Route index element={<Navigate to="/dashboard" replace />} />
                    <Route path="dashboard" element={<Dashboard />} />
                    <Route path="materials" element={<Materials />} />
                    <Route path="materials/:id" element={<MaterialDetail />} />
                    <Route path="upload" element={<Upload />} />
                    <Route path="analytics" element={<Analytics />} />
                </Route>

                <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
