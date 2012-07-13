from flask.ext.script import Command, Option, prompt_pass


class CreateUserCommand(Command):
    "  Create a user. "

    option_list = (
        Option('username'),
        Option('email'),
        Option('-a', '--active', dest='active', action='store_true'),
        Option('-p', '--password', dest='password', default=''),
    )

    def run(self, username=None, email=None, active=False, password=''):
        from base.users.models import User
        from base.ext import db

        password = password or prompt_pass("Set password")
        user = User(username=username,
                        email=email,
                        pw_hash=password,
                        active=active)

        db.session.add(user)
        db.session.commit()

        print 'User created successfully.'


class CreateRoleCommand(Command):
    "  Create a role. "

    option_list = (
        Option('name'),
    )

    def run(self, name=None):
        from base.users.models import Role
        from base.ext import db
        role = Role(name=name)

        db.session.add(role)
        db.session.commit()

        print 'Role "%s" created successfully.' % name


class AddRoleCommand(Command):
    "  Add a role to a user. "

    option_list = (
        Option('username'),
        Option('role'),
    )

    def run(self, username=None, role=None):
        from base.users.models import User, Role
        from base.ext import db
        u = User.query.filter_by(username=username).first()
        r = Role.query.filter_by(name=role).first()
        if u and r:
            u.roles.append(r)
            db.session.add(u)
            db.session.commit()
            print "Role '%s' added to user '%s' successfully" % (role, username)


class RemoveRoleCommand(Command):
    "  Remove a role from user. "

    option_list = (
        Option('username'),
        Option('role'),
    )

    def run(self, username=None, role=None):
        from base.users.models import User, Role
        from base.ext import db
        u = User.query.filter_by(username=username).first()
        r = Role.query.filter_by(name=role).first()
        if r in u.roles:
            u.roles.remove(r)
            db.session.add(u)
            db.session.commit()
        print "Role '%s' removed from user '%s' successfully" % (role, username)
