import graphene

class Query(CRMQuery, graphene.ObjectType):
    pass


class Mutation(CRMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation) 
