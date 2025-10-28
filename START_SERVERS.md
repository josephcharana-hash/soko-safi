# How to Start Soko Safi Application

## Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- All dependencies installed

## Start Backend (Flask Server)

Open Terminal 1:
```bash
cd server
python main.py
```

Expected output:
```
 * Running on http://0.0.0.0:5001
```

## Start Frontend (React + Vite)

Open Terminal 2:
```bash
cd client
npm run dev
```

Expected output:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

## Access Application

Open browser and go to: **http://localhost:5173**

## Troubleshooting

### Backend not starting:
1. Check if `.env` file exists in `server/` directory
2. Ensure database is configured: `DATABASE_URL=sqlite:///soko_safi.db`
3. Install dependencies: `pip install -r requirements.txt`

### Frontend showing "Backend server not responding":
1. Ensure Flask server is running on port 5001
2. Check terminal for Flask server errors
3. Verify proxy is configured in `vite.config.js`

### 404 errors on API calls:
- Backend server must be running BEFORE starting frontend
- Restart frontend if backend was started after

## Quick Start (Both Servers)

You can use this command to start both in one terminal (Linux/Mac):
```bash
cd server && python main.py & cd ../client && npm run dev
```

Or use two separate terminals as described above (recommended).
