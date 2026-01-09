export interface Role {
  id: number;
  name: string;
  description?: string;
  permissions?: string;
}

export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  roles: Role[];
}

export interface UserCreate {
  email: string;
  full_name: string;
  password?: string;
  is_superuser?: boolean;
}

export interface RoleCreate {
  name: string;
  description?: string;
  permissions?: string;
}
