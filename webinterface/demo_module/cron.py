from .models import Inbound_teststand_package

# Explanation:
# This function will be called and run when the crontab scheduler runs. The run schedule is defined in "settings.py"
# "testdatabase.objects" gets the different objects from the database "testdatabase"
# ".filter(NODELETE=False)"  checks the NODELETE fields value
# ".delete()" If the field NODELETE is "False" th object will be deleted

def Database_clean_up():
    print("Running Cron, whatup bitches...")
    Inbound_teststand_package.objects.filter(NODELETE=False).delete()
