from fastapi import Depends, HTTPException
from starlette import status

from app.api.dependencies.users import get_current_user
from app.db.models import User


def PermissionChecker(required_perms: list[str]):
    def checker(current_user: User = Depends(get_current_user)):
        user_permissions = {perm.name for perm in current_user.role.permissions}

        print(f"{user_permissions=}")
        if not any(p in user_permissions for p in required_perms):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )
        return current_user

    return checker
