library(xtable)
games = read.csv('/Users/Jake/Documents/Classes/MATH410/final_project/season17.csv')


# Preprocessing
names(games) = c("X", "X2PFG", "X3PFG", "Assists", "Blocks", "D.Reb", "FT", "O.Reb", "PF", "Steals", "Turnovers", "WLR", "Season.Day", "T1.GB", "T2.GB", "T1", "T1.Score", "T2", "T2.Score", "Tournament")

games['X2PFG'] = games['X2PFG'] + games['X3PFG']
names(games)[2] = 'FG'
games = games[, !(names(games) %in% c('X', 'X3PFG'))]


meta_cols = names(games)[11:length(names(games))]  # meta column names
games_meta = games[meta_cols]  # meta table
games = games[!(names(games) %in% meta_cols)] # remove meta columns

#Response Variables:
spread = games_meta[,'T1.Score'] - games_meta[,'T2.Score'] #  Point Spread
winner = rep(2, length(spread))
winner[spread > 0] = 1

# Number of 2's is far greater than number of 1's. These must be even. 
winner_dist = data.frame(table(winner))
num_change = round((winner_dist[2, 'Freq'] -  winner_dist[1, 'Freq'])/2)
changed = 0
idx = 1
while(changed < num_change) {
  while(winner[idx] != 2) {
    idx = idx + 1
  }
  games[idx,] = games[idx,] * -1
  temp_df = games_meta[idx, c('T1', 'T1.Score', 'T1.GB')]
  games_meta[idx, c('T1', 'T1.Score', 'T1.GB')] = games_meta[idx, c('T2', 'T2.Score', 'T2.GB')]
  games_meta[idx, c('T2', 'T2.Score', 'T2.GB')] = temp_df
  winner[idx] = 1
  spread[idx] = spread[idx] * -1
  changed = changed + 1
  idx = idx + 1
}

#Shuffle data
shuffle = sample(1:nrow(games))
games = games[shuffle,]
games_meta = games_meta[shuffle,]
winner = winner[shuffle]
spread = spread[shuffle]

print(xtable(games[1:5, c("FG", "FT", "Assists", "Blocks", "WLR")],
             caption="Subset of Game Stats Data"))
print(xtable(games_meta[1:5, c("T1", "T1.Score", "T2", "T2.Score", "Tournament")],
             caption="Subset of Game Meta Data"))


library(boot)
games = data.frame(games, spread)  # Linear Regression
lm.fit = lm(spread~., data=games)
s = summary(lm.fit)
rmse = (sum(s$residuals^2)/length(s$residuals))^0.5

print(xtable(s, caption="Summary of All-Variable Linear Model Fit"))


#Variable Selection
library(leaps)
regforward = regsubsets(spread~., data=games, nvmax=10, method="forward")
outmat_df = data.frame(summary(regforward)$outmat)
print(xtable(outmat_df, caption="Forward Stepwise Selection"))


#F-tests
wlr_fit = lm(spread~WLR, data=games)
assists_fit = lm(spread~WLR+Assists, data=games)
turnovers_fit = lm(spread~WLR+Assists+Turnovers, data=games)
blocks_fit = lm(spread~WLR+Assists+Turnovers+Blocks, data=games)
oreb_fit = lm(spread~WLR+Assists+Turnovers+Blocks+O.Reb, data=games)
pf_fit = lm(spread~WLR+Assists+Turnovers+Blocks+O.Reb+PF, data=games)
dreb_fit = lm(spread~WLR+Assists+Turnovers+Blocks+O.Reb+PF+D.Reb, data=games)
steals_fit = lm(spread~WLR+Assists+Turnovers+Blocks+O.Reb+PF+D.Reb+Steals, data=games)
ft_fit = lm(spread~WLR+Assists+Turnovers+Blocks+O.Reb+PF+D.Reb+Steals+FT, data=games)
fg_fit = lm(spread~WLR+Assists+Turnovers+Blocks+O.Reb+PF+D.Reb+Steals+FT+FG, data=games)
aov_fits = anova(wlr_fit, assists_fit, turnovers_fit, blocks_fit, oreb_fit, pf_fit, dreb_fit, steals_fit, ft_fit, fg_fit)
print(xtable(aov_fits, caption="Analysis of Variance"))


#Test logistic regression
indicies = sample(1:nrow(games), I(2/3)*nrow(games))
games = games[, !(names(games) %in% c('spread'))]
games['winner'] = winner
split.fit = glm((winner-1)~WLR+Assists+Turnovers+Blocks+O.Reb, data=games[indicies,], family='binomial')
preds = predict(split.fit, newdata=games[-indicies,], type='response')
r.preds = round(preds)
t = table(games[-indicies,]$winner, r.preds)
xtable(t, caption="Winner v. Predictions Confusion Matrix")

#Visualize logistic regression
plot(games[-indicies,]$WLR, games[-indicies,]$winner-1, col='blue', xlab='Win Loss Ratio', ylab='Winner - 1')
points(games[-indicies,]$WLR, preds)
plt.fit = glm((winner-1)~WLR, data=games[indicies,], family='binomial')
ndf = data.frame(WLR=seq(min(games$WLR), max(games$WLR), len=100))
ndf$win.min1 = predict(plt.fit, newdata=ndf, type='response')
lines(win.min1~WLR, ndf, col='red', lwd=2)
legend(-1, 0.3, legend=c("Prediction Curve", "Winner - 1", "Predictions"),
       col=c('red', 'blue', 'black'), lty=c(1, NA, NA), pch=c(NA, 16, 16))


#KNN
library('class')
training_size = round(I(2/3)*max(games_meta$Season.Day))
knn.preds = 1:50
for(i in seq(1, 100, 2)) {
  knn.pred = knn(games[games_meta$Season.Day <= training_size,],
                 games[games_meta$Season.Day > training_size,],
                 games[games_meta$Season.Day <= training_size,]$winner,
                 k=i)
  t = table(games[games_meta$Season.Day > training_size,]$winner, knn.pred)
  knn.preds[ceiling(i/2)] = ((t[1, 1]+t[2, 2])/sum(t))*100
}

optimal_k = which.max(knn.preds)
plot(seq(1, 100, 2), knn.preds, xlab="K", ylab="Test Set Accuracy", main="Figure 1. Finding the Optimal K")