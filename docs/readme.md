## Heroku
[Heroku Document](https://devcenter.heroku.com/articles/getting-started-with-python)

Use the heroku login command to log in to the Heroku CLI:
```
heroku login
```

Clone the application
```
git clone git@github.com:pocoweb/mindful-poc1.git
cd mindful-poc1
```

Deploy the app
```
heroku git:remote -a mindful-ucb
```

View logs
```
heroku logs --tail
```

Connect to the remote database and see all the rows
```
heroku pg:psql
```

Deploy your change
```
git add .
git commit -m "Demo"
git push heroku master:master
```

Finally, check that everything is working:
```
heroku open
```
