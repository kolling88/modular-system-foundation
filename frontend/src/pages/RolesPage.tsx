import React, { useEffect } from 'react';
import { useRoleStore } from '../store/useRoleStore';
import { Shield, Plus, Edit2 } from 'lucide-react';

const RolesPage: React.FC = () => {
  const { roles, loading, fetchRoles } = useRoleStore();

  useEffect(() => {
    fetchRoles();
  }, [fetchRoles]);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold text-gray-800">Perfis de Acesso</h2>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center hover:bg-blue-700 transition-colors">
          <Plus className="w-5 h-5 mr-2" />
          Novo Perfil
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <p>Carregando...</p>
        ) : roles.map((role) => (
          <div key={role.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-4">
              <div className="bg-blue-100 p-2 rounded-lg">
                <Shield className="w-6 h-6 text-blue-600" />
              </div>
              <button className="text-gray-400 hover:text-blue-600">
                <Edit2 className="w-4 h-4" />
              </button>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-1 capitalize">{role.name}</h3>
            <p className="text-sm text-gray-600 mb-4">{role.description || 'Sem descrição'}</p>
            <div className="pt-4 border-t border-gray-50">
              <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Permissões</span>
              <div className="mt-2 flex flex-wrap gap-2">
                {role.permissions?.split(',').map((perm, idx) => (
                  <span key={idx} className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-[10px] font-medium">
                    {perm.trim()}
                  </span>
                )) || <span className="text-xs text-gray-400 italic">Nenhuma</span>}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RolesPage;
