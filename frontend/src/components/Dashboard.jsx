import { UserButton, useAuth } from "@clerk/clerk-react";
import axios from "axios";

function Dashboard() {
  const { getToken } = useAuth();

  const callBackend = async () => {
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
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Dashboard</h1>
      <UserButton />
      <br /><br />
      <button onClick={callBackend}>
        Call Backend (Protected)
      </button>
    </div>
  );
}

export default Dashboard;
