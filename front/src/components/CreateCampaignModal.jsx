import React from 'react';
import { Modal, Form, Input, message } from 'antd';
import { api } from '../api';

export default function CreateCampaignModal({ open, onCancel, onCreated }) {
  const [form] = Form.useForm();

  const handleCreate = async (values) => {
    // Преобразуем usernames из строки в массив
    const usernamesArray = values.usernames
      ? values.usernames
          .split(',')
          .map((u) => u.trim())
          .filter(Boolean)
      : [];

    const payload = {
      ...values,
      usernames: usernamesArray,
    };

    try {
      const res = await api.createCampaign(payload);

      // ✅ передаем данные, включая dublicate_usernames
      onCreated?.(res.data);

      form.resetFields();

    } catch (err) {
      const detail =
        err.response?.data?.detail ||
        err.response?.data?.error ||
        err.response?.data?.message;

      if (detail) {
        message.error(detail);
      } else {
        message.error("Ошибка при создании кампании");
      }
    }
  };

  return (
    <Modal
      title="Создать новую кампанию"
      open={open}
      onCancel={onCancel}
      okText="Создать"
      cancelText="Отмена"
      onOk={() => form.submit()}
    >
      <Form
        form={form}
        layout="vertical"
        onFinish={handleCreate}
        className="mt-2"
      >
        <Form.Item
          label="Название кампании"
          name="name"
          rules={[{ required: true, message: 'Введите название кампании' }]}
        >
          <Input placeholder="Например: Приветственная рассылка" />
        </Form.Item>

        <Form.Item
          label="Текст сообщения"
          name="text"
          rules={[{ required: true, message: 'Введите текст сообщения' }]}
        >
          <Input.TextArea rows={3} placeholder="Привет! Как дела?" />
        </Form.Item>

        <Form.Item
          label="Промпт (описание ассистента)"
          name="promt"
          rules={[{ required: true, message: 'Введите промпт' }]}
        >
          <Input.TextArea rows={2} placeholder="Ты — бизнес ассистент..." />
        </Form.Item>

        <Form.Item
          label="Список username (через запятую, без @)"
          name="usernames"
          rules={[{ required: true, message: 'Введите хотя бы одного пользователя' }]}
        >
          <Input placeholder="user1, user2, user3" />
        </Form.Item>
      </Form>
    </Modal>
  );
}
