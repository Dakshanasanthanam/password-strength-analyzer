
import streamlit as st
import secrets
import string
import re

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Password Security Lab",
    page_icon="🔐",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #14213d);
    color: #f1f5f9;
}
.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}
.hero {
    background: #172642;
    border: 1px solid #334766;
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 22px;
}
.hero h1 { color: #67e8f9; }
.panel {
    background: #172642;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #334766;
    margin-bottom: 12px;
}
</style>

<div class="hero">
    <h1>🔐 Password Security Lab</h1>
    <p>Analyze password patterns, generate random passwords,
    and learn safer cybersecurity habits.</p>
</div>
""", unsafe_allow_html=True)

st.warning(
    "Use made-up test passwords only. Never enter a password "
    "you actually use."
)

# ---------------- PASSWORD ANALYZER ----------------
def analyze_password(password):
    suggestions = []
    common_passwords = {
        "password", "password123", "12345678",
        "123456789", "qwerty", "admin123",
        "iloveyou", "welcome123", "abc123"
    }

    length = len(password)
    lower = any(c.islower() for c in password)
    upper = any(c.isupper() for c in password)
    digit = any(c.isdigit() for c in password)
    symbol = any(not c.isalnum() and not c.isspace()
                 for c in password)

    if length < 12:
        suggestions.append(
            "Use at least 12 characters; longer is generally better."
        )
    if not lower:
        suggestions.append("Consider using lowercase letters.")
    if not upper:
        suggestions.append("Consider using uppercase letters.")
    if not digit:
        suggestions.append("Consider including numbers.")
    if not symbol:
        suggestions.append("Consider including symbols.")
    if password.lower() in common_passwords:
        suggestions.append(
            "This is a common password example. Choose something unique."
        )
    if re.search(r"(.)\1{2,}", password):
        suggestions.append(
            "Avoid repeating the same character many times."
        )
    if re.search(r"1234|abcd|qwerty", password.lower()):
        suggestions.append(
            "Avoid predictable sequences and keyboard patterns."
        )

    score = 0
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1
    if sum([lower, upper, digit, symbol]) >= 3:
        score += 1
    if length >= 20:
        score += 1

    if password.lower() in common_passwords:
        score = 0
    elif re.search(r"(.)\1{2,}|1234|abcd|qwerty",
                   password.lower()):
        score = max(0, score - 1)

    if score <= 1:
        label = "Needs improvement"
    elif score <= 3:
        label = "Fair"
    else:
        label = "Good checklist result"

    if not suggestions:
        suggestions.append(
            "No basic checklist issues detected. Use a unique password "
            "and consider a password manager."
        )

    return score, label, suggestions, [
        ("12+ characters", length >= 12),
        ("Lowercase letters", lower),
        ("Uppercase letters", upper),
        ("Numbers", digit),
        ("Symbols", symbol),
    ]


# ---------------- NAVIGATION ----------------
analyzer_tab, generator_tab, tips_tab = st.tabs([
    "🔎 Password Analyzer",
    "🎲 Password Generator",
    "🛡️ Security Tips"
])

# ---------------- ANALYZER TAB ----------------
with analyzer_tab:
    st.subheader("Analyze a sample password")
    st.caption(
        "This is a basic educational checklist, not a guarantee "
        "of real-world password security."
    )

    password = st.text_input(
        "Enter a sample password",
        type="password",
        placeholder="Try a made-up password"
    )

    if st.button("Analyze Password", type="primary"):
        if not password:
            st.info("Please enter a sample password.")
        else:
            score, label, suggestions, checks = analyze_password(
                password
            )

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Checklist score", f"{score}/5")
                st.progress(score / 5)
            with col2:
                st.markdown(f"### {label}")
                st.write(f"Length: {len(password)} characters")

            st.subheader("Security checklist")
            for name, passed in checks:
                st.write(
                    f"{'✅' if passed else '○'} {name}"
                )

            st.subheader("Suggestions")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")

# ---------------- GENERATOR TAB ----------------
with generator_tab:
    st.subheader("Generate a random password")
    st.write(
        "Uses Python's cryptographically secure secrets module."
    )

    length = st.slider("Password length", 12, 64, 20)

    use_lower = st.checkbox("Lowercase letters", value=True)
    use_upper = st.checkbox("Uppercase letters", value=True)
    use_digits = st.checkbox("Numbers", value=True)
    use_symbols = st.checkbox("Symbols", value=True)

    if st.button("Generate Password", type="primary"):
        groups = []

        if use_lower:
            groups.append(string.ascii_lowercase)
        if use_upper:
            groups.append(string.ascii_uppercase)
        if use_digits:
            groups.append(string.digits)
        if use_symbols:
            groups.append("!@#$%^&*()-_=+?")

        if not groups:
            st.error("Select at least one character type.")
        else:
            chars = [secrets.choice(group) for group in groups]
            alphabet = "".join(groups)

            chars.extend(
                secrets.choice(alphabet)
                for _ in range(length - len(chars))
            )

            secrets.SystemRandom().shuffle(chars)
            generated = "".join(chars)

            st.session_state["generated_password"] = generated

    if st.session_state.get("generated_password"):
        st.success("Password generated!")
        st.code(
            st.session_state["generated_password"],
            language=None
        )
        st.caption(
            "Store generated passwords in a trusted password manager. "
            "Never reuse a password across accounts."
        )

# ---------------- SECURITY TIPS TAB ----------------
with tips_tab:
    st.markdown("""
    <div class="panel">
    <h3>🔑 1. Prioritize length</h3>
    Longer passwords or passphrases are generally harder to guess.
    </div>

    <div class="panel">
    <h3>♻️ 2. Never reuse passwords</h3>
    Use a different password for every important account.
    </div>

    <div class="panel">
    <h3>🚫 3. Avoid predictable patterns</h3>
    Names, birthdays and keyboard sequences can be easier to guess.
    </div>

    <div class="panel">
    <h3>🛡️ 4. Enable MFA</h3>
    Multi-factor authentication or passkeys add another layer
    of protection where available.
    </div>

    <div class="panel">
    <h3>🔐 5. Use a password manager</h3>
    A reputable password manager can help you create and store
    unique passwords.
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.caption(
    "Password Security Lab | Student Cybersecurity Project | "
    "Educational tool only — not a professional security assessment."
)

