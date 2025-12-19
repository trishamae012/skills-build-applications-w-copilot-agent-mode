
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):

        # Use pymongo to clear collections directly to avoid Djongo ORM issues
        db = connection.cursor().db_conn.client['octofit_db']
        db['octofit_tracker_leaderboard'].delete_many({})
        db['octofit_tracker_activity'].delete_many({})
        db['octofit_tracker_workout'].delete_many({})
        db['octofit_tracker_user'].delete_many({})
        db['octofit_tracker_team'].delete_many({})


        # Create teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Team')
        dc = Team.objects.create(name='DC', description='DC Team')

        # Create users
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)

        # Create activities
        Activity.objects.bulk_create([
            Activity(user=tony, type='Running', duration=30, date=timezone.now().date()),
            Activity(user=steve, type='Cycling', duration=45, date=timezone.now().date()),
            Activity(user=bruce, type='Swimming', duration=60, date=timezone.now().date()),
            Activity(user=clark, type='Yoga', duration=20, date=timezone.now().date()),
        ])

        # Create workouts
        w1 = Workout.objects.create(name='Full Body', description='Full body workout')
        w2 = Workout.objects.create(name='Cardio Blast', description='Intense cardio')
        w1.suggested_for.set([tony, bruce])
        w2.suggested_for.set([steve, clark])

        # Create leaderboard
        Leaderboard.objects.bulk_create([
            Leaderboard(user=tony, score=100),
            Leaderboard(user=steve, score=90),
            Leaderboard(user=bruce, score=95),
            Leaderboard(user=clark, score=85),
        ])

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
