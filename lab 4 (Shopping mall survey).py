import streamlit as st
import pandas as pd
import numpy as np

# Настройка страницы
st.set_page_config(
    page_title="Экспертная оценка проектов",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    # Заголовок
    st.title('Экспертная оценка вариантов строительства торгового центра')
    st.info("""
    Уважаемый эксперт! Просим Вас попарно сравнить варианты строительства торгового центра 
    и оценить, насколько один вариант предпочтительнее другого.
    """)

    # Определяем варианты
    options = [
        'Достройка одноэтажного неиспользуемого помещения в центральном районе города',
        'Строительство нового супермаркета, требующее крупных капиталовложений, с выгодным расположением',
        'Строительство супермаркета за чертой города с небольшими затратами',
        'Строительство торгового центра на окраине города (район оснащен развитой транспортной сетью и паркингом)'
    ]

    # Создаем DataFrame для отображения
    df = pd.DataFrame({'Варианты строительства': options})
    df.index = np.arange(1, len(df) + 1)
    st.table(df)

    # Ввод ФИО
    st.markdown('---')
    st.markdown('**Прежде всего, пожалуйста, введите свое ФИО:**')
    name = st.text_input("ФИО эксперта", placeholder="Введите ваше полное имя", label_visibility="collapsed")

    # Инструкция для эксперта
    st.markdown('---')
    st.header('Попарное сравнение вариантов')

    st.success("""
    **Инструкция:** 
    Для каждой пары вариантов распределите 15 баллов между ними в соответствии с тем, 
    насколько один вариант предпочтительнее другого. 

    **Пример:**
    - Если вариант A значительно лучше варианта B → A: 12 баллов, B: 3 балла
    - Если варианты примерно равны → A: 8 баллов, B: 7 баллов  
    - Если вариант A немного лучше варианта B → A: 9 баллов, B: 6 баллов

    **Общее количество баллов для каждой пары должно равняться 15.**
    """)

    # Создаем словарь для хранения оценок
    scores = {}

    # Генерируем все уникальные пары вариантов
    for i in range(len(options)):
        for j in range(i + 1, len(options)):
            option_a = options[i]
            option_b = options[j]

            st.markdown(f'### Сравнение: **Вариант {i + 1}** vs **Вариант {j + 1}**')

            # Краткое описание для удобства
            col_desc1, col_desc2 = st.columns(2)
            with col_desc1:
                st.caption(f"**Вариант {i + 1}:** {option_a}")
            with col_desc2:
                st.caption(f"**Вариант {j + 1}:** {option_b}")

            # Создаем два столбца для распределения баллов
            col1, col2 = st.columns([2, 2])

            with col1:
                st.markdown(f"**Баллы для Варианта {i + 1}:**")
                score_a = st.slider(
                    f"Баллы для варианта {i + 1}",
                    min_value=0,
                    max_value=15,
                    value=7,
                    key=f'{i}_{j}_a',
                    help=f"Сколько баллов присвоить варианту '{option_a[:50]}...'?"
                )

            with col2:
                st.markdown(f"**Баллы для Варианта {j + 1}:**")
                score_b = st.slider(
                    f"Баллы для варианта {j + 1}",
                    min_value=0,
                    max_value=15,
                    value=8,
                    key=f'{i}_{j}_b',
                    help=f"Сколько баллов присвоить варианту '{option_b[:50]}...'?"
                )


            st.markdown("**Проверка:**")
            total = score_a + score_b
            if total == 15:
                st.success("✓ Сумма: 15")
            else:
                st.error(f"✗ Сумма: {total}")
                st.warning("Сумма баллов должна равняться 15!")

            # Визуализация распределения
            st.markdown("**Распределение баллов:**")
            col_prog1, col_prog2 = st.columns(2)

            with col_prog1:
                st.metric(f"Вариант {i + 1}", f"{score_a} баллов")
                st.progress(score_a / 15)

            with col_prog2:
                st.metric(f"Вариант {j + 1}", f"{score_b} баллов")
                st.progress(score_b / 15)

            # Сохраняем оценки
            scores[f'{i}_{j}_a'] = score_a
            scores[f'{i}_{j}_b'] = score_b

            st.markdown('---')

    # Кнопка отправки с проверкой
    st.markdown('### Завершение оценки')

    if st.button("📤 Отправить экспертную оценку", type="primary", use_container_width=True):
        if not name.strip():
            st.error("Пожалуйста, введите ваше ФИО перед отправкой.")
        else:
            # Проверяем все суммы
            all_valid = True
            error_pairs = []

            for i in range(len(options)):
                for j in range(i + 1, len(options)):
                    total = scores[f'{i}_{j}_a'] + scores[f'{i}_{j}_b']
                    if total != 15:
                        all_valid = False
                        error_pairs.append(f"Варианты {i + 1} и {j + 1} (сумма: {total})")

            if not all_valid:
                st.error("Не все пары имеют сумму баллов равную 15!")
                st.write("**Ошибки в парах:**")
                for pair in error_pairs:
                    st.write(f"- {pair}")
                st.warning("Пожалуйста, исправьте отмеченные пары перед отправкой.")
            else:
                # Все проверки пройдены
                st.success(f'Большое спасибо, {name}! Ваша экспертная оценка сохранена.')


if __name__ == "__main__":
    main()