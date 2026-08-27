from app.database import init_db, SessionLocal
from app import crud

def run():
    init_db()
    db = SessionLocal()
    try:
        admin_role = crud.create_role_if_not_exists(db, 'admin')
        user_role = crud.create_role_if_not_exists(db, 'user')
        # create default admin if not exists
        if not crud.get_user_by_email(db, 'admin@example.com'):
            admin = crud.create_user(db, 'admin@example.com', 'adminpass', full_name='Admin', role=admin_role)
            print('Created admin:', admin.email)
    finally:
        db.close()

if __name__ == '__main__':
    run()
