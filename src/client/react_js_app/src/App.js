import './App.css';
import logo from './cAPItan_Logo.jpg';
//import { Route, Routes } from "react-router-dom"
import { BrowserRouter as Router, Routes, Switch, Route } from 'react-router-dom';
import { Home } from "./pages/Home"
import { Settings } from "./pages/Settings"
import React, { useState } from 'react';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import PreferencesPage from './pages/Preferences';
import RegistrationSuccess from './pages/RegisterSuccess';

export function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<Home />} />
      <Route path="/settings" element={<Settings />} />
      <Route path ="/register" element={<RegisterPage/>}/>
      <Route path ="/preferences" element={<PreferencesPage/>}/>
      <Route path ="/registersuccess" element={<RegistrationSuccess/>}/>
    </Routes>
  )
}
export default App