import graphene
import json
import uuid
from datetime import datetime

class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()

class User(graphene.ObjectType):
    id = graphene.ID(default_value=uuid.uuid4())
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return f'https://cloudinary.com/{self.username.lower()}/{self.id}'


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()

    def resolve_hello(self,info):
        return "world"

    def resolve_is_admin(self, info): 
        return True

    def resolve_users(self, info, limit=None): 
        return [
            User(id=uuid.uuid4(), username="Rupert", created_at=datetime.now()),
            User(id=uuid.uuid4(), username="Cedric", created_at=datetime.now()),
            User(id=uuid.uuid4(), username="Baby", created_at=datetime.now())
        ][:limit]
    
class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()
    
    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)

class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)
    class Arguments:
        title = graphene.String()
        content = graphene.String()

    def mutate(self, info, title, content):
        
        if info.context.get('is_anonymous'):
            raise Exception('Not authenticated!')

        post = Post(title=title, content=content)
        return CreatePost(post=post)

class Mutation(graphene.ObjectType): 
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

query_result = schema.execute(
    '''
    query getUsersQuery ($limit: Int) {
        users(limit: $limit) {
            id
            username
            createdAt
            avatarUrl
        }
    }
    ''',
    # variable_values={ 'limit': 2 }
)

mutation_result = schema.execute(
    '''
    mutation ($username: String!) {
        createUser(username: $username) {
            user{
                id
                username
                createdAt
            }
        }
    }
    ''',
    variable_values={ 'username': 'Pooka' }
)

mutation_post = schema.execute(
     '''
    mutation {
        createPost(title: "hello", content: "world") {
            post {
                title
                content
            }
        }
    }
    ''',
    # variable_values={ 'username': 'Pooka' }
    # context={ 'is_anonymous': True }
)

dict_query_result = dict(query_result.data.items())
# dict_mutation_result = dict(mutation_result.data.items())
# dict_mutation_post = dict(mutation_post.data.items())

print(json.dumps(dict_query_result,indent=2))
# print(json.dumps(dict_mutation_result,indent=2))
# print(json.dumps(dict_mutation_post,indent=2))