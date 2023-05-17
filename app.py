from datetime import datetime

from flask import render_template, request, flash, redirect, url_for

from models import Posts  # если * - все будет импортироваться
from settings import app, db


@app.route("/")
def home():
    """
    Показывает главную страницу сайта

    :return: шаблон главной страницы со всеми заметками
    """

    all_posts: list[Posts] = Posts.query.all()

    print(type(all_posts))
    print(all_posts)

    return render_template("home.html", posts=all_posts)


@app.route("/post/<int:post_id>")
def show_post(post_id: int):
    """
    Функция для отправки содержимого одной заметки

    :param post_id: Идентификатор заметки в БД (int)
    :return: шаблон заметки
    """

    # Если нет по такому id заметки - будет 404
    post: Posts = db.get_or_404(Posts, post_id, description="Неверно указан id поста")

    return render_template("show_post.html", post=post)


@app.route("/create", methods=("GET", "POST"))
def create_post():

    if request.method == "POST":

        # Получаем данные от пользователя
        title = request.form["title"]
        content = request.form["text"]

        # print(f"title: '{title}'")
        # print(f"title: '{content}'")

        if not title or not content:
            flash("Укажите заголовок и содержимое!")

        else:
            post = Posts(
                title=title,
                content=content,
                created=datetime.now()
            )
            db.session.add(post)  # Добавляем в таблицу
            db.session.commit()  # Подтверждаем

        return render_template("create_post.html")


@app.route("/post/<int:post_id>/edit", methods=("GET", "POST"))
def edit_post(post_id: int):
    # Если нет по такому id заметки - будет 404
    post: Posts = db.get_or_404(Posts, post_id, description="Неверно указан id поста")

    if request.method == "POST":

        # Получаем изменения от пользователя, которые он хочет сохранить для заметки
        title = request.form["title"]
        content = request.form["text"]

        if not title or not content:
            flash("Необходимо указать заголовок и содержимое!")

        else:
            # Меняем поля
            post.title = title
            post.content = content

            db.session.add(post)  # Обновляем запись
            db.session.commit()  # Подтверждаем

            return redirect(url_for("show_post", post_id=post.id))  # возвращает объект ответа

    return render_template("edit_post.html", post=post)


@app.route("/post/<int:post_id>/delete", methods=("GET", "POST"))
def delete_post(post_id):
    post: Posts = db.get_or_404(Posts, post_id, description="Неверно указан id поста")

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("delete_post.html", post=post)


if __name__ == '__main__':
    # Создаем таблицы
    with app.app_context():
        db.create_all()

    app.run()
