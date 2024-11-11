from django.core.management.base import BaseCommand
from django.db import connection, IntegrityError, transaction
from meetups.models import Users  # Import your custom Users model

class Command(BaseCommand):
    help = "Migrate data from auth_user to meetups_users"

    def handle(self, *args, **kwargs):
        migrated_count = 0
        errors = []

        # Raw SQL query to fetch all data from auth_user
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, username, first_name, last_name, email, password, is_staff, is_superuser, is_active FROM auth_user")
            old_users = cursor.fetchall()

        for old_user in old_users:
            user_id, username, first_name, last_name, email, password, is_staff, is_superuser, is_active = old_user
            try:
                # Start a transaction for each user to ensure atomicity
                with transaction.atomic():
                    # Check if a user with the same email already exists in meetups_users
                    if Users.objects.filter(email=email).exists():
                        self.stdout.write(
                            self.style.WARNING(f"User with email {email} already exists. Skipping.")
                        )
                        continue

                    # Create a new user in meetups_users with the data from auth_user
                    new_user = Users(
                        email=email,
                        name=first_name,
                        surname=last_name,
                        password=password,  # Copy hashed password directly
                        is_staff=is_staff,
                        is_superuser=is_superuser,
                        is_active=is_active,
                    )

                    # Save the new user to meetups_users
                    new_user.save()
                    migrated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Successfully migrated user: {email}"))

            except IntegrityError as e:
                errors.append(f"Error migrating user {email}: {e}")
                self.stderr.write(self.style.ERROR(f"Error migrating user {email}: {e}"))

        # Final output
        self.stdout.write(self.style.SUCCESS(f"Migration completed. Total users migrated: {migrated_count}"))
        if errors:
            self.stdout.write(self.style.ERROR("Errors encountered:"))
            for error in errors:
                self.stdout.write(self.style.ERROR(error))
