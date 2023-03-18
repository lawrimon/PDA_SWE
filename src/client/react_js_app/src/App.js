import './App.css';
import logo from './cAPItan_Logo.jpg';
import { Route, Routes } from "react-router-dom"
import { Home } from "./pages/Home"
import { Settings } from "./pages/Settings"
import React, { useState } from 'react';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import PreferencesPage from './pages/Preferences';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/settings" element={<Settings />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path ="/register" element={<RegisterPage/>}/>
      <Route path ="/preferences" element={<PreferencesPage/>}/>

    </Routes>
  )
}
export default App