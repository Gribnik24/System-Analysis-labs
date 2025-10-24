import streamlit as st
import pandas as pd
import numpy as np

# Настройка страницы
st.set_page_config(
    page_title="Опрос",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def main():
    # Заголовок
    st.title('Оценка вариантов по строительству торгового центра')
    st.info("""
    Уважаемый эксперт! В рамках исследования просим Вас оценить 4 варианта строительства торгового центра:
    """)

    # Определяем варианты
    options = [
        'Достройка одноэтажного неиспользуемого помещения в центральном районе города',
        'Строительство нового супермаркета, требующее крупных капиталовложений, с выгодным расположением',
        'Строительство супермаркета за чертой города с небольшими затратами',
        'Строительство торгового центра на окраине города (район оснащен развитой транспортной сетью и паркингом)'
    ]

    # Создаем DataFrame для отображения
    df = pd.DataFrame({'Варианты': options})
    df.index = np.arange(1, len(df) + 1)
    st.table(df)

    # Ввод ФИО
    st.markdown('Прежде всего, пожалуйста введите свое ФИО:')
    name = st.text_input("ФИО", placeholder="Введите ваше полное имя")

    # Основные вопросы с слайдерами
    st.markdown('---')
    st.header('Попарное сравнение вариантов')
    st.markdown('Пожалуйста, оцените, в скольких случаях из 15 вы считаете один вариант лучше другого:')

    # Создаем словарь для хранения оценок
    scores = {}

    # Генерируем все уникальные пары вариантов
    for i in range(len(options)):
        for j in range(i + 1, len(options)):
            option_a = options[i]
            option_b = options[j]

            st.markdown(f'**Сравнение:** "{option_a}" **против** "{option_b}"')

            # Создаем два столбца для лучшего отображения
            col1, col2 = st.columns(2)

            with col1:
                score_ab = st.slider(
                    f'Случаев, когда "{option_a}" лучше, чем "{option_b}"',
                    min_value=0,
                    max_value=15,
                    value=7,
                    key=f'{i}_{j}_ab',
                    help="0 - никогда не лучше, 15 - всегда лучше"
                )

                # Визуальная индикация оценки
                st.metric("Оценка", f"{score_ab}/15")
                st.progress(score_ab / 15)

            with col2:
                score_ba = st.slider(
                    f'Случаев, когда "{option_b}" лучше, чем "{option_a}"',
                    min_value=0,
                    max_value=15,
                    value=7,
                    key=f'{i}_{j}_ba',
                    help="0 - никогда не лучше, 15 - всегда лучше"
                )

                # Визуальная индикация оценки
                st.metric("Оценка", f"{score_ba}/15")
                st.progress(score_ba / 15)

            # Сохраняем оценки
            scores[f'{i}_{j}_ab'] = score_ab
            scores[f'{i}_{j}_ba'] = score_ba

            # Проверка согласованности (сумма должна быть <= 15)
            total = score_ab + score_ba
            if total > 15:
                st.warning(f"⚠️ Сумма оценок ({total}) превышает 15 случаев. Пожалуйста, проверьте ваши оценки.")
            elif total < 15:
                st.info(f"ℹ️ В {15 - total} случаях варианты равнозначны.")

            st.markdown('---')

    # Кнопка отправки
    if st.button("📤 Отправить ответ", type="primary", use_container_width=True):
        if not name.strip():
            st.error("Пожалуйста, введите ваше ФИО перед отправкой.")
        else:
            st.success(f'Большое спасибо, {name}! Ваши ответы сохранены.')


if __name__ == "__main__":
    main()