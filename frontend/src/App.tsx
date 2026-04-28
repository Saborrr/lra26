import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { LeaderboardPage } from './pages/LeaderboardPage';
import { AdminLayout } from './pages/admin/AdminLayout';
import { DashboardPage } from './pages/admin/DashboardPage';
import { TeamsPage } from './pages/admin/TeamsPage';
import { ScoresPage } from './pages/admin/ScoresPage';
import { QuestsPage } from './pages/admin/QuestsPage';
import { TrainersPage } from './pages/admin/TrainersPage';
import { MarksPage } from './pages/admin/MarksPage';
import { VkProvider } from './services/vk';
import './index.css';

function App() {
  return (
    <VkProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LeaderboardPage />} />
          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<DashboardPage />} />
            <Route path="teams" element={<TeamsPage />} />
            <Route path="scores" element={<ScoresPage />} />
            <Route path="quests" element={<QuestsPage />} />
            <Route path="trainers" element={<TrainersPage />} />
            <Route path="marks" element={<MarksPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </VkProvider>
  );
}

export default App;
