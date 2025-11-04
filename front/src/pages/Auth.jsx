import React, { useState } from 'react';
import { Form, Input, Button, message, Card, Tabs } from 'antd';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';

const { TabPane } = Tabs;

export default function Auth() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleLogin = async (values) => {
    setLoading(true);
    try {
      const res = await api.login(values);
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('username', values.username);
      message.success('Успешный вход');
      navigate('/');
    } catch (err) {
      message.error('Неверный логин или пароль');
    } finally {
      setLoading(false);
    }
  };

    const handleRegister = async (values) => {
    setLoading(true);
    try {
        const res = await api.register(values);

        // Если сервер вернул 200, считаем регистрацию успешной
        message.success('Успешная регистрация! Теперь войдите в систему.');
        navigate('/login'); // переключение на страницу логина
    } catch (err) {
        // Обработка ошибок
        if (err.response && err.response.data && err.response.data.detail) {
        message.error(err.response.data.detail); // сообщение от сервера
        } else {
        message.error('Ошибка регистрации');
        }
    } finally {
        setLoading(false);
    }
    };


  return (
    <div className="flex justify-center items-center h-screen bg-gray-50">
      <Card title="Авторизация" className="w-96">
        <Tabs defaultActiveKey="login">
          <TabPane tab="Вход" key="login">
            <Form layout="vertical" onFinish={handleLogin}>
              <Form.Item
                label="Логин"
                name="username"
                rules={[{ required: true, message: 'Введите логин' }]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Пароль"
                name="password"
                rules={[{ required: true, message: 'Введите пароль' }]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} block>
                  Войти
                </Button>
              </Form.Item>
            </Form>
          </TabPane>

          <TabPane tab="Регистрация" key="register">
            <Form layout="vertical" onFinish={handleRegister}>
              <Form.Item
                label="Логин"
                name="username"
                rules={[{ required: true, message: 'Введите логин' }]}
              >
                <Input />
              </Form.Item>

              <Form.Item
                label="Пароль"
                name="password"
                rules={[{ required: true, message: 'Введите пароль' }]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item
                label="Код приглашения"
                name="invite_code"
                rules={[{ required: true, message: 'Введите код приглашения' }]}
              >
                <Input />
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} block>
                  Зарегистрироваться
                </Button>
              </Form.Item>
            </Form>
          </TabPane>
        </Tabs>
      </Card>
    </div>
  );
}
