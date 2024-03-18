from django.contrib.auth.models import Permission

def remove_duplicate_permissions(codename):
    try:
        # Retrieve all permissions with the given codename
        permissions = Permission.objects.filter(codename=codename)
        
        # If there are multiple permissions, keep only one and delete the rest
        if permissions.count() > 1:
            # Keep the first permission and delete the rest
            duplicate_permissions = permissions[1:]
            for permission in duplicate_permissions:
                permission.delete()
                print(f"Duplicate permission '{permission.codename}' deleted.")
    except Exception as e:
        print(f"An error occurred while removing duplicate permissions: {str(e)}")
