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

    // Sphinx writes the language of this build into DOCUMENTATION_OPTIONS and
    // into the lang attribute of the html element. DOCUMENTATION_OPTIONS is a
    // top level const, so it is not a property of window.
    function getCurrentLanguage() {
        const fromOptions =
            typeof DOCUMENTATION_OPTIONS !== "undefined"
                ? DOCUMENTATION_OPTIONS.LANGUAGE
                : undefined;

        const candidate = fromOptions || document.documentElement.lang;
        const code = (candidate || "en").split(/[-_]/)[0];

        return supportedLanguages.some((language) => language.code === code)
            ? code
            : "en";
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

            option.href = buildLanguageUrl(language.code);
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

    // English lives at the site root and every other language in its own folder,
    // for example /lugha-api-docs/ and /lugha-api-docs/fr/. Sphinx stores the path
    // back to the root of the current build in data-content_root, so this works
    // on any host and under any base path, including GitHub project pages.
    function buildLanguageUrl(targetLanguage) {
        const currentLanguage = getCurrentLanguage();
        const contentRoot = document.documentElement.dataset.content_root || "./";
        const buildRoot = new URL(contentRoot, window.location.href).pathname;

        const pagePath = window.location.pathname.slice(buildRoot.length);

        const siteRoot =
            currentLanguage === "en"
                ? buildRoot
                : buildRoot.replace(new RegExp(`${currentLanguage}/$`), "");

        const targetRoot =
            targetLanguage === "en" ? siteRoot : `${siteRoot}${targetLanguage}/`;

        return `${targetRoot}${pagePath}${window.location.search}${window.location.hash}`;
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
        // Rebuild the link on click so the current hash and search are kept.
        option.addEventListener("click", () => {
            option.href = buildLanguageUrl(option.dataset.language);
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

    const activeLanguage = getCurrentLanguage();

    if (activeLanguage === "ar") {
        document.documentElement.dir = "rtl";
        document.documentElement.lang = "ar";
    } else {
        document.documentElement.dir = "ltr";
        document.documentElement.lang = activeLanguage;
    }
});