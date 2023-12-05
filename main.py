import streamlit as st
from gramformer import Gramformer
import torch
from spellchecker import SpellChecker
from gtts import gTTS
import os


def set_seed(seed):
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


set_seed(1212)

gf = Gramformer(models=1, use_gpu=False)

spell = SpellChecker()

if "messages" not in st.session_state:
    st.session_state.messages = []


def talk(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')
    os.system('mpg123 output.mp3')


st.title("Spell and Grammar Checker")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Spelling Checker")
    sentence = st.text_input("Enter a sentence or a word for spelling check:")
    if st.button("Check Spelling"):
        words = sentence.split()
        corrected_text = " ".join(spell.correction(word) for word in words)
        misspelled = spell.unknown(words)

        st.session_state.messages.append({"role": "user", "content": sentence})
        with st.chat_message("user"):
            st.markdown(sentence)

        assistant_response = f"Corrected: {corrected_text}\nMisspelled: {', '.join(misspelled)}"

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        talk(corrected_text)

with col2:
    st.subheader("Grammar Checker")
    sentence = st.text_input("Enter a sentence for grammar check:")
    if st.button("Check Grammar"):
        corrected_sentences = gf.correct(sentence, max_candidates=1)

        st.session_state.messages.append({"role": "user", "content": sentence})
        with st.chat_message("user"):
            st.markdown(sentence)

        for corrected_sentence in corrected_sentences:
            st.session_state.messages.append({"role": "assistant", "content": corrected_sentence})
            with st.chat_message("assistant"):
                st.markdown(corrected_sentence)
            talk(corrected_sentence)

