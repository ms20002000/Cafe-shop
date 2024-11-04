function validatePasswords() {
    const password1 = document.getElementById('password1').value;
    const password2 = document.getElementById('password2').value;
    if (password1 !== password2) {
        alert('رمز عبور و تکرار آن باید یکسان باشند.');
        return false;
    }

    if (password1.length < 8) {
        alert('رمز عبور باید حداقل ۸ کاراکتر باشد.');
        return false;
    }

    if (/^\d+$/.test(password1)) {
        alert('رمز عبور نمی‌تواند به‌طور کامل عددی باشد.');
        return false;
    }
    return true;
}