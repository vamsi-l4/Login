import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Lock, Mail } from 'react-feather';
import { useSignIn } from '@clerk/clerk-react';
import './ClerkAuth.css';

const ClerkOTP = () => {
  const navigate = useNavigate();
  const { signIn, isLoaded, setActive } = useSignIn();
  const [otp, setOtp] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [otpError, setOtpError] = useState('');
  const email = localStorage.getItem('email');

  const validateForm = () => {
    let isValid = true;
    setOtpError('');

    if (!otp) {
      setOtpError('OTP is required');
      isValid = false;
    } else if (otp.length < 6) {
      setOtpError('OTP should be 6 digits');
      isValid = false;
    }

    return isValid;
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setOtpError('');

    if (!validateForm()) return;
    if (!isLoaded) return;

    setLoading(true);
    try {
      // Attempt email code verification
      const completeSignIn = await signIn.attemptFirstFactor({
        strategy: 'email_code',
        code: otp,
      });

      if (completeSignIn.status === 'complete') {
        // Set the session
        await setActive({ session: completeSignIn.createdSessionId });
        
        setErrorMsg('✅ OTP verified! Login successful!');
        
        // Clear localStorage
        localStorage.removeItem('email');
        localStorage.removeItem('signInId');
        
        setTimeout(() => navigate('/'), 1500);
      } else {
        setErrorMsg('Verification failed. Please try again.');
      }
    } catch (error) {
      let serverMsg = 'OTP verification failed. Please check your code.';
      if (error?.errors?.[0]?.message) {
        serverMsg = error.errors[0].message;
      } else if (error.message.includes('expired')) {
        serverMsg = 'OTP has expired. Please request a new one.';
      } else if (error.message.includes('incorrect')) {
        serverMsg = 'Incorrect OTP. Please try again.';
      }
      setErrorMsg(serverMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleResendOTP = async () => {
    if (!isLoaded || !signIn) return;
    
    setLoading(true);
    setErrorMsg('');
    try {
      // Resend OTP
      await signIn.create({
        strategy: 'email_code',
        identifier: email,
      });
      setErrorMsg('✅ New OTP sent to your email!');
    } catch (error) {
      setErrorMsg('Failed to resend OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <video autoPlay muted loop className="background-video">
        <source src="/background1.mp4" type="video/mp4" />
      </video>
      <div className="auth-form-wrapper">
        <div className="glass-card-background"></div>
        <img src="/muscleman.png" alt="Gym Silhouette" className="silhouette" />
        <motion.div
          className="form-content"
          initial={{ opacity: 0, y: -60 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7 }}
        >
          <h2>
            Verify Your <span className="logo-text">OTP</span>
          </h2>
          <p className="verification-info">Enter the 6-digit code sent to</p>
          <p className="email-display">{email || 'your email'}</p>
          
          <form onSubmit={handleVerifyOTP}>
            <div className="input-group">
              <Lock className="input-icon" size={18} />
              <input
                type="text"
                placeholder="Enter 6-digit OTP"
                value={otp}
                onChange={(e) => {
                  // Only allow numbers, max 6 digits
                  const value = e.target.value.replace(/[^0-9]/g, '').slice(0, 6);
                  setOtp(value);
                  if (otpError) setOtpError('');
                }}
                maxLength="6"
                required
                className={otpError ? 'error' : ''}
                autoFocus
              />
              {otpError && <p className="field-error">{otpError}</p>}
            </div>
            
            {errorMsg && <p className={`error ${errorMsg.includes('✅') ? 'success' : ''}`}>{errorMsg}</p>}
            
            <button className="button" type="submit" disabled={loading || !isLoaded || otp.length < 6}>
              {loading ? 'Verifying...' : 'Verify OTP'}
            </button>
          </form>

          <div className="resend-section">
            <p className="footer-text">
              Didn't receive code?{" "}
              <span onClick={handleResendOTP} className={loading ? 'disabled' : ''}>
                Resend OTP
              </span>
            </p>
            <p className="back-text">
              <span onClick={() => navigate("/login")} className="back-link">
                ← Back to Login
              </span>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ClerkOTP;
