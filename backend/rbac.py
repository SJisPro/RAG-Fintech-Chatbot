role_permissions = {
    "finance": ["finance", "general"],
    "marketing": ["marketing", "general"],
    "hr": ["hr", "general"],
    "engineering": ["engineering", "general"],
    "executive": ["finance", "marketing", "hr", "engineering", "general"],
    "employee": ["general"]
}

def is_authorized(role, doc_category):
    return doc_category in role_permissions.get(role, [])
