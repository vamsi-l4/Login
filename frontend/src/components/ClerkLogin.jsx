import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Mail } from 'react-feather';
import { useSignIn } from '@clerk/clerk-react';
import './ClerkAuth.css';

const ClerkLogin = () => {
  const navigate = useNavigate();
  const { signIn, isLoaded } = useSignIn();
  const [email, setEmail] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [emailError, setEmailError] = useState('');

  const validateForm = () => {
    let isValid = true;
    setEmailError('');

    if (!email) {
      setEmailError('Email is required');
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      setEmailError('Please enter a valid email address');
      isValid = false;
    }

    return isValid;
  };

  const handleSendOTP = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setEmailError('');

    if (!validateForm()) return;
    if (!isLoaded) return;

    setLoading(true);
    try {
      // Send email code for verification
      await signIn.create({
        strategy: 'email_code',
        identifier: email,
      });

      // Save email to localStorage for OTP verification page
      localStorage.setItem('email', email);
      localStorage.setItem('signInId', signIn.id);

      setErrorMsg('OTP sent to your email! Redirecting...');
      setTimeout(() => navigate('/verify-otp'), 2000);
    } catch (error) {
      let serverMsg = 'Failed to send OTP. Please try again.';
      if (error?.errors?.[0]?.message) {
        serverMsg = error.errors[0].message;
      } else if (error.message.includes('not found')) {
        serverMsg = 'Email not found. Please check or sign up first.';
      }
      setErrorMsg(serverMsg);
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
            Welcome Back to <span className="logo-text">RedIron</span>
          </h2>
          <form onSubmit={handleSendOTP}>
            <div className="input-group">
              <Mail className="input-icon" size={18} />
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  if (emailError) setEmailError('');
                }}
                required
                className={emailError ? 'error' : ''}
              />
              {emailError && <p className="field-error">{emailError}</p>}
            </div>
            {errorMsg && <p className="error">{errorMsg}</p>}
            <button className="button" type="submit" disabled={loading || !isLoaded}>
              {loading ? 'Sending OTP...' : 'Send OTP to Email'}
            </button>
          </form>
          <p className="footer-text">
            Don't have an account?{" "}
            <span onClick={() => navigate("/signup")}>Signup</span>
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default ClerkLogin;