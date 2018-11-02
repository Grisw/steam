import pymysql
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
import random


def connectdb():
    db = pymysql.connect("localhost", "root", "lxt514335188", "steam")
    cursor = db.cursor()
    return db, cursor


def select(sql, cursor):
    cursor.execute(sql)
    results = cursor.fetchall()
    return results


def closedb(db):
    db.close()


def run(name, model, x, y, x_test, y_test):
    model.fit(x, y)
    score = model.score(x_test, y_test)
    predictions = model.predict(x_test)
    plt.figure()
    plt.plot(range(len(y_test)), y_test, 'go-', label='true value')
    plt.plot(range(len(predictions)), predictions, 'ro-', label='predict value')
    plt.title('%s, score: %.2f' % (name, score))
    plt.legend()
    plt.show()
    for i, prediction in enumerate(predictions):
        print('%s Predicted: %s, Target: %s' % (name, prediction, y_test[i]))
    print('%s squared: %.2f' % (name, score))


if __name__ == '__main__':
    db, cursor = connectdb()
    ids = select("SELECT id, price FROM steam.games", cursor)
    X = []
    y = []
    # X_test = []
    # y_test = []

    for c, row in enumerate(ids):
        tags = select(f"SELECT tag_id FROM steam.game_tags where game_id = {row[0]}", cursor)
        p = [0] * 7
        for i, tag in enumerate(tags):
            p[i] = tag[0]
        X.append(p)
        y.append(row[1])
        # if c < 22600:
        #     X.append(p)
        #     y.append(row[1])
        # else:
        #     X_test.append(p)
        #     y_test.append(row[1])

    X_test = [[], [], [], []]
    y_test = []
    n_test = [[], [], [], []]
    tgs = select("SELECT id, name FROM steam.tags", cursor)
    for d in range(0, 4):
        for i in range(0, 7):
            p = random.choice(tgs)
            X_test[d].append(p[0])
            n_test[d].append(p[1])
        y_test.append(0)
    print(n_test)
    closedb(db)

    # X_test = [[1662, 1774, 3859, 1775, 1663, 3814, 19],
    #           [19, 122, 21, 4667, 4345, 3859, 176981],
    #           [493, 1663, 19, 5055, 1774, 493, 4182],
    #           [87, 1027, 0, 0, 0, 0, 0],
    #           [19, 113, 4667, 597, 9, 492, 599],
    #           [493, 128, 19, 493, 122, 1662, 1718],
    #           [492, 21, 122, 4085, 10397, 1664, 3871],
    #           [493, 176981, 493, 128, 19, 1662, 1663],
    #           [599, 492, 19, 701, 1774, 1663, 4182],
    #           [87, 5055, 8013, 0, 0, 0, 0],
    #           [19, 597, 9, 128, 492, 1662, 176981],
    #           [493, 493, 599, 597, 9, 492, 4175],
    #           [1659, 113, 1662, 3859, 1695, 128, 1663]]
    # y_test = [98, 17, 21, 22, 0, 37, 6, 68, 18, 18, 0, 22, 0]
    # y_test = [49, 15, 86, 94, 54, 58, 98, 52, 50, 80, 68, 82, 48]


    # ####3.1决策树回归####
    # from sklearn import tree
    # model_DecisionTreeRegressor = tree.DecisionTreeRegressor()
    # run('决策树回归', model_DecisionTreeRegressor, X, y, X_test, y_test)
    # ####3.2线性回归####
    # from sklearn import linear_model
    # model_LinearRegression = linear_model.LinearRegression()
    # run('线性回归', model_LinearRegression, X, y, X_test, y_test)
    # ####3.3SVM回归####
    # from sklearn import svm
    # model_SVR = svm.SVR()
    # run('SVM回归', model_SVR, X, y, X_test, y_test)
    # ####3.4KNN回归####
    # from sklearn import neighbors
    # model_KNeighborsRegressor = neighbors.KNeighborsRegressor()
    # run('KNN回归', model_KNeighborsRegressor, X, y, X_test, y_test)
    # ####3.6Adaboost回归####
    # from sklearn import ensemble
    # model_AdaBoostRegressor = ensemble.AdaBoostRegressor(n_estimators=50)  # 这里使用50个决策树
    # run('Adaboost回归', model_AdaBoostRegressor, X, y, X_test, y_test)
    ####3.7GBRT回归####
    from sklearn import ensemble
    model_GradientBoostingRegressor = ensemble.GradientBoostingRegressor(n_estimators=100)  # 这里使用100个决策树
    run('GBRT回归', model_GradientBoostingRegressor, X, y, X_test, y_test)
    # ####3.8Bagging回归####
    # from sklearn.ensemble import BaggingRegressor
    # model_BaggingRegressor = BaggingRegressor()
    # run('Bagging回归', model_BaggingRegressor, X, y, X_test, y_test)
    # ####3.9ExtraTree极端随机树回归####
    # from sklearn.tree import ExtraTreeRegressor
    # model_ExtraTreeRegressor = ExtraTreeRegressor()
    # run('ExtraTree极端随机树回归', model_ExtraTreeRegressor, X, y, X_test, y_test)
    # ####3.5随机森林回归####
    # from sklearn import ensemble
    # model_RandomForestRegressor = ensemble.RandomForestRegressor(n_estimators=20)  # 这里使用20个决策树
    # run('随机森林回归', model_RandomForestRegressor, X, y, X_test, y_test)
