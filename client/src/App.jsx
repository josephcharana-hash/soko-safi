import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Components/Layout/Navbar';
import Sidebar from './Components/Layout/Sidebar';
import Footer from './Components/Layout/Footer';
import Dashboard from './Pages/Dashboard';
import Inventory from './Pages/Inventory';
import Sales from './Pages/Sales';
import Customers from './Pages/Customers';
import Reports from './Pages/Reports';
import Settings from './Pages/Settings';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <div className="flex pt-20">
          <Sidebar />
          <main className="flex-1 ml-72 p-8 min-h-screen flex flex-col">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/inventory" element={<Inventory />} />
              <Route path="/sales" element={<Sales />} />
              <Route path="/customers" element={<Customers />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="/settings" element={<Settings />} />
            </Routes>
            <Footer />
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App
