import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Card, message, Button, Space, Spin } from 'antd';
import { ArrowLeftOutlined, ReloadOutlined } from '@ant-design/icons';
import { api } from '../api';

export default function DialogDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [dialog, setDialog] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchDialog = async () => {
    setLoading(true);
    try {
      const res = await api.getDialog(id);
      setDialog(res.data);
    } catch (err) {
      message.error('Ошибка при загрузке диалога');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDialog();
  }, [id]);

  if (!dialog) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spin size="large" tip="Загрузка диалога..." />
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm">
      <Space className="mb-4">
        <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)}>
          Назад
        </Button>
        <Button icon={<ReloadOutlined />} onClick={fetchDialog}>
          Обновить
        </Button>
      </Space>

      <h1 className="text-2xl font-bold mb-4">
        Диалог #{dialog.id} — {dialog.username}
      </h1>

      <Card className="mb-6 space-y-2">
        <p><strong>Кампания:</strong> <Link to={`/campaigns/${dialog.campaign_id}`}>#{dialog.campaign_id}</Link></p>
        <p><strong>Аккаунт:</strong> {dialog.account_id || '—'}</p>
        <p><strong>Статус:</strong> {dialog.status}</p>
      </Card>

      <Card title="Сообщения" className="border border-gray-100">
        <div className="flex flex-col gap-3">
          {dialog.messages.length === 0 ? (
            <p className="text-gray-500">Сообщений пока нет.</p>
          ) : (
            dialog.messages.map((msg) => (
            <div
            key={msg.id}
            className={`p-3 rounded-2xl max-w-xl ${
                msg.from_user
                ? 'bg-gray-100 self-start text-left'   // теперь от пользователя слева
                : 'bg-blue-50 self-end text-right'     // бот/не пользователь справа
            }`}
            >
            <p className="whitespace-pre-wrap text-gray-800">{msg.text}</p>
            </div>
            ))
          )}
        </div>
      </Card>
    </div>
  );
}
