import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Home } from "./pages/Home"
import { Settings } from "./pages/Settings"
import React, { Component, useState } from 'react';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import PreferencesPage from './pages/Preferences';
import RegistrationSuccess from './components/RegisterSuccess';
import NotFound from './components/NotFound';

export function App() {
  return (
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<Home />} />
        <Route path="/settings" element={<Settings />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/preferences" element={<PreferencesPage />} />
        <Route path="/registersuccess" element={<RegistrationSuccess />} />
        <Route path="*"  element={<NotFound />}/>
        
      </Routes>
  )
}

export default App;
