#!/bin/sh
# Make migrations for all models
python manage.py makemigrations subawardBackend

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Check if superuser already exists for the custom user model
if [ "$(python manage.py shell -c 'from subawardBackend.models import CustomUser; print(CustomUser.objects.filter(username=os.environ["DJANGO_SUPERUSER_USERNAME"]).exists())')" = "False" ]; then
    # Create a superuser (if needed)
    if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]; then
        python manage.py createsuperuser --noinput
    else
        echo "Missing environment variables for superuser creation."
    fi
else
    echo "Superuser already exists."
fi 

# Start the application
gunicorn --bind=0.0.0.0:8000 subawardsApp.wsgi:application --log-level DEBUG --error-logfile /var/log/gunicorn/error.log --access-logfile /var/log/gunicorn/access.log
