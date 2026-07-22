import { BrowserRouter, Route, Routes } from 'react-router-dom';

import { AppShell } from './components/AppShell';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AuthProvider } from './contexts/AuthContext';
import { AdminPage } from './pages/AdminPage';
import { HomePage } from './pages/HomePage';
import { LoginPage } from './pages/LoginPage';
import { NotFoundPage } from './pages/NotFoundPage';
import { ParticipantPage } from './pages/ParticipantPage';
import { SuperAdminPage } from './pages/SuperAdminPage';

const basename = import.meta.env.BASE_URL.replace(/\/$/, '');

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter basename={basename}>
        <Routes>
          <Route element={<AppShell />}>
            <Route index element={<HomePage />} />
            <Route path="login" element={<LoginPage />} />
            <Route path="app" element={<ProtectedRoute><ParticipantPage /></ProtectedRoute>} />
            <Route path="admin" element={<ProtectedRoute minimum="admin"><AdminPage /></ProtectedRoute>} />
            <Route path="superadmin" element={<ProtectedRoute minimum="superadmin"><SuperAdminPage /></ProtectedRoute>} />
            <Route path="*" element={<NotFoundPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}
