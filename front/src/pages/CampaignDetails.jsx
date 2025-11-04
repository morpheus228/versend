import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Table, Card, message, Button, Space, Spin } from 'antd';
import { ReloadOutlined, ArrowLeftOutlined } from '@ant-design/icons';
import { api } from '../api';

export default function CampaignDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [campaign, setCampaign] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchCampaign = async () => {
    setLoading(true);
    try {
      const res = await api.getCampaign(id);
      setCampaign(res.data);
    } catch (err) {
      message.error('Ошибка при загрузке кампании');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCampaign();
  }, [id]);

  if (!campaign) {
    return (
      <div className="flex justify-center items-center h-64">
        <Spin size="large" tip="Загрузка кампании..." />
      </div>
    );
  }

  const statusCounts = campaign.dialogs?.reduce(
    (acc, dialog) => {
      acc[dialog.status] = (acc[dialog.status] || 0) + 1;
      return acc;
    },
    { wait: 0, open: 0, fail: 0, stop: 0 }
  );

  const dialogColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: 'Username', dataIndex: 'username', key: 'username' },
    { title: 'Account ID', dataIndex: 'account_id', key: 'account_id' },
    { title: 'Status', dataIndex: 'status', key: 'status' },
  ];

  // 👇 Вот здесь return внутри функции!
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm">
      <Space className="mb-4">
        <Button icon={<ArrowLeftOutlined />} onClick={() => navigate('/campaigns')}>
          Назад
        </Button>
        <Button icon={<ReloadOutlined />} onClick={fetchCampaign}>
          Обновить
        </Button>
      </Space>

      <h1 className="text-2xl font-bold mb-4">{campaign.name}</h1>

      <Card className="mb-4 space-y-4">
        <div className="border border-gray-200 bg-gray-50 rounded-xl p-3">
          <p className="font-semibold text-gray-700 mb-1">Текст рассылки:</p>
          <p className="whitespace-pre-wrap text-gray-800">{campaign.text}</p>
        </div>

        <div className="border border-gray-200 bg-gray-50 rounded-xl p-3">
          <p className="font-semibold text-gray-700 mb-1">Промпт:</p>
          <p className="whitespace-pre-wrap text-gray-800">{campaign.promt}</p>
        </div>

        <div className="flex flex-wrap gap-4 text-sm mt-3">
          <span className="text-yellow-600">⏳ Ожидают: {statusCounts.wait}</span>
          <span className="text-green-600">🟢 Активные: {statusCounts.open}</span>
          <span className="text-gray-500">⛔ Завершены: {statusCounts.stop}</span>
          <span className="text-red-600">❌ Неуспех: {statusCounts.fail}</span>
        </div>
      </Card>

      <Table
        dataSource={campaign.dialogs}
        columns={dialogColumns}
        rowKey="id"
        bordered
        loading={loading}
        pagination={false}
        onRow={(record) => ({
          onClick: () => navigate(`/dialogs/${record.id}`),
        })}
        rowClassName="cursor-pointer hover:bg-gray-50 transition"
      />
    </div>
  );
}
