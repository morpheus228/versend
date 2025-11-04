// src/components/Header.jsx
import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { Button, message } from 'antd';

export default function Header() {
  const location = useLocation();
  const navigate = useNavigate();

  const links = [
    { path: '/accounts', label: 'Аккаунты' },
    { path: '/campaigns', label: 'Кампании' },
  ];

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    message.success('Вы вышли из аккаунта');
    navigate('/login');
  };

  return (
    <header className="bg-white border-b shadow-sm px-6 py-3 flex items-center justify-between">
      {/* Название админки ведёт на домашнюю страницу */}
      <Link to="/" className="text-lg font-semibold hover:text-blue-600 transition">
        📢 Versand Admin Panel
      </Link>

      <div className="flex items-center gap-6">
        <nav className="flex gap-6">
          {links.map((link) => {
            const active = location.pathname.startsWith(link.path);
            return (
              <Link
                key={link.path}
                to={link.path}
                className={`${
                  active
                    ? 'text-blue-600 font-medium'
                    : 'text-gray-600 hover:text-blue-500'
                } transition`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Кнопка выхода */}
        <Button type="primary" danger onClick={handleLogout}>
          Выйти
        </Button>
      </div>
    </header>
  );
}
