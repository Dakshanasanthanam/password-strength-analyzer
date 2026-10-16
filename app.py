import streamlit as st

st.set_page_config(
    page_title="Password Strength Analyzer",
    page_icon="🔐"
)

st.title("🔐 Password Strength Analyzer")
st.write("Check password characteristics with this educational tool.")
st.warning("Use sample passwords only. Never enter a real password.")

password = st.text_input(
    "Enter a sample password",
    type="password"
)

if st.button("Analyze Password"):
    if not password:
        st.info("Please enter a sample password.")
    else:
        score = 0

        if len(password) >= 8:
            score += 1

        if any(c.isupper() for c in password):
            score += 1

        if any(c.islower() for c in password):
            score += 1

        if any(c.isdigit() for c in password):
            score += 1

        if any(not c.isalnum() and not c.isspace()
               for c in password):
            score += 1

        st.subheader(f"Score: {score}/5")

        if score <= 2:
            st.error("Checklist result: Weak")
        elif score <= 4:
            st.warning("Checklist result: Medium")
        else:
            st.success("Checklist result: Strong")

        st.write("### Suggestions")

        if len(password) < 8:
            st.write("- Use at least 8 characters.")
        if not any(c.isupper() for c in password):
            st.write("- Add an uppercase letter.")
        if not any(c.islower() for c in password):
            st.write("- Add a lowercase letter.")
        if not any(c.isdigit() for c in password):
            st.write("- Add a number.")
        if not any(not c.isalnum() and not c.isspace()
                   for c in password):
            st.write("- Add a special character.")

        st.caption(
            "This is a basic character checklist, "
            "not a guarantee of password security."
        )
