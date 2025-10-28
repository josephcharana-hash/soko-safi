# Soko Safi - Production Deployment Guide

## Prerequisites
- PostgreSQL database
- Python 3.8+
- Node.js 16+
- Domain with SSL certificate

## Backend Deployment

### 1. Environment Setup
```bash
cd server
cp .env.example .env
```

Edit `.env` with production values:
- Set strong `SECRET_KEY`
- Configure PostgreSQL `DATABASE_URL`
- Add production domain to `ALLOWED_ORIGINS`
- Configure M-Pesa credentials
- Set `FLASK_ENV=production`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Migration
```bash
flask db upgrade
python create_admin.py  # Create admin user
```

### 4. Run with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5001 --worker-class eventlet main:app
```

## Frontend Deployment

### 1. Environment Setup
```bash
cd client
cp .env.example .env.production
```

Edit `.env.production`:
- Set `VITE_API_URL` to your backend URL

### 2. Build
```bash
npm install
npm run build
```

### 3. Deploy
Upload `dist/` folder to your hosting service (Netlify, Vercel, etc.)

## Production Checklist

### Security
- [ ] Change SECRET_KEY to random string
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Remove debug endpoints
- [ ] Set secure session cookies

### Performance
- [ ] Enable gzip compression
- [ ] Use CDN for static files
- [ ] Configure database connection pooling
- [ ] Set up caching (Redis)

### Monitoring
- [ ] Set up error logging (Sentry)
- [ ] Configure health checks
- [ ] Monitor database performance
- [ ] Set up uptime monitoring

### Backup
- [ ] Automated database backups
- [ ] File upload backups
- [ ] Environment variable backups

## Recommended Hosting

### Backend
- Railway
- Render
- Heroku
- AWS EC2

### Frontend
- Vercel
- Netlify
- AWS S3 + CloudFront

### Database
- Railway PostgreSQL
- AWS RDS
- DigitalOcean Managed Database
