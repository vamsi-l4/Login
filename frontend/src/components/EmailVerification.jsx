import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const EmailVerification = () => {
  const [otp, setOtp] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const email = localStorage.getItem('email');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/api/accounts/verify-email/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, otp }),
      });
      if (response.ok) {
        navigate('/login');
      } else {
        const data = await response.json();
        setError(data.error || 'Verification failed');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center">Email Verification</h2>
        {error && <p className="text-red-500 mb-4">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700">Verification Code</label>
            <input
              type="text"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              className="w-full px-3 py-2 border rounded"
              required
            />
          </div>
          <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">
            Verify
          </button>
        </form>
      </div>
    </div>
  );
};

export default EmailVerification;
