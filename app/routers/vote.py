from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2, database
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

# select users.id, COUNT() from users RIGHT JOIN posts ON users.id = posts.owner_id group by users.id;
# select posts.id, posts.title, count(votes.post_id) from posts left join votes on posts.id = votes.post_id group by posts.id order by posts.id;


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # retrace le post dont il est question dans le vote
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    # si ce post n'existe pas
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist")

    # si le post existe, on cherche à savoir si le user a déjà voté sur ce post
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    # si le user inscrit un vote
    if (vote.dir == 1):

        # si un vote a été trouvé sur le post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")

        # si aucun vote a été trouvé, on l'inscrit
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    # si le user retire son vote
    else:
        # si aucun vote a été trouvé
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")

        # si le vote a été trouvé, on le retire
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
