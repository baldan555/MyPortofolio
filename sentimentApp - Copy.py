import streamlit as st
from sentiment_model import analyze_sentiment

def main():
    # Setup Streamlit
    st.markdown("<h1 style='text-align: center;'>Sentiment Analysis</h1>", unsafe_allow_html=True)

    st.info("""
        **Information**:
        - To try, Please insert you text in the box.
        - The model provide in this app is the pre-trained model by HuggingFace
        """)

    # Add custom CSS for styling
    st.markdown("""
        <style>
            .title {
                font-size: 32px;
                font-weight: bold;
                color: #2D2D2D;
                text-align: center;
            }
            .card {
                background-color: #F0F2F6;
                border-radius: 8px;
                padding: 20px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                margin: 20px 0;
            }
            .input-box {
                font-size: 16px;
                padding: 10px;
                width: 100%;
                border-radius: 4px;
                border: 1px solid #DDDDDD;
            }
            .result {
                font-size: 18px;
                font-weight: bold;
            }
            .confidence {
                font-size: 16px;
                color: #5A5A5A;
            }
        </style>
    """, unsafe_allow_html=True)

    # Input Text
    tweet_text = st.text_area('Masukkan teks tweet untuk analisis:', '', height=150, max_chars=280, key='tweet_input', placeholder='Tulis teks tweet di sini...')

    # Add submit button
    submit_button = st.button("Analyze Sentiment")

    if submit_button and tweet_text:
        # Analyze sentiment
        sentiment_result = analyze_sentiment(tweet_text)

        # Display results in a card
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div class="result">Sentiment: {sentiment_result[0]["label"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="confidence">Confidence: {sentiment_result[0]["score"]:.2f}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()