import React, { useState, useEffect, useRef, RefObject } from "react";
import { Outlet, NavLink, Link } from "react-router-dom";
import { useTranslation } from "react-i18next";
import styles from "./Layout_Login.module.css";

import { useLogin } from "../../authConfig";

import { LoginButton } from "../../components/LoginButton";
import { IconButton } from "@fluentui/react";
import { LanguagePicker } from "../../i18n/LanguagePicker";
import {
    configApi,
} from "../../api";

const Layout = () => {
    const [showLanguagePicker, setshowLanguagePicker] = useState<boolean>(false);
    const { t, i18n } = useTranslation();
    const [menuOpen, setMenuOpen] = useState(false);
    const menuRef: RefObject<HTMLDivElement> = useRef(null);

    const toggleMenu = () => {
        setMenuOpen(!menuOpen);
    };

    const handleClickOutside = (event: MouseEvent) => {
        if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
            setMenuOpen(false);
        }
    };

    const getConfig = async () => {
        configApi().then(config => {
            setshowLanguagePicker(config.showLanguagePicker);

        });
    };

    useEffect(() => {
        if (menuOpen) {
            document.addEventListener("mousedown", handleClickOutside);
        } else {
            document.removeEventListener("mousedown", handleClickOutside);
        }
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [menuOpen]);

    useEffect(() => {
        getConfig();
    }, []);

    return (
        <div className={styles.layout}>
            <header className={styles.header} role={"banner"}>
                <div className={styles.headerContainer} ref={menuRef}>
                    <Link to="/" className={styles.headerTitleContainer}>
                        <h3 className={styles.headerTitle}>{t("headerTitle")}</h3>
                    </Link>
                    <div></div>
                    <div className={styles.loginMenuContainer}>
                        {/* {showLanguagePicker && <LanguagePicker onLanguageChange={newLang => i18n.changeLanguage(newLang)} />} */}
                        {useLogin && <LoginButton />}
                        <IconButton
                            iconProps={{ iconName: "GlobalNavButton" }}
                            className={styles.menuToggle}
                            onClick={toggleMenu}
                            ariaLabel={t("labels.toggleMenu")}
                        />

                    </div>
                </div>
            </header>

            <Outlet />
        </div>
    );
};

export default Layout;
