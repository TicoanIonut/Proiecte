# coding: utf-8
from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, ForeignKey, Index, Integer, String, Table, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AuthGroup(Base):
    __tablename__ = 'auth_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)


class AuthUser(Base):
    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)
    password = Column(String(128), nullable=False)
    last_login = Column(DateTime)
    is_superuser = Column(Boolean, nullable=False)
    username = Column(String(150), nullable=False)
    last_name = Column(String(150), nullable=False)
    email = Column(String(254), nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime, nullable=False)
    first_name = Column(String(150), nullable=False)


class TicketAppUsercreate(AuthUser):
    __tablename__ = 'ticketApp_usercreate'

    user_ptr_id = Column(ForeignKey('auth_user.id'), primary_key=True)
    active = Column(Boolean, nullable=False)
    compartment = Column(String(25), nullable=False)


class DjangoContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = (
        Index('django_content_type_app_label_model_76bd3d3b_uniq', 'app_label', 'model', unique=True),
    )

    id = Column(Integer, primary_key=True)
    app_label = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)


class DjangoMigration(Base):
    __tablename__ = 'django_migrations'

    id = Column(Integer, primary_key=True)
    app = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    applied = Column(DateTime, nullable=False)


class DjangoSession(Base):
    __tablename__ = 'django_session'

    session_key = Column(String(40), primary_key=True)
    session_data = Column(Text, nullable=False)
    expire_date = Column(DateTime, nullable=False, index=True)


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class AuthPermission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = (
        Index('auth_permission_content_type_id_codename_01ab375a_uniq', 'content_type_id', 'codename', unique=True),
    )

    id = Column(Integer, primary_key=True)
    content_type_id = Column(ForeignKey('django_content_type.id'), nullable=False, index=True)
    codename = Column(String(100), nullable=False)
    name = Column(String(255), nullable=False)

    content_type = relationship('DjangoContentType')


class AuthUserGroup(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = (
        Index('auth_user_groups_user_id_group_id_94350c0c_uniq', 'user_id', 'group_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, index=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    user = relationship('AuthUser')


class DjangoAdminLog(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = (
        CheckConstraint('"action_flag" >= 0)'),
    )

    id = Column(Integer, primary_key=True)
    action_time = Column(DateTime, nullable=False)
    object_id = Column(Text)
    object_repr = Column(String(200), nullable=False)
    change_message = Column(Text, nullable=False)
    content_type_id = Column(ForeignKey('django_content_type.id'), index=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, index=True)
    action_flag = Column(Integer, nullable=False)

    content_type = relationship('DjangoContentType')
    user = relationship('AuthUser')


class TicketAppTicket(Base):
    __tablename__ = 'ticketApp_ticket'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    status = Column(String(25), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    assignee_id = Column(ForeignKey('auth_user.id'), index=True)
    compartment = Column(String(25), nullable=False)
    active = Column(Boolean, nullable=False)

    assignee = relationship('AuthUser')


class AuthGroupPermission(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = (
        Index('auth_group_permissions_group_id_permission_id_0cd325b0_uniq', 'group_id', 'permission_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    group_id = Column(ForeignKey('auth_group.id'), nullable=False, index=True)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    group = relationship('AuthGroup')
    permission = relationship('AuthPermission')


class AuthUserUserPermission(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = (
        Index('auth_user_user_permissions_user_id_permission_id_14a6b632_uniq', 'user_id', 'permission_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('auth_user.id'), nullable=False, index=True)
    permission_id = Column(ForeignKey('auth_permission.id'), nullable=False, index=True)

    permission = relationship('AuthPermission')
    user = relationship('AuthUser')
