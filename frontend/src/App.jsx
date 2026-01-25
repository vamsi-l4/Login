import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SignedIn, SignedOut } from "@clerk/clerk-react";
import Dashboard from "./components/Dashboard";
import ClerkLogin from "./components/ClerkLogin";
import ClerkSignup from "./components/ClerkSignup";
import ClerkOTP from "./components/ClerkOTP";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <>
              <SignedIn>
                <Dashboard />
              </SignedIn>
              <SignedOut>
                <ClerkLogin />
              </SignedOut>
            </>
          }
        />
        <Route path="/login" element={<ClerkLogin />} />
        <Route path="/verify-otp" element={<ClerkOTP />} />
        <Route path="/signup" element={<ClerkSignup />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
