## AUN
Official Website of HUST Student Association Union
## deploy
1. third party
    1. pip3 install -r requirements.txt
2. database init
    1. python manage.py db init
    2. python manage.py db migrate
    3. python manage.py db upgrade
3. create super user    
    1. python manage.py create_super_role
    2. python manage.py create_super_user -n name -p password -e email
    
4. test data
    1. python manage.py create_test_items 

