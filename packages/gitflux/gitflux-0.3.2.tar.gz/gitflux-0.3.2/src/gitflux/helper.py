from github.AuthenticatedUser import AuthenticatedUser
from github.Organization import Organization


def parse_repo_fullname(user: AuthenticatedUser, orgs: list[Organization], fullname: str) -> tuple:
    if fullname.find('/') == -1:
        owner = user
        repo_name = fullname
    else:
        org_name, repo_name = fullname.split('/')

        if org_name == user.login:
            owner = user
        else:
            owner = next((x for x in orgs if x.login == org_name), None)

        if owner is None:
            raise NameError(f'Organization not found: {org_name}.')

    return owner, repo_name
