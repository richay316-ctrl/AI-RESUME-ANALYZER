import matplotlib.pyplot as plt
import streamlit as st



def pie_chart(score):

    fig,ax=plt.subplots()


    ax.pie(
        [
            score,
            100-score
        ],
        labels=[
            "Matched",
            "Missing"
        ],
        autopct="%1.1f%%"
    )


    st.pyplot(fig)



def gauge_chart(score):

    fig,ax=plt.subplots()


    ax.barh(
        [0],
        [score]
    )


    ax.set_xlim(
        0,
        100
    )


    st.pyplot(fig)