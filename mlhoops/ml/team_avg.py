from mlhoops.db import session
from mlhoops.models import Team, Season, Game
from mlhoops.ml.normalize import feature_scaling

from sqlalchemy import and_, or_

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense


teams = session().query(Team).filter(Team.season_id == 15,
                                     Team.made_tournament == True).all()
print("Number of tournament teams: {}".format(len(teams)))
team_ids = []
team_data = []
for team in teams:
    team_ids.append(team.id)
    team_data.append(team.get_data()[1])
team_data = {team_ids[i]: row for i, row in enumerate(feature_scaling(team_data))}

tour_cond = and_(Game.tournament_id != None, Game.season_id == 15)
season_cond = and_(Game.tournament_id == None,
                   Game.season_id == 15,
                   or_(Game.team_one.in_(team_ids),
                       Game.team_two.in_(team_ids)))

tour_games = session().query(Game).filter(tour_cond).all()
season_games = session().query(Game).filter(season_cond).all()
print("Number of tournament games: {}".format(len(tour_games)))
print("Number of season games: {}".format(len(season_games)))

training_X = []
training_Y = []
for game in season_games:
    training_X.append(team_data[game.team_one] + team_data[game.team_two])
    training_Y.append(0 if game.team_one_score > game.team_two_score else 1)

testing_X = []
testing_Y = []
for game in tour_games:
    testing_X.append(team_data[game.team_one] + team_data[game.team_two])
    testing_Y.append(0 if game.team_one_score > game.team_two_score else 1)

num_attrs = len(testing_X[0])
model = Sequential()
model.add(Dense(num_attrs*2, input_dim=num_attrs, activation='relu'))
model.add(Dense(num_attrs*2, activation='relu'))
model.add(Dense(num_attrs, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
print("Hyperparameters: {}".format(['Layers: 3',
                                    [num_attrs*2, num_attrs*2, num_attrs],
                                    'Loss: mean_squared_error',
                                    'Optimizer: sgd']))

model.compile(loss='mean_squared_error', optimizer='sgd', metrics=['accuracy'])

model.fit(training_X, training_Y)
print(model.evaluate(testing_X, testing_Y))
