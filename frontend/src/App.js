import React from 'react';
import { AuthProvider } from './AuthContext';
import ProtectedRoute from './ProtectedRoute';
import MainApp from './MainApp';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <ProtectedRoute>
        <MainApp />
      </ProtectedRoute>
    </AuthProvider>
  );
}

export default App;