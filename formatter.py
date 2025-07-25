from tabulate import tabulate

# 📋 Форматированный вывод фильмов в консоль (таблица)
def print_results(results, start_index=1):
    """
    Выводит фильмы в виде таблицы в консоли с общей нумерацией.
    :param results: список фильмов (title, year, description)
    :param start_index: с какого номера начинать нумерацию (для пагинации)
    """
    if not results:
        print("⚠️ Нет результатов.\n")
        return

    headers = ["#", "Название", "Год", "Описание (до 100 символов)"]
    table = [
        [start_index + i, title, year,
         (desc[:100] + "...") if desc and len(desc) > 100 else desc]
        for i, (title, year, desc) in enumerate(results)
    ]
    print(tabulate(table, headers=headers, tablefmt="grid"))
    print()


# 💬 Форматирование фильмов для Telegram (Markdown)
def format_film_list(films, start_index=1):
    """
    Возвращает отформатированный список фильмов в виде Markdown-строки
    для отправки в Telegram.
    :param films: список фильмов (title, year, description)
    :param start_index: порядковый номер начала (при пагинации)
    :return: строка Markdown
    """
    lines = []
    for i, (title, year, description) in enumerate(films, start=start_index):
        desc = description or ""
        desc_short = desc[:80].replace("*", "\\*").replace("_", "\\_")
        title_safe = title.replace("*", "\\*").replace("_", "\\_")

        lines.append(f"*{i}. {title_safe}* ({year})\n_{desc_short}_\n")
    return "\n".join(lines)
