import React, {useState, useEffect} from 'react';
import './style/App.css';
import {io} from "socket.io-client";
import Dashboard from "./components/Dashboard";

import {SERVER_ENDPOINT} from "./config/config"

import {AppProvider} from "./context/context";

// const [response, setResponse] = useState("");
//
// useEffect(() => {
//     const socket = io(SERVER_ENDPOINT);
//     socket.on("FromAPI", data => {
//         setResponse(data);
//     });
// }, []);


const App = () => {
    return (
        <AppProvider>
            <div className="App">
                <header className="App-header">
                    <Dashboard />
                </header>
            </div>
        </AppProvider>
    );
}

export default App;
