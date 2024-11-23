import React, { useState, useContext } from "react";
import { useMsal } from "@azure/msal-react";
import { useTranslation } from "react-i18next";
import { LoginContext } from "../../loginContext";
import { loginRequest } from "../../authConfig";
import "./LoginPage.css";

const LoginPage: React.FC = () => {
    const { instance } = useMsal();
    const { setLoggedIn } = useContext(LoginContext);
    const { t } = useTranslation();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await instance.loginPopup(loginRequest);
            setLoggedIn(true);
        } catch (err) {
            setError(t("loginError"));
        }
    };

    return (
        <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <div className="form-group">
                    <label htmlFor="email">Azure Account</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </div>
                {error && <p className="error">{error}</p>}
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default LoginPage;