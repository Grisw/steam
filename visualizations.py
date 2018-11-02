import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pymysql

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False


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


def show_top_10(cursor):
    results = select("SELECT * FROM games order by total_reviews desc limit 10", cursor)
    names = []
    good_reviews = []
    bad_reviews = []
    total_reviews = []
    reviews_percent = []
    for row in results:
        names.append(row[1])
        good_reviews.append(row[2] * row[3] * 0.01)
        bad_reviews.append(row[2] * (100 - row[3]) * 0.01)
        total_reviews.append(row[2])
        reviews_percent.append(row[3] * 0.01)

    x = range(len(results))
    p1 = plt.bar(x, height=good_reviews, width=0.45, alpha=0.8, color='red', label="好评")
    p2 = plt.bar(x, height=bad_reviews, width=0.45, color='green', label="中差评", bottom=good_reviews)
    plt.xticks(range(len(results)), names, rotation=30, horizontalalignment='right')
    plt.title("最受关注的前10名评价对比")
    plt.legend((p1[0], p2[0]), ('好评', '中差评'))
    for x, y in enumerate(total_reviews):
        plt.text(x, y + 100, '%.2f' % reviews_percent[x], horizontalalignment='center')
    plt.show()


def show_f_tags(cursor):
    results = select("SELECT tags.name, sum(total_reviews) FROM games inner join game_tags on games.id = game_tags.game_id inner join tags on game_tags.tag_id = tags.id group by tag_id order by sum(total_reviews) desc limit 10", cursor)
    tags = []
    total_reviews = []
    for row in results:
        tags.insert(0, row[0])
        total_reviews.insert(0, row[1])

    x = range(len(results))
    plt.barh(x, total_reviews, height=0.5, color='steelblue', alpha=0.8)
    plt.yticks(x, tags)
    plt.title("最受欢迎的10大类型")
    plt.show()


def show_reviews_dis(cursor):
    results = select("SELECT reviews_percent, count(*) FROM steam.games where reviews_percent <> 0 and reviews_percent <> 100 group by reviews_percent", cursor)
    rp = []
    count = []
    for row in results:
        rp.append(row[0])
        count.append(row[1])

    plt.plot(rp, count)
    plt.title("好评率分布")
    plt.show()


def show_price_dis(cursor):
    results = select("SELECT price, count(*) FROM steam.games where price < 200 group by price", cursor)
    rp = []
    count = []
    for row in results:
        rp.append(row[0])
        count.append(row[1])

    plt.plot(rp, count)
    plt.title("价格分布")
    plt.show()


def main():
    db, cursor = connectdb()
    show_price_dis(cursor)
    closedb(db)


if __name__ == '__main__':
    main()
