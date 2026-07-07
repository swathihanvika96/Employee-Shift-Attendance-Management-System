from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.employee import Employee
from app.schemas.user import UserRegister
from app.utils.hashing import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.logger import logger


class AuthService:

    @staticmethod
    def register(db: Session, user: UserRegister):

        try:
            print("========== REGISTER DEBUG ==========")
            print("STEP 1 : Register API Called")
            print("Request:", user.model_dump())

            # Check existing email
            existing_user = (
                db.query(User)
                .filter(User.email == user.email)
                .first()
            )

            print("STEP 2 : Email Check Completed")

            if existing_user:
                print("Email already exists")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            # Validate employee for Employee role
            if user.role == "Employee":

                print("STEP 3 : Employee Role")

                if user.employee_id is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="employee_id is required"
                    )

                employee = (
                    db.query(Employee)
                    .filter(
                        Employee.id == user.employee_id,
                        Employee.is_active == True
                    )
                    .first()
                )

                print("STEP 4 : Employee Validation Completed")

                if not employee:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Employee not found"
                    )

            print("STEP 5 : Hashing Password")

            hashed_pwd = hash_password(user.password)

            print("STEP 6 : Password Hashed")

            db_user = User(
                username=user.username,
                email=user.email,
                hashed_password=hashed_pwd,
                role=user.role,
                employee_id=user.employee_id,
                is_active=True
            )

            print("STEP 7 : User Object Created")

            db.add(db_user)

            print("STEP 8 : User Added to Session")

            db.commit()

            print("STEP 9 : Commit Successful")

            db.refresh(db_user)

            print("STEP 10 : Refresh Successful")

            logger.info(f"User Registered : {user.email}")

            print("========== REGISTER SUCCESS ==========")

            return db_user

        except HTTPException:
            raise

        except Exception as e:
            db.rollback()

            print("\n========== REGISTER ERROR ==========")
            print("ERROR TYPE :", type(e).__name__)
            print("ERROR :", str(e))
            print("====================================\n")

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ):

        try:
            print("========== LOGIN DEBUG ==========")

            user = (
                db.query(User)
                .filter(User.email == email)
                .first()
            )

            print("STEP 1 : User Query Completed")

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )

            print("STEP 2 : User Found")

            if not verify_password(password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )

            print("STEP 3 : Password Verified")

            token = create_access_token(
                data={
                    "sub": user.email,
                    "role": user.role,
                    "employee_id": user.employee_id
                }
            )

            print("STEP 4 : Token Created")

            logger.info(f"User Login : {user.email}")

            return {
                "access_token": token,
                "token_type": "bearer"
            }

        except HTTPException:
            raise

        except Exception as e:
            print("\n========== LOGIN ERROR ==========")
            print("ERROR TYPE :", type(e).__name__)
            print("ERROR :", str(e))
            print("=================================\n")

            raise HTTPException(
                status_code=500,
                detail=str(e)
            )