from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    print("hello")
    # OAuth2PasswordRequestForm returns username and password
    # but it is ok, we can use the email for the username

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    # si le user n'existe pas
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials1")

    # si le mot de passe ne correspond pas à celui de la bd
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials2")

    # create token -- on peut ajouter "user_email" ou autre à data
    access_token = oauth2.create_access_token(
        data={"user_id": user.id})

    print(access_token)

    # return token
    return {"access_token": access_token, "token_type": "bearer"}
