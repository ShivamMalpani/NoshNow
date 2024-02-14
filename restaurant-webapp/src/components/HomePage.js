import React from 'react';
import './HomePage.css'; // Import CSS file for styling

const HomePage = () => {
    return (
        <div className="homepage">
            <div className="background-image" />
            <div className="content">
                <h1 className="heading">Welcome to Your Restaurant Dashboard</h1>
                <p>You are proud to serve delicious meals at our restaurant located at IIT Bhilai.</p>
                <p>Manage all your restaurant activities with this web app.</p>
                <br></br>
                <>Made with ❤️ by Team HASO</>
            </div>
        </div>
    );
}

export default HomePage;
