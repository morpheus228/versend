import React, { useRef, useState } from 'react';
import { Modal, Form, Input, message } from 'antd';
import { api } from '../api';

export default function AccountForm({ visible, onClose, onSuccess }) {
  const [saving, setSaving] = useState(false);
  const formRef = useRef(null);

  const handleSubmit = async () => {
    try {
      const values = await formRef.current.validateFields();

      // Преобразуем числовые поля
      values.id = Number(values.id);
      values.api_id = Number(values.api_id);

      setSaving(true);

      const response = await api.createAccount(values);

      // Проверяем статус, если сервер возвращает его явно
      if (response && response.status && response.status !== 200) {
        message.error(`Ошибка ${response.status}: ${response.statusText}`);
        return;
      }

      message.success('Аккаунт добавлен');
      onClose();
      onSuccess?.();
    } catch (err) {
      console.error('Ошибка при добавлении аккаунта:', err);

      // axios иногда кидает err как обычный Error, иногда как объект с response
      const status = err?.response?.status || err?.status || 0;
      const text =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        err?.message ||
        'Неизвестная ошибка';

      message.error(
        status ? `Ошибка ${status}: ${text}` : `Ошибка: ${text}`
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <Modal
      title="Добавить аккаунт"
      open={visible}
      onCancel={onClose}
      onOk={handleSubmit}
      confirmLoading={saving}
      destroyOnClose
    >
      <Form layout="vertical" ref={formRef}>
        <Form.Item
          label="ID"
          name="id"
          rules={[{ required: true, message: 'Введите ID' }]}
        >
          <Input placeholder="Числовой ID" />
        </Form.Item>

        <Form.Item
          label="Username"
          name="username"
          rules={[{ required: true, message: 'Введите username' }]}
        >
          <Input placeholder="username" />
        </Form.Item>

        <Form.Item
          label="Телефон"
          name="phone_number"
          rules={[{ required: true, message: 'Введите телефон' }]}
        >
          <Input placeholder="Любой формат" />
        </Form.Item>

        <Form.Item
          label="API ID"
          name="api_id"
          rules={[{ required: true, message: 'Введите API ID' }]}
        >
          <Input placeholder="Число" />
        </Form.Item>

        <Form.Item
          label="API Hash"
          name="api_hash"
          rules={[{ required: true, message: 'Введите API Hash' }]}
        >
          <Input placeholder="API Hash" />
        </Form.Item>

        <Form.Item
          label="Session String"
          name="session_string"
          rules={[{ required: true, message: 'Введите session_string' }]}
        >
          <Input.TextArea rows={3} />
        </Form.Item>
      </Form>
    </Modal>
  );
}
