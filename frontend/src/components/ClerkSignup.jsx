import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { User, Mail, Lock, Eye, EyeOff } from 'react-feather';
import { useSignUp } from '@clerk/clerk-react';
import './ClerkAuth.css';

const ClerkSignup = () => {
  const navigate = useNavigate();
  const { signUp, isLoaded } = useSignUp();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [pendingVerification, setPendingVerification] = useState(false);
  const [code, setCode] = useState('');
  const [errorMsg, setErrorMsg] = useState('');
  const [loading, setLoading] = useState(false);
  const [usernameError, setUsernameError] = useState('');
  const [emailError, setEmailError] = useState('');
  const [passwordError, setPasswordError] = useState('');

  const validateForm = () => {
    let isValid = true;
    setUsernameError('');
    setEmailError('');
    setPasswordError('');

    if (!username) {
      setUsernameError('Username is required');
      isValid = false;
    }

    if (!email) {
      setEmailError('Email is required');
      isValid = false;
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      setEmailError('Please enter a valid email address');
      isValid = false;
    }

    if (!password) {
      setPasswordError('Password is required');
      isValid = false;
    } else if (password.length < 6) {
      setPasswordError('Password must be at least 6 characters');
      isValid = false;
    }

    return isValid;
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setUsernameError('');
    setEmailError('');
    setPasswordError('');

    if (!validateForm()) return;
    if (!isLoaded) return;

    setLoading(true);
    try {
      await signUp.create({
        emailAddress: email,
        password: password,
        username: username,
      });

      await signUp.prepareEmailAddressVerification({ strategy: 'email_code' });
      setPendingVerification(true);
      setErrorMsg('Verification code sent to your email!');
    } catch (error) {
      let serverMsg = 'Signup failed. Please try again.';
      if (error?.errors?.[0]?.message) {
        serverMsg = error.errors[0].message;
      } else if (error.message.includes('duplicate')) {
        serverMsg = 'Email already exists. Please use a different email.';
      }
      setErrorMsg(serverMsg);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyEmail = async (e) => {
    e.preventDefault();
    if (!code) {
      setErrorMsg('Please enter verification code');
      return;
    }

    setLoading(true);
    try {
      const completeSignUp = await signUp.attemptEmailAddressVerification({ code });

      if (completeSignUp.status === 'complete') {
        setErrorMsg('Email verified! Account created successfully!');
        setTimeout(() => navigate('/'), 2000);
      }
    } catch (error) {
      let serverMsg = 'Verification failed. Please check your code.';
      if (error?.errors?.[0]?.message) {
        serverMsg = error.errors[0].message;
      }
      setErrorMsg(serverMsg);
    } finally {
      setLoading(false);
    }
  };

  if (pendingVerification) {
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
              Verify Your <span className="logo-text">Email</span>
            </h2>
            <p className="verification-info">Check your email for verification code</p>
            <form onSubmit={handleVerifyEmail}>
              <div className="input-group">
                <Mail className="input-icon" size={18} />
                <input
                  type="text"
                  placeholder="Enter verification code"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  required
                />
              </div>
              {errorMsg && <p className="error">{errorMsg}</p>}
              <button className="button" type="submit" disabled={loading}>
                {loading ? 'Verifying...' : 'Verify Email'}
              </button>
            </form>
          </motion.div>
        </div>
      </div>
    );
  }

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
            Join <span className="logo-text">RedIron</span>
          </h2>
          <form onSubmit={handleSignup}>
            <div className="input-group">
              <User className="input-icon" size={18} />
              <input
                type="text"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => {
                  setUsername(e.target.value);
                  if (usernameError) setUsernameError('');
                }}
                required
                className={usernameError ? 'error' : ''}
              />
              {usernameError && <p className="field-error">{usernameError}</p>}
            </div>
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
            <div className="input-group">
              <Lock className="input-icon" size={18} />
              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  if (passwordError) setPasswordError('');
                }}
                required
                className={passwordError ? 'error' : ''}
              />
              <span
                className="toggle-icon"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
              </span>
              {passwordError && <p className="field-error">{passwordError}</p>}
            </div>
            {errorMsg && <p className="error">{errorMsg}</p>}
            <button className="button" type="submit" disabled={loading || !isLoaded}>
              {loading ? 'Creating Account...' : 'Signup'}
            </button>
          </form>
          <p className="footer-text">
            Already have an account?{" "}
            <span onClick={() => navigate("/login")}>Login</span>
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default ClerkSignup;