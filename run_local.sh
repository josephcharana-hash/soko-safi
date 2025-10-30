#!/bin/bash

echo "Starting Soko Safi Local Development..."

# Start backend server
echo "Starting backend server on http://127.0.0.1:5001"
cd server
python3 local_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "Starting frontend server on http://127.0.0.1:5173"
cd ../client
npm run dev &
FRONTEND_PID=$!

echo "Servers started!"
echo "Backend: http://127.0.0.1:5001"
echo "Frontend: http://127.0.0.1:5173"
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait