document.addEventListener("DOMContentLoaded", () => {
    const supportedLanguages = [
        { code: "en", name: "English" },
        { code: "fr", name: "Français" },
        { code: "pt", name: "Português" },
        { code: "sw", name: "Kiswahili" },
        { code: "zu", name: "Zulu" },
        { code: "yo", name: "Yorùbá" },
        { code: "ar", name: "العربية" },
    ];

    function getCurrentLanguage() {
        const path = window.location.pathname;
        const match = path.match(
            /\/(en|fr|pt|sw|zu|yo|ar)(?=\/|$)/
        );
        return match ? match[1] : "en";
    }

    function buildLanguagePicker() {
        const currentLanguage = getCurrentLanguage();

        const picker = document.createElement("div");
        picker.className = "lugha-language-picker";
        picker.setAttribute("aria-label", "Language selector");

        const button = document.createElement("button");
        button.className = "lugha-language-button";
        button.type = "button";
        button.setAttribute("aria-haspopup", "true");
        button.setAttribute("aria-expanded", "false");
        button.setAttribute("aria-label", "Select language");

        button.innerHTML = `
            <span class="lugha-language-globe" aria-hidden="true">
                ◎
            </span>

            <span class="lugha-current-language">
                ${
                    supportedLanguages.find(
                        (language) => language.code === currentLanguage
                    )?.name || "English"
                }
            </span>

            <span class="lugha-chevron" aria-hidden="true">
                ⌄
            </span>
        `;

        const menu = document.createElement("div");
        menu.className = "lugha-language-menu";
        menu.setAttribute("role", "menu");

        const label = document.createElement("div");
        label.className = "lugha-language-label";
        label.textContent = "Language";

        menu.appendChild(label);

        supportedLanguages.forEach((language) => {
            const option = document.createElement("a");

            option.href = "#";
            option.dataset.language = language.code;
            option.className = "lugha-language-option";
            option.setAttribute("role", "menuitem");

            const name = document.createElement("span");
            name.textContent = language.name;

            option.appendChild(name);

            if (language.code === currentLanguage) {
                option.setAttribute("aria-current", "true");

                const check = document.createElement("span");
                check.className = "lugha-check";
                check.setAttribute("aria-hidden", "true");
                check.textContent = "✓";

                option.appendChild(check);
            }

            menu.appendChild(option);
        });

        picker.appendChild(button);
        picker.appendChild(menu);

        document.body.appendChild(picker);

        return {
            picker,
            button,
            menu,
        };
    }

    function buildLanguageUrl(targetLanguage) {
        const currentPath = window.location.pathname;
        const currentLanguage = getCurrentLanguage();

        if (targetLanguage === currentLanguage) {
            return currentPath;
        }

        if (targetLanguage === "en") {
            if (currentLanguage === "en") {
                return currentPath;
            }

            const languagePrefix = `/${currentLanguage}`;

            const englishPath = currentPath.replace(
                languagePrefix,
                ""
            );

            return englishPath || "/";
        }

        if (currentLanguage === "en") {
            return `/${targetLanguage}${currentPath}`;
        }

        const currentLanguagePrefix = `/${currentLanguage}`;

        return currentPath.replace(
            currentLanguagePrefix,
            `/${targetLanguage}`
        );
    }

    const { picker, button } = buildLanguagePicker();
    const options = picker.querySelectorAll(".lugha-language-option");

    function openPicker() {
        picker.classList.add("is-open");
        button.setAttribute("aria-expanded", "true");
    }

    function closePicker() {
        picker.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
    }

    button.addEventListener("click", (event) => {
        event.stopPropagation();

        if (picker.classList.contains("is-open")) {
            closePicker();
        } else {
            openPicker();
        }
    });

    options.forEach((option) => {
        option.addEventListener("click", (event) => {
            event.preventDefault();

            const targetLanguage = option.dataset.language;
            const destination = buildLanguageUrl(targetLanguage);

            window.location.href = destination;
        });
    });

    document.addEventListener("click", (event) => {
        if (!picker.contains(event.target)) {
            closePicker();
        }
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            closePicker();
            button.focus();
        }
    });

    const currentLanguage = getCurrentLanguage();

    if (currentLanguage === "ar") {
        document.documentElement.dir = "rtl";
        document.documentElement.lang = "ar";
    } else {
        document.documentElement.dir = "ltr";
        document.documentElement.lang = currentLanguage;
    }
});