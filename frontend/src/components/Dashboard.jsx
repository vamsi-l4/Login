import { UserButton, useAuth, useUser } from "@clerk/clerk-react";
import axios from "axios";
import "./Dashboard.css";

function Dashboard() {
  const { getToken } = useAuth();
  const { user } = useUser();

  const callBackend = async () => {
    try {
      const token = await getToken();

      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/accounts/protected/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      alert(JSON.stringify(response.data, null, 2));
    } catch (error) {
      alert('Error calling backend: ' + error.message);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Welcome to <span className="brand">RedIron</span></h1>
          <p className="subtitle">You are logged in</p>
        </div>
        <UserButton afterSignOutUrl="/login" />
      </div>

      <div className="dashboard-content">
        <div className="dashboard-card">
          <h2>Your Profile</h2>
          <div className="profile-info">
            <p><strong>Email:</strong> {user?.emailAddresses[0]?.emailAddress}</p>
            <p><strong>Username:</strong> {user?.username || 'Not set'}</p>
            <p><strong>Name:</strong> {user?.fullName || 'Not set'}</p>
          </div>
        </div>

        <div className="dashboard-card">
          <h2>Protected API Call</h2>
          <p>Test your backend connection with a protected endpoint</p>
          <button className="btn-primary" onClick={callBackend}>
            Call Backend (Protected)
          </button>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
