import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Layout from './components/Layout';
import UsersPage from './pages/UsersPage';
import RolesPage from './pages/RolesPage';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={
            <div className="bg-white p-8 rounded-xl shadow-sm">
              <h2 className="text-3xl font-bold text-gray-800 mb-4">Bem-vindo ao Modular System</h2>
              <p className="text-gray-600">Selecione um módulo no menu lateral para começar.</p>
              <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-4">
                <Link to="/users" className="p-6 border border-gray-100 rounded-lg hover:bg-blue-50 transition-colors">
                  <h3 className="font-bold text-blue-600">Gestão de Usuários</h3>
                  <p className="text-sm text-gray-500">Cadastre e gerencie os usuários do sistema.</p>
                </Link>
                <Link to="/roles" className="p-6 border border-gray-100 rounded-lg hover:bg-blue-50 transition-colors">
                  <h3 className="font-bold text-blue-600">Perfis de Acesso</h3>
                  <p className="text-sm text-gray-500">Configure permissões e perfis de segurança.</p>
                </Link>
              </div>
            </div>
          } />
          <Route path="/users" element={<UsersPage />} />
          <Route path="/roles" element={<RolesPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
