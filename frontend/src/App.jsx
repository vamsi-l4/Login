import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Signup from './components/Signup';
import EmailVerification from './components/EmailVerification';
import Login from './components/Login';
import OTP from './components/OTP';
import Success from './components/Success';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Signup />} />
        <Route path="/verify-email" element={<EmailVerification />} />
        <Route path="/login" element={<Login />} />
        <Route path="/otp" element={<OTP />} />
        <Route path="/success" element={<Success />} />
      </Routes>
    </Router>
  );
}

export default App;
