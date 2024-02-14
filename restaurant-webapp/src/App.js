import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './components/Login';
import HomePage from './components/HomePage';
import Menu from './components/Menu'
import Order from './components/Orders'
import OrderHistory from './components/OrderHistory'
import MultiActionAreaCard from './components/card/newqCard';


const App = () => {
    return (
        <Router>
            <div>
                <Navbar />
                <Routes>
                <Route path="/" element={<Login />} />
                    <Route path="/login" element={<Login />} />
                    <Route path="/home" element={<HomePage />} />
                    <Route path="/menu" element={<Menu />} />
                    <Route path="/orders" element={<Order />} />
                    <Route path="/history" element={<OrderHistory />} />
                    <Route path="/card" element={<MultiActionAreaCard name={"Burger"} cost={40}  quantity={10} imageUrl={"https://images.themodernproper.com/billowy-turkey/production/posts/2023/ShrimpChowMein_11.jpg?w=800&q=82&fm=jpg&fit=crop&dm=1683035122&s=77863530cd58ad17b88df8041ef94e1d"} />} />

                    {/* Add routes for other pages */}
                </Routes>
            </div>
        </Router>
    );
}

export default App;
