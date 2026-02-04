import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/auth';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import HomePage from './pages/HomePage';
import ResumeListPage from './pages/ResumeListPage';
import ResumeEditorPage from './pages/ResumeEditorPage';
import TemplatesPage from './pages/TemplatesPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';

function App() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return (
    <Routes>
      {/* 公开路由 */}
      <Route
        path="/login"
        element={!isAuthenticated ? <LoginPage /> : <Navigate to="/" replace />}
      />
      <Route
        path="/register"
        element={!isAuthenticated ? <RegisterPage /> : <Navigate to="/" replace />}
      />

      {/* 受保护路由 */}
      <Route
        path="/"
        element={isAuthenticated ? <HomePage /> : <Navigate to="/login" replace />}
      />
      <Route
        path="/resumes"
        element={isAuthenticated ? <ResumeListPage /> : <Navigate to="/login" replace />}
      />
      <Route
        path="/resumes/new"
        element={isAuthenticated ? <ResumeEditorPage /> : <Navigate to="/login" replace />}
      />
      <Route
        path="/resumes/:id"
        element={isAuthenticated ? <ResumeEditorPage /> : <Navigate to="/login" replace />}
      />
      <Route
        path="/templates"
        element={isAuthenticated ? <TemplatesPage /> : <Navigate to="/login" replace />}
      />
      <Route
        path="/profile"
        element={isAuthenticated ? <ProfilePage /> : <Navigate to="/login" replace />}
      />
      <Route
        path="/settings"
        element={isAuthenticated ? <SettingsPage /> : <Navigate to="/login" replace />}
      />

      {/* 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
