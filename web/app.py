import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin, ModelView

from db import db
from db.models import User, Group, Controller, Social
from web.provider import UsernameAndPasswordProvider

app = Starlette()

admin = Admin(db._engine,
              title="Example: SQLAlchemy",
              base_url='/',
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key="qewrerthytju4")])




class AllModelView(ModelView):
    exclude_fields_from_create = ["created_at" , 'updated_at' , "products"]


admin.add_view(AllModelView(User))
admin.add_view(AllModelView(Controller))
admin.add_view(AllModelView(Group))
admin.add_view(AllModelView(Social))


admin.mount_to(app)

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)


