import React, { useEffect, useState } from 'react';
import { Table, Button, message, Space, Modal } from 'antd';
import { PlusOutlined, ReloadOutlined } from '@ant-design/icons';
import { api } from '../api';
import { useNavigate } from 'react-router-dom';
import CreateCampaignModal from '../components/CreateCampaignModal';

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);

  // ✅ модалка дублей
  const [duplicateModal, setDuplicateModal] = useState({
    open: false,
    list: [],
  });

  const navigate = useNavigate();

  const fetchCampaigns = async () => {
    setLoading(true);
    try {
      const res = await api.getCampaigns();
      setCampaigns(res.data || []);
    } catch (err) {
      message.error('Ошибка при загрузке кампаний');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCampaigns();
  }, []);

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: 'Название',
      dataIndex: 'name',
      key: 'name',
      render: (text, record) => (
        <span
          onClick={() => navigate(`/campaigns/${record.id}`)}
          className="text-blue-600 cursor-pointer hover:underline"
        >
          {text}
        </span>
      ),
    },
    {
      title: 'Текст рассылки',
      dataIndex: 'text',
      key: 'text',
      ellipsis: true,
    },
    {
      title: 'Промпт',
      dataIndex: 'promt',
      key: 'promt',
      ellipsis: true,
    },
    {
      title: 'Статусы',
      key: 'statuses',
      render: (_, record) => (
        <div className="flex gap-3 text-sm">
          <span className="text-yellow-600">⏳ {record.wait}</span>
          <span className="text-green-600">🟢 {record.open}</span>
          <span className="text-gray-500">⛔ {record.stop}</span>
          <span className="text-red-600">❌ {record.fail}</span>
        </div>
      ),
    },
  ];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-xl font-semibold">Кампании</h1>
        <Space>
          <Button icon={<ReloadOutlined />} onClick={fetchCampaigns}>
            Обновить
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setModalVisible(true)}
          >
            Создать кампанию
          </Button>
        </Space>
      </div>

      <Table
        dataSource={campaigns}
        columns={columns}
        rowKey="id"
        loading={loading}
        bordered
        pagination={false}
      />

     <CreateCampaignModal
  open={modalVisible}
  onCancel={() => setModalVisible(false)}
  onCreated={(data) => {
    setModalVisible(false);
    fetchCampaigns();

    // ✅ Уведомление об успешном создании
    message.success("Кампания успешно создана!");

    // ✅ Если есть дубли — открываем отдельное окно
    if (data?.duplicate_usernames?.length) {
      setDuplicateModal({
        open: true,
        list: data.duplicate_usernames
      });
    }
  }}

    />  

      {/* ✅ модальное окно для дублей */}
      <Modal
        open={duplicateModal.open}
        title="Найдены дубликаты"
        onCancel={() => setDuplicateModal({ open: false, list: [] })}
        onOk={() => setDuplicateModal({ open: false, list: [] })}
      >
        <p>Следующие usernames уже существуют:</p>
        <p style={{ marginTop: 10, fontWeight: "bold" }}>
          {duplicateModal.list.join(', ')}
        </p>
      </Modal>
    </div>
  );
}
