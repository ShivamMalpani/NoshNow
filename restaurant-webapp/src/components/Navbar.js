import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
    return (
        <nav className="navbar">
            <ul className="navbar-nav">
                {/* Use Link component to navigate to '/' */}
                <li className="nav-item"><Link to="/home">Home</Link></li>
                <li className="nav-item"><Link to="/menu">Menu</Link></li>
                <li className="nav-item"><Link to="/orders">Orders</Link></li>
                <li className="nav-item"><Link to="/history">Order History</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;
