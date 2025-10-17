import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ApplicationForm from './components/ApplicationForm';
import ApplicationResult from './components/ApplicationResult';


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ApplicationForm />} />
        <Route path="/result" element={<ApplicationResult />} />
      </Routes>
    </Router>
  );
}

export default App;
