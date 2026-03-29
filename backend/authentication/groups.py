from django.contrib.auth.models import Group, Permission


def create_groups():
    """
    Create the four user role groups.
    Run this once when setting up the system.
    """

    # Create groups
    student_group, _ = Group.objects.get_or_create(name='Student')
    volunteer_group, _ = Group.objects.get_or_create(name='Volunteer')
    manager_group, _ = Group.objects.get_or_create(name='Manager')
    admin_group, _ = Group.objects.get_or_create(name='Admin')

    print("Groups created: Student, Volunteer, Manager, Admin")
    return {
        'student': student_group,
        'volunteer': volunteer_group,
        'manager': manager_group,
        'admin': admin_group,
    }