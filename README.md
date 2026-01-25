# RedIron - Login Frontend with Clerk Authentication

A modern, beautifully designed authentication system using **Clerk** for backend authentication and a custom **RedIron gym-themed UI**.

## 🎨 Design Features

- **Glass-Morphism Design**: Modern frosted glass effect with backdrop blur
- **Dark Gym Theme**: Professional dark background with red accent colors
- **Animated Elements**: Smooth animations using Framer Motion
- **Gym Silhouette**: Muscleman image with drop-shadow effects
- **Video Background**: Dynamic video background with brightness filter
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop
- **Form Validation**: Real-time validation with helpful error messages
- **Password Visibility Toggle**: Show/hide password with eye icon

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- Clerk account (free at https://clerk.dev)

### Installation

1. **Run the setup script** (Windows):
```bash
setup-frontend.bat
```

Or manually:
```bash
cd frontend
npm install
```

2. **Set up environment variables** (`.env`):
```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
VITE_API_URL=http://localhost:8000
```

Get your Clerk key from: https://dashboard.clerk.dev

3. **Add assets to `public/` folder**:
   - `background1.mp4` - Background video
   - `muscleman.png` - Gym silhouette image

4. **Start the development server**:
```bash
npm run dev
```

Visit `http://localhost:5173` in your browser.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ClerkLogin.jsx          # Login page with Clerk
│   │   ├── ClerkSignup.jsx         # Signup page with email verification
│   │   ├── Dashboard.jsx           # User dashboard after login
│   │   ├── ClerkAuth.css           # Shared auth pages styling
│   │   └── Dashboard.css           # Dashboard styling
│   ├── App.jsx                     # Main app component
│   ├── main.jsx                    # App entry point (Clerk setup)
│   └── index.css                   # Global styles
├── public/
│   ├── background1.mp4             # Background video
│   └── muscleman.png               # Silhouette image
├── .env                            # Environment variables (create this)
├── .env.example                    # Example env variables
├── package.json                    # Dependencies
└── vite.config.js                  # Vite configuration
```

## 🔐 Authentication Flow

```
┌─────────────────────────────────────────┐
│        User Visits App (/)              │
└──────────────┬──────────────────────────┘
               │
        Is User Logged In?
              /│\
            /  │  \
           Y   │   N
          /    │    \
         /     │     \
    ┌────┐  ┌──────┐
    │ D  │  │Login │
    │ a  │  │ Page │
    │ s  │  └──────┘
    │ h  │     │
    │ b  │     └─→ User Enters Email
    │ o  │          & Password
    │ a  │              │
    │ r  │              ↓
    │ d  │         Clerk Auth API
    │    │              │
    └────┘              ↓
         ←─────────────────
         (Verified)
```

## 🎯 Pages

### Login Page (`/login`)
- Email and password inputs
- Password visibility toggle
- Remember Me checkbox
- Forgot password link
- Navigation to signup

### Signup Page (`/signup`)
- Username, email, password inputs
- Automatic email verification
- Password strength validation
- Navigation to login

### Dashboard (`/`)
- Shows user profile info
- Logout button (UserButton)
- Example protected API call

## 🔌 API Integration

The app includes an example of calling a protected backend:

```javascript
const callBackend = async () => {
  const token = await getToken();
  const response = await axios.get('/api/protected/', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
};
```

Your backend should verify the JWT token from Clerk.

## 📦 Dependencies

- **React 18.3** - UI framework
- **Vite 5.3** - Build tool
- **Clerk 5.59** - Authentication provider
- **Framer Motion 10.16** - Animation library
- **React Feather 2.0** - Icon library
- **Axios 1.13** - HTTP client
- **React Router 7.11** - Client routing
- **Tailwind CSS 4.1** - Utility CSS (optional)

## 🎬 Building for Production

```bash
npm run build
```

Creates an optimized production build in the `dist/` folder.

## 📱 Mobile Optimization

The design is fully responsive with breakpoints at:
- 480px (mobile phones)
- 768px (tablets)
- 1024px+ (desktop)

## 🐛 Troubleshooting

### "Missing Clerk Publishable Key"
- Check `.env` file exists and has correct key
- Restart dev server: `npm run dev`

### Video/Images not loading
- Ensure files are in `public/` folder (not `src/`)
- Check file names match exactly: `background1.mp4`, `muscleman.png`

### "Module not found" errors
- Delete `node_modules` folder
- Run `npm install` again

### Style not applying
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Check CSS import in components

## 🔑 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_CLERK_PUBLISHABLE_KEY` | Clerk public key | `pk_test_...` |
| `VITE_API_URL` | Backend API URL | `http://localhost:8000` |

## 📚 Resources

- **Clerk Docs**: https://clerk.dev/docs
- **React Router**: https://reactrouter.com
- **Framer Motion**: https://www.framer.com/motion
- **Vite**: https://vitejs.dev

## 🎨 Customization

### Change Theme Color
Update `ClerkAuth.css` - change all `red` values to your color:
```css
color: red;           /* Change to your color */
border-color: red;    /* Change to your color */
background-color: red;/* Change to your color */
```

### Change Brand Name
Update `ClerkLogin.jsx` and `ClerkSignup.jsx`:
```jsx
<h2>Welcome to <span className="logo-text">YourBrand</span></h2>
```

### Change Videos/Images
Replace files in `public/`:
- `background1.mp4` - New background video
- `muscleman.png` - New silhouette image

## 📄 License

This project uses Clerk for authentication services.

## ✅ Checklist Before Deployment

- [ ] Clerk credentials in `.env`
- [ ] Assets (video, image) in `public/` folder
- [ ] Backend API URL correct in `.env`
- [ ] Backend set up to verify Clerk JWT tokens
- [ ] Frontend builds without errors (`npm run build`)
- [ ] All pages tested in production mode (`npm run preview`)
- [ ] Mobile responsive design verified
- [ ] Clerk dashboard rules configured
- [ ] Domain/URL added to Clerk allowed origins

## 🚀 Deployment Options

### Vercel (Recommended)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm install -g netlify-cli
netlify deploy
```

### Docker
```bash
docker build -t rediron-frontend .
docker run -p 5173:5173 rediron-frontend
```

---

**Made with ❤️ for RedIron Gym**
