from run import app, db
from models import Users, Skills, Comments
# Password hashing.
from passlib.hash import sha256_crypt

def create_database_and_data():
    db.reflect()
    # db.drop_all()
    db.create_all()

    adminUser = db.session.query(Users).filter_by(
        email="mayank.patel@admin.com").first()

    standardUser = db.session.query(Users).filter_by(
        email="mayank.patel@standard.com").first()


    if not standardUser:
        newUser = Users(
            name="Mayank Patel Standard",
            email="mayank.patel@standard.com",
            password=sha256_crypt.encrypt("standard"),
            jobRole="Software Developer - Standard",
            currentTeam="NHS.UK - Service Profiles",
        )
        db.session.add(newUser)
        db.session.commit()

    if not adminUser:
        newUser = Users(
            name="Mayank Patel",
            email="mayank.patel@admin.com",
            password=sha256_crypt.encrypt("admin"),
            jobRole="Software Developer",
            currentTeam="NHS.UK - Service Profiles",
            userRole="Admin",
        )
        db.session.add(newUser)
        db.session.commit()

        registeredUser = db.session.query(Users).filter_by(
            email="mayank.patel@admin.com").first()

        skill_one = Skills(
            userId=registeredUser.id,
            skillName="Kubernetes",
            skillRating=5
        )
        skill_two = Skills(
            userId=registeredUser.id,
            skillName="C# dotnet",
            skillRating=4
        )
        comment = Comments(
            userId=registeredUser.id,
            comments="I also do performance testing for NHS.UK on varies Covid and Non-Covid related services."
        )

        db.session.add(comment)
        db.session.add(skill_one)
        db.session.add(skill_two)
        db.session.commit()
