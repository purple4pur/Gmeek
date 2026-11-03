**[简体中文](README.md)** | **[English](README-en.md)** | **Русский**
# Gmeek

Gmeek — генератор статических блогов и лёгкий шаблон личного блога. Он использует `GitHub Pages`, `GitHub Issues` и `GitHub Actions`. Локальный сервер не нужен. Создайте репозиторий и пишите в Issue.

Этот репозиторий — форк [Meekdai/Gmeek](https://github.com/Meekdai/Gmeek). В нём зависимости управляются через uv, результаты сборки кэшируются по времени обновления Issue, а ссылки относительные.

- [Демо](http://meekdai.github.io/)
- [Журнал обновлений](https://meekdai.github.io/post/Gmeek-geng-xin-ri-zhi.html)
- [Начало работы](https://blog.meekdai.com/post/Gmeek-kuai-su-shang-shou.html)

![dark](img/dark.jpg)

## Как это работает

Каждый Issue с меткой становится статьей. Gmeek читает Issues и метки, преобразует Markdown в HTML и записывает результат в `docs/`. Шаблоны создают главную страницу, страницы пагинации, страницу меток, RSS и карту сайта.

- GitHub Actions собирает и публикует сайт при создании или изменении Issue.
- Статьи с неизменившимся временем обновления пропускают повторную сборку.
- Относительные ссылки работают на `XXX.github.io` и на `XXX.github.io/repo`.
- Комментарии используют [utteranc.es](https://utteranc.es/) и загружаются после нажатия.
- Только владелец репозитория может задавать параметры статьи.

## Установка

1. Создайте репозиторий из [шаблона Gmeek](https://github.com/new?template_name=Gmeek-template&template_owner=Meekdai). Используйте имя `XXX.github.io`, где `XXX` — ваше имя пользователя GitHub.

2. В `Settings` откройте `Pages->Build and deployment->Source` и выберите `GitHub Actions`.

3. Откройте Issue и начните писать. Добавьте хотя бы одну метку. Сохраните Issue. Через некоторое время статья будет доступна по адресу `https://XXX.github.io`.

4. Для полной пересборки запустите `Actions->build Gmeek->Run workflow`. Сделайте это после изменения `config.json` или при ошибке.

## Настройка

Поместите `config.json` в корень репозитория блога. Минимальный файл:

```json
{
  "title": "Мой блог",
  "subTitle": "Заметки о коде и жизни",
  "avatarUrl": "https://example.com/avatar.jpg"
}
```

Если `homeUrl`, `displayTitle`, `faviconUrl` и `ogImage` отсутствуют, Gmeek выводит их сам. Все поля, значения по умолчанию и параметры статей описаны в [CONFIG.md](CONFIG.md). CONFIG.md написан на китайском языке.

## Локальная сборка

Нужны [uv](https://docs.astral.sh/uv/) и Python 3.14+. Версии зависимостей записаны в `uv.lock`.

```bash
uv sync
uv run python Gmeek.py <github_token> <owner/repo>
uv run pytest
```

`Gmeek.py` читает `config.json` и `templates/` из текущего каталога. Он записывает `docs/`, `backup/` и `blogBase.json`. Если сборка что-то изменила, он также перезаписывает `README.md` в текущем каталоге. Запускайте сборку в отдельном каталоге, чтобы сохранить этот README.

## Структура репозитория

| Путь | Содержимое |
|---|---|
| `Gmeek.py` | Точка входа. Читает Issues, создает страницы и записывает `docs/`. |
| `templates/` | Шаблоны Jinja2 для макета, главной страницы, статьи, страницы меток и подвала. |
| `plugins/` | Необязательные браузерные плагины: оглавление, просмотр изображений и счетчики просмотров. |
| `tests/` | Модульные тесты pytest. |
| `pyproject.toml` | Метаданные проекта и зависимости uv. |
| `uv.lock` | Зафиксированные версии зависимостей. |
| `CONFIG.md` | Справочник по настройке. |
| `img/` | Изображения для README. |

Gmeek не загружает `plugins/` автоматически. Скопируйте нужный плагин в каталог `static/` репозитория блога или подключите его через поле `script` или `style` в `config.json`.

## Возможности

- Интерфейс использует CSS GitHub: [primer.style](https://primer.style/css)
- Запись в Issues запускает сборку и публикацию
- Пагинация, фильтр по меткам и поиск по сайту
- RSS, `sitemap.txt` и индекс `postList.json`
- Формулы MathJax, стили GitHub alert, подсветка кода и кнопка копирования
- Комментарии через [utteranc.es](https://utteranc.es/)
- Рендеринг через `jinja2`; тему можно изменить в шаблонах
- Интерфейс на китайском, английском и русском языках

## Тесты

Запустите `uv run pytest`. Тесты проверяют разбор параметров статьи, извлечение описания, очистку имени файла, контраст текста и рендеринг шаблона статьи.

## Вопросы

Перед созданием [Issue](https://github.com/Meekdai/Gmeek/issues) выполните полную пересборку. Если ошибка осталась, создайте Issue и приложите журнал сборки.

## Благодарность

- [jinja2](https://jinja.palletsprojects.com/)
- [utteranc.es](https://utteranc.es/)
- [primer.style](https://primer.style/css)
- [gitblog](https://github.com/yihong0618/gitblog)

## Лицензия

Сохраните уведомление об авторских правах в подвале страницы и в консоли браузера.
