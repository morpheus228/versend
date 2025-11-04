import React, { useEffect, useState } from 'react';
import { Table, Button, message, Spin, Tooltip } from 'antd';
import { CopyOutlined, ReloadOutlined, PlusOutlined } from '@ant-design/icons';
import { api } from '../api';
import AccountForm from '../components/AccountForm';

export default function Accounts() {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);

  const loadAccounts = async () => {
    setLoading(true);
    try {
      const res = await api.getAccounts();
      // Берём данные из res.data, т.к. api возвращает весь объект ответа
      const data = Array.isArray(res.data) ? res.data : [];
      setAccounts(data);
    } catch (err) {
      console.error('Ошибка при загрузке аккаунтов:', err);
      const detail =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        err?.message ||
        'Неизвестная ошибка';
      const status = err?.response?.status;
      message.error(status ? `Ошибка ${status}: ${detail}` : `Ошибка: ${detail}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  const handleCopy = async (text, label) => {
    try {
      await navigator.clipboard.writeText(text);
      message.success(`${label} скопирован`);
    } catch {
      message.error('Не удалось скопировать');
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 160 },
    {
      title: 'Username',
      dataIndex: 'username',
      key: 'username',
      render: (v) => (v ? `@${v}` : '-'),
    },
    { title: 'Телефон', dataIndex: 'phone_number', key: 'phone_number', width: 180 },
    {
      title: 'API ID',
      key: 'api_id',
      align: 'center',
      render: (_, record) => (
        <Tooltip title={record.api_id}>
          <Button
            icon={<CopyOutlined />}
            size="small"
            onClick={() => handleCopy(record.api_id, 'API ID')}
          >
            Скопировать
          </Button>
        </Tooltip>
      ),
    },
    {
      title: 'API Hash',
      key: 'api_hash',
      align: 'center',
      render: (_, record) => (
        <Tooltip title={record.api_hash}>
          <Button
            icon={<CopyOutlined />}
            size="small"
            onClick={() => handleCopy(record.api_hash, 'API Hash')}
          >
            Скопировать
          </Button>
        </Tooltip>
      ),
    },
    {
      title: 'Session String',
      key: 'session_string',
      align: 'center',
      render: (_, record) => (
        <Tooltip title="Скопировать session_string">
          <Button
            icon={<CopyOutlined />}
            size="small"
            onClick={() => handleCopy(record.session_string, 'Session String')}
          >
            Скопировать
          </Button>
        </Tooltip>
      ),
    },
  ];

  return (
    <div className="p-4">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold">Аккаунты Telegram</h2>
        <div className="flex gap-2">
          <Button
            icon={<ReloadOutlined />}
            onClick={loadAccounts}
            loading={loading}
          >
            Обновить
          </Button>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setModalVisible(true)}
          >
            Добавить
          </Button>
        </div>
      </div>

      <Spin spinning={loading}>
        <Table
          rowKey="id"
          dataSource={accounts}
          columns={columns}
          bordered
          pagination={{ pageSize: 10 }}
        />
      </Spin>

      <AccountForm
        visible={modalVisible}
        onClose={() => setModalVisible(false)}
        onSuccess={loadAccounts}
      />
    </div>
  );
}
