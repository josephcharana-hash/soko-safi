# Authentication & Authorization Test Guide

## Test the Integration

### 1. Start Both Servers

**Terminal 1 - Backend:**
```bash
cd server
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd client
npm run dev
```

### 2. Test Registration

1. Go to `http://localhost:5173/register`
2. Fill in the form:
   - Full Name: Test User
   - Email: test@example.com
   - Password: Test1234
   - Role: Select Buyer or Artisan
3. Click "Sign Up"
4. Should redirect to dashboard based on role

### 3. Test Login

1. Go to `http://localhost:5173/login`
2. Enter credentials:
   - Email: test@example.com
   - Password: Test1234
3. Click "Log in"
4. Should redirect to appropriate dashboard

### 4. Test Authentication State

1. After login, check Navbar:
   - Should show user icon
   - Should show logout button
   - Should show cart and messages icons
2. Try accessing protected routes:
   - `/cart` - Should work when logged in
   - `/buyer-dashboard` or `/artisan-dashboard` - Should work when logged in

### 5. Test Logout

1. Click logout button in Navbar
2. Should redirect to login page
3. Try accessing `/cart` - Should prompt to login

### 6. Test Session Persistence

1. Login successfully
2. Refresh the page
3. Should remain logged in (session persists)

## Backend API Endpoints

### Auth Endpoints:
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/session` - Check session status
- `GET /api/auth/profile` - Get user profile (requires auth)

### Test with curl:

**Register:**
```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test1234",
    "full_name": "Test User",
    "role": "buyer"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "test@example.com",
    "password": "Test1234"
  }'
```

**Check Session:**
```bash
curl -X GET http://localhost:5001/api/auth/session \
  -b cookies.txt
```

## What's Working:

✅ User registration with password hashing (bcrypt)
✅ User login with session creation
✅ Session-based authentication (Flask-Session)
✅ Protected routes with @require_auth decorator
✅ Role-based access control with @require_role decorator
✅ Frontend AuthContext for state management
✅ API service for backend communication
✅ CORS enabled for cross-origin requests
✅ Automatic session checking on app load
✅ Logout functionality
✅ Navbar updates based on auth state
