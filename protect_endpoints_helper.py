# Helper script to add authentication to remaining endpoints
# This script will be used to quickly protect all remaining endpoints

ENDPOINTS = ["bank.py", "distance.py", "parameter.py", "posting.py", "state.py"]

AUTH_IMPORTS = """from app.application.auth.dependencies import get_current_user
from app.domain.user import User"""

AUTH_PARAM = ", current_user: User = Depends(get_current_user)"

print("Add these imports to each endpoint file:")
print(AUTH_IMPORTS)
print("\nAdd this parameter to each route function:")
print(AUTH_PARAM)
