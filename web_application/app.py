# http://pycrud-app.herokuapp.com/account




# Import modules required to perform sqLite commands to create and fetch existing data from the sqlite flaskApp.db files

# from forms import RegistrationForm
# from flask_login import *



# # Create a connection with the local sqlite database file.
# engine = create_engine('sqlite:///flaskApp.db', echo=False)
# # Check and create new tables with defined schema from Models/model.py file
# metadata.create_all(engine, checkfirst=True)


# def do_insert():
#     stmt = insert(users).values(
#         Name='mayank', 
#         Email='Arnold', 
#         Password='2000-01-31',
#         Role='2000-01-31',
#         CurrentTeam='2000-01-31')
    
#     with engine.begin() as con:
#         result = con.execute(stmt)
#         x = result.inserted_primary_key['Id']
#     return result.inserted_primary_key['Id']

# def do_insert_skill(userId):
#     stmt = insert(skills).values(
#         UserId=userId,
#         SkillName='SkillName', 
#         SkillRating=1)
    
#     with engine.begin() as con:
#         result = con.execute(stmt)
#     return result.inserted_primary_key['Id']

# def do_insert_comment(userId):
#     stmt = insert(comments).values(
#         UserId=userId,
#         Comments='Id qui enim ipsum sit laboris reprehenderit ex dolore ullamco tempor consequat aliqua. Sint ut amet amet et laborum fugiat culpa cillum minim. Mollit dolor labore pariatur commodo laborum eiusmod ex. Veniam Lorem tempor sunt deserunt mollit non cillum commodo laboris do voluptate in. Qui officia eiusmod ut culpa eiusmod laborum sint officia esse dolor.')
    
#     with engine.begin() as con:
#         result = con.execute(stmt)
#     return result.inserted_primary_key['Id']

# createdUser=do_insert()
# do_insert_skill(createdUser)
# do_insert_comment(createdUser)


