import './App.css';
import logo from './cAPItan_Logo.jpg';
import { Route, Routes } from "react-router-dom"
import { Home } from "./pages/Home"
import { Settings } from "./pages/Settings"
import React, { useState } from 'react';

export function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  )
}
export default App