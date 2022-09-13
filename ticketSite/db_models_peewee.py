from peewee import *

database = SqliteDatabase('db.sqlite3')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AuthGroup(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = 'auth_group'

class DjangoContentType(BaseModel):
    app_label = CharField()
    model = CharField()

    class Meta:
        table_name = 'django_content_type'
        indexes = (
            (('app_label', 'model'), True),
        )

class AuthPermission(BaseModel):
    codename = CharField()
    content_type = ForeignKeyField(column_name='content_type_id', field='id', model=DjangoContentType)
    name = CharField()

    class Meta:
        table_name = 'auth_permission'
        indexes = (
            (('content_type', 'codename'), True),
        )

class AuthGroupPermissions(BaseModel):
    group = ForeignKeyField(column_name='group_id', field='id', model=AuthGroup)
    permission = ForeignKeyField(column_name='permission_id', field='id', model=AuthPermission)

    class Meta:
        table_name = 'auth_group_permissions'
        indexes = (
            (('group', 'permission'), True),
        )

class AuthUser(BaseModel):
    date_joined = DateTimeField()
    email = CharField()
    first_name = CharField()
    is_active = BooleanField()
    is_staff = BooleanField()
    is_superuser = BooleanField()
    last_login = DateTimeField(null=True)
    last_name = CharField()
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        table_name = 'auth_user'

class AuthUserGroups(BaseModel):
    group = ForeignKeyField(column_name='group_id', field='id', model=AuthGroup)
    user = ForeignKeyField(column_name='user_id', field='id', model=AuthUser)

    class Meta:
        table_name = 'auth_user_groups'
        indexes = (
            (('user', 'group'), True),
        )

class AuthUserUserPermissions(BaseModel):
    permission = ForeignKeyField(column_name='permission_id', field='id', model=AuthPermission)
    user = ForeignKeyField(column_name='user_id', field='id', model=AuthUser)

    class Meta:
        table_name = 'auth_user_user_permissions'
        indexes = (
            (('user', 'permission'), True),
        )

class DjangoAdminLog(BaseModel):
    action_flag = IntegerField()
    action_time = DateTimeField()
    change_message = TextField()
    content_type = ForeignKeyField(column_name='content_type_id', field='id', model=DjangoContentType, null=True)
    object_id = TextField(null=True)
    object_repr = CharField()
    user = ForeignKeyField(column_name='user_id', field='id', model=AuthUser)

    class Meta:
        table_name = 'django_admin_log'

class DjangoMigrations(BaseModel):
    app = CharField()
    applied = DateTimeField()
    name = CharField()

    class Meta:
        table_name = 'django_migrations'

class DjangoSession(BaseModel):
    expire_date = DateTimeField(index=True)
    session_data = TextField()
    session_key = CharField(primary_key=True)

    class Meta:
        table_name = 'django_session'

class SqliteSequence(BaseModel):
    name = BareField(null=True)
    seq = BareField(null=True)

    class Meta:
        table_name = 'sqlite_sequence'
        primary_key = False

class TicketAppTicket(BaseModel):
    active = BooleanField()
    assignee = ForeignKeyField(column_name='assignee_id', field='id', model=AuthUser, null=True)
    compartment = CharField()
    created_at = DateTimeField()
    description = TextField()
    status = CharField()
    title = CharField()
    updated_at = DateTimeField()

    class Meta:
        table_name = 'ticketApp_ticket'

class TicketAppUsercreate(BaseModel):
    active = BooleanField()
    compartment = CharField()
    user_ptr = ForeignKeyField(column_name='user_ptr_id', field='id', model=AuthUser, primary_key=True)

    class Meta:
        table_name = 'ticketApp_usercreate'

