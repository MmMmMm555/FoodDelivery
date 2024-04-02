from django.core.cache import cache



def email_check_verified(uuid, email) -> bool:
    key = f"{email}_{uuid}"
    data = cache.get(key)
    if data and data['verified']:
        cache.delete(key)
        return True
    return False