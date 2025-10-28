from app import create_app
from app.extensions import db, socketio
from app.utils.db_migrations import ensure_deleted_at_columns

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Ensure optional columns exist for older databases (adds `deleted_at` for sqlite)
        ensure_deleted_at_columns(app)
    # Run without the interactive debugger to avoid the PIN-locked console in background runs
    socketio.run(app, debug=False, host='0.0.0.0', port=5001, allow_unsafe_werkzeug=True)
