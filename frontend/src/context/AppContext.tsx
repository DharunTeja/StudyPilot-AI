import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface User {
    id: string;
    name: string;
    email: string;
}

interface AppContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (userData: User, token: string) => void;
    logout: () => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useAppContext = () => {
    const context = useContext(AppContext);
    if (!context) {
        throw new Error('useAppContext must be used within an AppProvider');
    }
    return context;
};

export const AppProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const checkAuth = () => {
            const token = localStorage.getItem('studypilot_token');
            if (token) {
                try {
                    const storedUser = localStorage.getItem('studypilot_user');
                    if (storedUser) {
                        setUser(JSON.parse(storedUser));
                        setIsAuthenticated(true);
                    } else {
                        localStorage.removeItem('studypilot_token');
                    }
                } catch (error) {
                    console.error("Auth check failed:", error);
                    localStorage.removeItem('studypilot_token');
                    localStorage.removeItem('studypilot_user');
                }
            }
            setIsLoading(false);
        };

        checkAuth();
    }, []);

    const login = (userData: User, token: string) => {
        localStorage.setItem('studypilot_token', token);
        localStorage.setItem('studypilot_user', JSON.stringify(userData));
        setUser(userData);
        setIsAuthenticated(true);
    };

    const logout = () => {
        localStorage.removeItem('studypilot_token');
        localStorage.removeItem('studypilot_user');
        setUser(null);
        setIsAuthenticated(false);
    };

    return (
        <AppContext.Provider value={{ user, isAuthenticated, isLoading, login, logout }}>
            {children}
        </AppContext.Provider>
    );
};
