import React from 'react';
import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Accounts from './pages/Accounts';
import Campaigns from './pages/Campaigns';
import CampaignDetails from './pages/CampaignDetails';
import DialogDetails from './pages/DialogDetails';
import PrivateRoute from './components/PrivateRoute';
import Auth from './pages/Auth';


function AppWrapper() {
  const location = useLocation();
  const hideHeader = location.pathname === '/login'; // скрываем Header на странице логина

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {!hideHeader && <Header />}

      <main className="flex-1 p-6">
        <Routes>
          <Route path="/login" element={<Auth />} />

          <Route path="/" element={
            <PrivateRoute>
              <Home />
            </PrivateRoute>
          } />
          <Route path="/accounts" element={
            <PrivateRoute>
              <Accounts />
            </PrivateRoute>
          } />
          <Route path="/campaigns" element={
            <PrivateRoute>
              <Campaigns />
            </PrivateRoute>
          } />
          <Route path="/campaigns/:id" element={
            <PrivateRoute>
              <CampaignDetails />
            </PrivateRoute>
          } />
          <Route path="/dialogs/:id" element={
            <PrivateRoute>
              <DialogDetails />
            </PrivateRoute>
          } />

          <Route path="*" element={<div>404 — страница не найдена</div>} />
        </Routes>
      </main>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppWrapper />
    </BrowserRouter>
  );
}
