import React from 'react';
import './style/App.css';
import Dashboard from "./components/Dashboard";

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
            <div className="App" data-testid={"app"}>
                <header className="App-header">
                    <Dashboard/>
                </header>
            </div>
        </AppProvider>
    );
}

export default App;
